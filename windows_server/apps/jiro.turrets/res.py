import pyglet

IMG_TURRET1 = pyglet.image.load("res/turret1.png")
IMG_TURRET2 = pyglet.image.load("res/turret2.png")
IMG_BULLET = pyglet.image.load("res/bullet.png")
IMG_BIG_BULLET = pyglet.image.load("res/bigbullet.png")

for img in (IMG_TURRET1, IMG_TURRET2, IMG_BULLET, IMG_BIG_BULLET):
    img.anchor_x = img.width / 2
    img.anchor_y = img.height / 2

IMG_CROSSHAIR = pyglet.image.load("res/crosshair.png")
IMG_CROSSHAIR.anchor_x = IMG_CROSSHAIR.width / 2
IMG_CROSSHAIR.anchor_y = -250