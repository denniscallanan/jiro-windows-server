import pyglet
import res, batch, group
from Camera import *
from Vector import *

class BigBullet(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = []
    
    def __init__(self, x, y, dx, dy):

        pyglet.sprite.Sprite.__init__(self, res.IMG_BIG_BULLET, batch=batch.main, group=group.bullets)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.2
        self.vpos.x = x
        self.vpos.y = y
        self.dpos = Vector(dx, dy)
        self.speed = 600

        BigBullet.instances.append(self)

    def update(self, dt):
        self.vpos += self.dpos * dt * self.speed
        if self.vscale < 0.35:
            self.vscale = min(0.35, self.vscale + 1 * dt)

    def out_of_bounds(self, bounds):
        return self.vpos.x < bounds[0].x or self.vpos.x > bounds[1].x or self.vpos.y < bounds[0].y or self.vpos.y > bounds[1].y