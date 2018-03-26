import pyglet
import res, batch, group
from Camera import *
from Vector import *

class Astroid(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = []

    def __init__(self, pos, r, speed, rot, img):

        pyglet.sprite.Sprite.__init__(self, img, batch=batch.main, group=group.bullets)
        CameraRelativeSprite.__init__(self)

        self.r = r
        self.vpos = pos
        self.vpos.y += self.r
        self.speed = speed
        self.dpos = Vector(math.cos(math.radians(rot)) * speed, math.sin(math.radians(rot)) * speed)
        self.vscale = float(r * 2) / img.width

        Astroid.instances.append(self)

    def update(self, dt):
        self.vpos.x += self.dpos.x * dt
        self.vpos.y += self.dpos.y * dt