import jgsapi, pyglet, datetime
import res, batch
from Camera import *
from Vector import *
from SpriteSheet import *
from Player import *
from Poop import *
from ScoreboardBar import *

#######################################
# GLOBAL VARIABLES
#######################################

cam = None #: Camera
queue = []

#######################################
# INITIALIZATION
#######################################

# Create Game Server

jiro = jgsapi.GameServer()
jiro.importController("controllers/spider.xml")

# Create Window

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(1, 1, 1, 1)

# Create Camera

cam = Camera(window.width, window.height)

# Create Scoreboard

scoreboard = ScoreboardBar(window.width, window.height)

#######################################
# SERVER EVENTS
#######################################

@jiro.event
def on_player_join(addr):
    print jgsapi.pretty_ip(addr), "joined app"
    jiro.switchController("spider", addr)
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
# CONTROLLER EVENTS
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
    batch.poop.draw()
    batch.main.draw()
    batch.indicators.draw()
    batch.overlay1.draw()
    batch.overlay2.draw()
    #label.draw()

##################################
# UPDATE EVENTS
##################################

def process_queue():
    while len(queue) != 0:
        action = queue.pop(0)
        if action["type"] == "createPlayer":
            Player.instances[action["addr"]] = Player()
            scoreboard.addPlayer(action["addr"], jiro.getPlayerName(action["addr"]))

def update(dt):
    cam.zoom = 1.01
    process_queue()
    for addr in Player.instances:
        player = Player.instances[addr]
        player.pooSpeedScalar = 1
        if not player.scuttering or player.pooSecondsLeft <= 0:
            for tup in Poop.instances:
                poo = Poop.instances[tup]
                if poo.checkCollisionWithPlayer(player):
                    val = 0.1 * poo.opacity / 255
                    player.pooSpeedScalar *= 1 - val

    for p in Player.instances:
        #scoreboard.playerScoreAdd(p, 1)
        Player.instances[p].update(dt, cam)
        Player.instances[p].relative_to_cam(cam)
    to_delete = []
    for p in Poop.instances:
        Poop.instances[p].relative_to_cam(cam)
        if Poop.instances[p].vanished(dt):
            to_delete.append(p)
    for p in to_delete:
        Poop.instances.pop(p, None)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()