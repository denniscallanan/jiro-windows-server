import jgsapi, pyglet, math, batch, res
from Vector import *
from Camera import *
from Turret import *
from Bullet import *

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
jiro.importController("controllers/turret.xml")

# Create Window

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(116/255.0, 29/255.0, 29/255.0, 1)

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
    jiro.switchController("turret", addr)
    queue.append({"type": "createPlayer", "addr": addr})

@jiro.event
def on_player_leave(addr):
    print jgsapi.pretty_ip(addr), "left app"
    player = Turret.instances.get(addr, None)
    Turret.instances.pop(addr, None)
    if player != None:
        player.delete()

@jiro.event
def cleanup():
    queue.append({"type": "cleanup"})

def cleanup():
    for addr in Turret.instances.keys():
        on_player_leave(addr)
    window.close()
    pyglet.app.exit()
    print "Turrets server stopped!"

#######################################
# CONTROLLER EVENTS
#######################################

turret_controller = jiro.getController("turret")
btn_shoot = turret_controller.getInteractable("shoot")
btn_power = turret_controller.getInteractable("power")

@turret_controller.event
def accelerometer(event):
    turret = Turret.instances.get(event.addr, None)
    if turret == None: return
    turret.rot_velocity = event.y

@btn_shoot.event
def tapStart(event):
    turret = Turret.instances.get(event.addr, None)
    if turret == None: return
    turret.shooting = 1
    turret.shoot_end_time = 0

@btn_shoot.event
def tapEnd(event):
    turret = Turret.instances.get(event.addr, None)
    if turret == None: return
    if turret.shooting == 1:
        turret.shooting = 0

@btn_power.event
def tapStart(event):
    turret = Turret.instances.get(event.addr, None)
    if turret == None: return
    img = turret.power_shoot()
    #queue.append({"type": "changeTurretImage", "addr": event.addr, "image": img})

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

def process_queue(dt, bounds):
    while len(queue) != 0:
        action = queue.pop(0)
        if action["type"] == "cleanup":
            cleanup()
        elif action["type"] == "createPlayer":
            Turret.instances[action["addr"]] = Turret(bounds)
        elif action["type"] == "changeTurretImage":
            turret = Turret.instances.get(action["addr"], None)
            if turret == None: continue
            turret.image = action["image"]

increase_ammo_time = 0

def update(dt):
    global increase_ammo_time
    increase_ammo_time -= dt
    bounds = cam.get_bounds()
    process_queue(dt, bounds)
    cam.update(dt)
    for t in Turret.instances:
        turret = Turret.instances[t]
        if increase_ammo_time <= 0:
            turret.increase_ammo()
        turret.update(dt)
        turret.shoot(dt)
        turret.relative_to_cam(cam)
    for bullet in Bullet.instances:
        bullet.update(dt)
        bullet.relative_to_cam(cam)
    for bullet in BigBullet.instances:
        bullet.update(dt)
        bullet.relative_to_cam(cam)
    if increase_ammo_time <= 0:
        increase_ammo_time += 0.5

# Start Game Loop

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()