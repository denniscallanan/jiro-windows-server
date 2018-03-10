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

@jiro.event
def on_player_leave(addr):
    print jgsapi.pretty_ip(addr), "left app"
    player = Player.instances.get(addr, None)
    if player != None:
        player.delete()
    Player.instances.pop(addr, None)
    scoreboard.removePlayer(addr)

@jiro.event
def cleanup():
    window.close()
    pyglet.app.exit()
    print "Podium Bounce server stopped!"

#######################################
# COLOR CONTROLLER EVENTS
#######################################

color_controller = jiro.getController("color")

#for color in Player.color_tints.keys():
#    interactable = color_controller.getInteractable(color)
#    @interactable.event
#    def tapStart(event):
#        change_color(event.addr, color)

intr = color_controller.getInteractable("color_red")
@intr.event
def tapStart(event):
    change_color(event.addr, "color_red")

intr = color_controller.getInteractable("color_green")
@intr.event
def tapStart(event):
    change_color(event.addr, "color_green")

intr = color_controller.getInteractable("color_blue")
@intr.event
def tapStart(event):
    change_color(event.addr, "color_blue")

intr = color_controller.getInteractable("color_yellow")
@intr.event
def tapStart(event):
    change_color(event.addr, "color_yellow")

intr = color_controller.getInteractable("color_purple")
@intr.event
def tapStart(event):
    change_color(event.addr, "color_purple")

intr = color_controller.getInteractable("color_aqua")
@intr.event
def tapStart(event):
    change_color(event.addr, "color_aqua")

intr = color_controller.getInteractable("color_orange")
@intr.event
def tapStart(event):
    change_color(event.addr, "color_orange")

def change_color(addr, color):
    player = Player.instances.get(addr, None)
    if player != None:
        jiro.switchController("wait", addr)
        player.color = Player.color_tints[color]

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
        if p != None:
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