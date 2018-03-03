import pyglet
import res, batch, group
from Camera import *
from Vector import *

class Platform(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = []

    def __init__(self, x, y, w, h):

        pyglet.sprite.Sprite.__init__(self, res.IMG_PLATFORM, batch=batch.main, group=group.balls)
        CameraRelativeSprite.__init__(self)
        self.vpos.x = x
        self.vpos.y = y
        self.scale_x = w / 2
        self.scale_y = h / 2