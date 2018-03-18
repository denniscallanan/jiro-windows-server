import jgsapi, pyglet, math, batch
from Vector import *
from Camera import *
from Ball import *
from Platform import *
from BallAirBounceEffect import *
from ObstacleFactory import *

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
jiro.importController("controllers/wait.xml")
jiro.importController("controllers/start.xml")
jiro.importController("controllers/youlose.xml")

# Create Window

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(1, 1, 1, 1)

# Create Camera

cam = Camera(window.width, window.height, fixedheight=True)
cam.zoom = 0.8

# Create Initial Game Objects

#Platform.instances.append(Platform(0, -200, 500, 50))
#Platform.instances.append(Platform(400, 0, 300, 50))

last = -150#750
for i in range(100):
    last += ObstacleFactory.createObstaclePlatforms(last)

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
    queue.append({"type": "destroyPlayer", "addr": addr})

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

'''@smalljump.event
def tapEnd(event):
    ball = Ball.instances.get(event.addr, None)
    if ball != None and ball.target_jump_power == 12:
        ball.target_jump_power = 0'''

@bigjump.event
def tapStart(event):
    ball = Ball.instances.get(event.addr, None)
    if ball != None:
        ball.target_jump_power = 18

'''@bigjump.event
def tapEnd(event):
    ball = Ball.instances.get(event.addr, None)
    if ball != None and ball.target_jump_power == 16:
        ball.target_jump_power = 0'''

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
        if action["type"] == "destroyPlayer":
            player = Ball.instances.get(action["addr"], None)
            if player != None:
                player.delete()
            Ball.instances.pop(action["addr"], None)


def update(dt):
    process_queue()
    cam.update(dt)
    bounds = cam.get_bounds()
    ball_count = float(len(Ball.instances))
    target_cam_pos = Vector(0, 0)
    furthest_ball_x = 0
    for b in Ball.instances:
        ball = Ball.instances[b]
        ball.update(dt)
        ball.check_platform_collisions(Platform.instances)
        ball.update_air_jumps(dt)
        #ball.wrap(bounds)
        #ball.update_top_bounce(bounds)
        target_cam_pos.x += ball.vpos.x / ball_count # average
        if ball.vpos.x > furthest_ball_x and ball.vpos.x > bounds[1].x:
            furthest_ball_x = ball.vpos.x
        if ball.is_out_of_bounds(bounds):
            queue.append({"type": "destroyPlayer", "addr": b})
            jiro.switchController("youlose", b)
    if target_cam_pos.x < cam.pos.x:
        target_cam_pos.x = cam.pos.x
    target_cam_pos.x = max(furthest_ball_x, target_cam_pos.x)
    cam.target_pos(target_cam_pos, 0.5, 1)
    for b in Ball.instances:
        Ball.instances[b].relative_to_cam(cam)
    for platform in Platform.instances:
        platform.relative_to_cam(cam)
    for id in BallAirBounceEffect.instances:
        effect = BallAirBounceEffect.instances.get(id, None)
        if effect == None: continue
        effect.relative_to_cam(cam)
        effect.update(dt)

# Start Game Loop

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()