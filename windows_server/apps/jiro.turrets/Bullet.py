import pyglet
import res, batch, group
from Camera import *
from Vector import *

class Bullet(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = []
    
    def __init__(self, x, y, dx, dy):

        pyglet.sprite.Sprite.__init__(self, res.IMG_BULLET, batch=batch.main, group=group.bullets)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.2
        self.vpos.x = x
        self.vpos.y = y
        self.dpos = Vector(dx, dy)
        self.speed = 250
        self.opacity = 50

        Bullet.instances.append(self)

    def update(self, dt):
        self.vpos += self.dpos * dt * self.speed
        if self.opacity < 255:
            self.opacity = min(255, self.opacity + 1024 * dt)
        if self.vscale < 0.5:
            self.vscale = min(0.5, self.vscale + 1 * dt)