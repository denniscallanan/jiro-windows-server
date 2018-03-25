import pyglet

IMG_TURRET = pyglet.image.load("res/turretnofire.png")
IMG_TURRET1 = pyglet.image.load("res/turret1.png")
IMG_TURRET2 = pyglet.image.load("res/turret2.png")
IMG_TURRET_FL = pyglet.image.load("res/turretfireleft.png")
IMG_TURRET_FR = pyglet.image.load("res/turretfireright.png")
IMG_TURRET_FP = pyglet.image.load("res/turretfirepower.png")

for img in (IMG_TURRET, IMG_TURRET_FL, IMG_TURRET_FR, IMG_TURRET_FP):
    img.anchor_x = 120
    img.anchor_y = 124

IMG_BULLET = pyglet.image.load("res/bullet.png")
IMG_BIG_BULLET = pyglet.image.load("res/bigbullet.png")

for img in (IMG_TURRET1, IMG_BULLET, IMG_BIG_BULLET):
    img.anchor_x = img.width / 2
    img.anchor_y = img.height / 2