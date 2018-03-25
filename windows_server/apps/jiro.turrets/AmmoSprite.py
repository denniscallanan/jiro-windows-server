import pyglet
import res, batch, group
from Camera import *
from Vector import *

class AmmoSprite(pyglet.sprite.Sprite, CameraRelativeSprite):

    def __init__(self, x, y, w):

        pyglet.sprite.Sprite.__init__(self, res.IMG_AMMOLINE, batch=batch.main, group=group.background)
        CameraRelativeSprite.__init__(self)
        self.vpos.x = x
        self.vpos.y = y
        self.w = w
        self.scale_x = 0

    def ammo(self, pc):
        self.scale_x = pc * self.w