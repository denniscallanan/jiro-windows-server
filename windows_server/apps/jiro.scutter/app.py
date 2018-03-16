import jgsapi, pyglet, datetime, math
import res, batch
from Camera import *
from Vector import *
from SpriteSheet import *
from Player import *
from Poop import *
from Fly import *
from ScoreboardBar import *

#######################################
# GLOBAL VARIABLES
#######################################

queue = []
cam         = None  #: Camera
scoreboard  = None  #: ScoreboardBar
fly         = None  #: Fly

#######################################
# INITIALIZATION
#######################################

# Create Game Server

jiro = jgsapi.GameServer()
jiro.importController("controllers/color.xml")
jiro.importController("controllers/wait.xml")
jiro.importController("controllers/waitstart.xml")
jiro.importController("controllers/startgame.xml")
jiro.importController("controllers/spider.xml")

# Create Window

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(1, 1, 1, 1)

# Create Camera

cam = Camera(window.width, window.height)
cam.zoom = 1.8

# Create Initial Game Objects

scoreboard = ScoreboardBar(window.width, window.height)
fly = Fly()
fly.random_pos(cam)

#######################################
# SERVER EVENTS
#######################################

@jiro.event
def on_player_join(addr):
    print jgsapi.pretty_ip(addr), "joined app"
    jiro.switchController("color", addr)
    queue.append({"type": "createPlayer", "addr": addr})
    
    change_back = False
    for addr in Player.instances.keys():
        if jiro.getPlayerControllerName(addr) in ["waitstart", "startgame"]:
            change_back = True
            break

    if change_back:
        for addr in Player.instances.keys():
            if jiro.getPlayerControllerName(addr) in ["waitstart", "startgame"]:
                jiro.switchController("wait", addr)

@jiro.event
def on_player_leave(addr):
    print jgsapi.pretty_ip(addr), "left app"
    player = Player.instances.get(addr, None)
    if player != None:
        player.delete()
    Player.instances.pop(addr, None)
    scoreboard.removePlayer(addr)
    
    change = True
    for target in Player.instances:
        if jiro.getPlayerControllerName(target) == "color":
            change = False
            break

    if change:
        i = 0
        for target in Player.instances:
            if i == 0:
                jiro.switchController("startgame", target)
            else:
                jiro.switchController("waitstart", target)
            i += 1

@jiro.event
def cleanup():
    window.close()
    pyglet.app.exit()
    print "Podium Bounce server stopped!"

#######################################
# COLOR CONTROLLER EVENTS
#######################################

color_controller = jiro.getController("color")

def argdec(*decargs, **deckwargs):
    def decorator(func):
        def wrappedfunc(*args, **kwargs):
            func(*(args + decargs), **dict(kwargs, **deckwargs))
        wrappedfunc.__name__ = func.__name__
        return wrappedfunc
    return decorator

for color in Player.color_tints.keys():
    interactable = color_controller.getInteractable(color)
    @interactable.event
    @argdec(color)
    def tapStart(event, color):
        change_color(event.addr, color)

def change_color(addr, color):
    player = Player.instances.get(addr, None)
    if player != None:
        player.color = Player.color_tints[color]

        change = True
        for target in Player.instances:
            if target != addr and jiro.getPlayerControllerName(target) == "color":
                change = False
                break

        if change:
            i = 0
            for target in Player.instances:
                if i == 0:
                    jiro.switchController("startgame", target)
                else:
                    jiro.switchController("waitstart", target)
                i += 1

            reposition_players_circle()
        else:
            jiro.switchController("wait", addr)

def reposition_players_circle():
    i, length = 0, len(Player.instances)
    for p in Player.instances.keys():
        player = Player.instances.get(p, None)
        if player == None: continue
        player.reset()
        cam_bounds = cam.get_bounds()
        r = min(0 - cam_bounds[0].x, 0 - cam_bounds[0].y)
        r /= 1.1
        t = (float(i) / length) * math.pi * 2
        player.vpos.x = r * math.cos(t)
        player.vpos.y = r * math.sin(t)
        player.rot = math.degrees(t) + 180
        i += 1
    fly.vpos.x = 0
    fly.vpos.y = 0

#######################################
# START GAME CONTROLLER EVENTS
#######################################

startgame_controller = jiro.getController("startgame")
startgame_btn = startgame_controller.getInteractable("button")

@startgame_btn.event
def tapStart(event):
    for addr in Player.instances:
        jiro.switchController("spider", addr)

#######################################
# SPIDER CONTROLLER EVENTS
#######################################

spider_controller = jiro.getController("spider")
btn_move = spider_controller.getInteractable("move")
btn_poo = spider_controller.getInteractable("poo")

@spider_controller.event
def accelerometer(event):
    player = Player.instances.get(event.addr, None)
    if player != None:
        player.rotVelocity = event.y

@btn_move.event
def tapStart(event):
    player = Player.instances.get(event.addr, None)
    if player != None:
        player.moving = True

@btn_move.event
def tapEnd(event):
    player = Player.instances.get(event.addr, None)
    if player != None:
        player.moving = False

@btn_poo.event
def tapStart(event):
    player = Player.instances.get(event.addr, None)
    if player != None:
        player.lastPooTime = datetime.datetime.now()
        player.scuttering = True

@btn_poo.event
def tapEnd(event):
    player = Player.instances.get(event.addr, None)
    if player != None:
        player.scuttering = False

##################################
# WINDOW EVENTS
##################################

@window.event
def on_draw():
    window.clear()
    res.SPR_BG.draw()
    batch.main.draw()

##################################
# UPDATE EVENTS
##################################

def process_queue():
    while len(queue) != 0:
        action = queue.pop(0)
        if action["type"] == "createPlayer":
            Player.instances[action["addr"]] = Player()
            scoreboard.addPlayer(action["addr"], jiro.getPlayerName(action["addr"]))
            cam.target_zoom(min(1.8, 1.0 / max(0.1, math.sqrt(0.3 * len(Player.instances)))), 5)

def update(dt):
    process_queue()
    cam.update()

    # Update Players

    for p in Player.instances.keys():
        player = Player.instances.get(p, None)
        if player != None:
            player.update(dt, cam)
            player.checkPoopCollisions(Poop.instances)
            if player.checkFlyCollision(fly, dt):
                scoreboard.playerScoreAdd(p, 1)
                fly.random_pos(cam)
            player.relative_to_cam(cam)

    # Update Poop

    to_delete = []

    for p in Poop.instances:
        poop = Poop.instances[p]
        if poop.vanished(dt):
            to_delete.append(p)
        poop.relative_to_cam(cam)
    
    for p in to_delete:
        Poop.instances.pop(p, None)

    # Update Fly
    
    fly.relative_to_cam(cam)

# Start Game Loop

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()