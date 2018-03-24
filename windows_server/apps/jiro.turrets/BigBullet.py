import pyglet
import res, batch, group
from Camera import *
from Vector import *

class BigBullet(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = []
    
    def __init__(self, x, y, dx, dy):

        pyglet.sprite.Sprite.__init__(self, res.IMG_BIG_BULLET, batch=batch.main, group=group.bullets)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.25
        self.vpos.x = x
        self.vpos.y = y
        self.dpos = Vector(dx, dy)
        self.speed = 400

        BigBullet.instances.append(self)

    def update(self, dt):
        self.vpos += self.dpos * dt * self.speed
        if self.vscale < 0.4:
            self.vscale = min(0.4, self.vscale + 1 * dt)