import pyglet
import res, batch, group
from Camera import *
from Vector import *

class Crosshair(pyglet.sprite.Sprite, CameraRelativeSprite):

    def __init__(self, y):

        pyglet.sprite.Sprite.__init__(self, res.IMG_CROSSHAIR, batch=batch.main, group=group.foreground)
        CameraRelativeSprite.__init__(self)
        self.vpos.y = y
        self.vscale = 0.6

    def update(self, rot, dt):
        self.rotation = rot