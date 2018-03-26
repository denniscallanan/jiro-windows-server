import pyglet

def centered(img):
    img.anchor_x = img.width / 2
    img.anchor_y = img.height / 2
    return img

IMG_TURRET1 = centered(pyglet.image.load("res/turret1.png"))
IMG_TURRET2 = centered(pyglet.image.load("res/turret2.png"))
IMG_BULLET = centered(pyglet.image.load("res/bullet.png"))
IMG_BIG_BULLET = centered(pyglet.image.load("res/bigbullet.png"))
IMG_ASTROID1 = centered(pyglet.image.load("res/enemy_astroid_1.png"))

IMG_CROSSHAIR = pyglet.image.load("res/crosshair.png")
IMG_CROSSHAIR.anchor_x = IMG_CROSSHAIR.width / 2
IMG_CROSSHAIR.anchor_y = -250

IMG_AMMOLINE = pyglet.image.load("res/ammoline.png")