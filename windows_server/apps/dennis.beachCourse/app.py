import jgsapi, pyglet, math, batch
from Vector import *
from Camera import *
from Ball import *
from Platform import *

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
cam.zoom = 0.8

# Create Initial Game Objects

Platform.instances.append(Platform(0, -200, 500, 50))

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

ball_controller = jiro.getController("ball")
smalljump = ball_controller.getInteractable("smalljump")
bigjump = ball_controller.getInteractable("bigjump")

@ball_controller.event
def accelerometer(event):
    ball = Ball.instances.get(event.addr, None)
    if ball != None:
        ball.update_acceleration_x(event.y)

@smalljump.event
def tapStart(event):
    ball = Ball.instances.get(event.addr, None)
    if ball != None:
        ball.target_jump_power = 12

@smalljump.event
def tapEnd(event):
    ball = Ball.instances.get(event.addr, None)
    if ball != None:
        ball.target_jump_power = 0

@bigjump.event
def tapStart(event):
    ball = Ball.instances.get(event.addr, None)
    if ball != None:
        ball.target_jump_power = 16

@bigjump.event
def tapEnd(event):
    ball = Ball.instances.get(event.addr, None)
    if ball != None:
        ball.target_jump_power = 0

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
        ball = Ball.instances[b]
        ball.update(dt)
        ball.check_platform_collisions(Platform.instances)
        ball.relative_to_cam(cam)
    for platform in Platform.instances:
        platform.relative_to_cam(cam)

# Start Game Loop

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()