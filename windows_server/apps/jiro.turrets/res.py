import pyglet

IMG_TURRET = pyglet.image.load("res/turretnofire.png")
IMG_TURRET_FL = pyglet.image.load("res/turretfireleft.png")
IMG_TURRET_FR = pyglet.image.load("res/turretfireright.png")
IMG_TURRET_FP = pyglet.image.load("res/turretfirepower.png")

for img in (IMG_TURRET, IMG_TURRET_FL, IMG_TURRET_FR, IMG_TURRET_FP):
    img.anchor_x = 120
    img.anchor_y = 124