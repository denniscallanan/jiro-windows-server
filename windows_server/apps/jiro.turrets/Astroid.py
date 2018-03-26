import pyglet
import res, batch, group
from Camera import *
from Vector import *

class Astroid(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = []

    def __init__(self, img, r):

        pyglet.sprite.Sprite.__init__(self, img, batch=batch.main, group=group.bullets)
        CameraRelativeSprite.__init__(self)

        self.r = r
        self.dpos = Vector(0, 0)
        self.speed = 0
        self.vscale = float(r * 2) / img.width

        Astroid.instances.append(self)

    def update(self, dt):
        self.vpos.x += self.dpos.x * dt
        self.vpos.y += self.dpos.y * dt