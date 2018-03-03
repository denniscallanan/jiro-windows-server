import jgsapi, pyglet, math, batch
from Vector import *
from Camera import *
from Ball import *

#######################################
# GLOBAL VARIABLES
#######################################

queue = []
cam = None  #: Camera

#######################################
# INITIALIZATION
#######################################

# Create Game Server

jiro = jgsapi.GameServer()
jiro.importController("controllers/ball.xml")

# Create Window

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(1, 1, 1, 1)

# Create Camera

cam = Camera(window.width, window.height)
cam.zoom = 1

# Create Initial Game Objects


#######################################
# SERVER EVENTS
#######################################

@jiro.event
def on_player_join(addr):
    print jgsapi.pretty_ip(addr), "joined app"
    jiro.switchController("ball", addr)
    queue.append({"type": "createPlayer", "addr": addr})

@jiro.event
def on_player_leave(addr):
    print jgsapi.pretty_ip(addr), "left app"
    player = Ball.instances.get(addr, None)
    if player != None:
        player.delete()
    Ball.instances.pop(addr, None)

@jiro.event
def cleanup():
    window.close()
    pyglet.app.exit()
    print "Podium Bounce server stopped!"


#######################################
# CONTROLLER EVENTS
#######################################


##################################
# WINDOW EVENTS
##################################

@window.event
def on_draw():
    window.clear()
    #res.SPR_BG.draw()
    batch.main.draw()

##################################
# UPDATE EVENTS
##################################

def process_queue():
    while len(queue) != 0:
        action = queue.pop(0)
        if action["type"] == "createPlayer":
            Ball.instances[action["addr"]] = Ball()


def update(dt):
    process_queue()
    cam.update()
    for b in Ball.instances:
        Ball.instances[b].relative_to_cam(cam)
    print cam.zoom

# Start Game Loop

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()