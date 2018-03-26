import pyglet, math
import res, batch, group
from Camera import *
from Vector import *

class Bullet(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = []
    
    def __init__(self, x, y, dx, dy):

        pyglet.sprite.Sprite.__init__(self, res.IMG_BULLET, batch=batch.main, group=group.bullets)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.15
        self.r = self.vwidth() / 2
        self.vpos.x = x
        self.vpos.y = y
        self.speed = 400
        self.dpos = Vector(dx * self.speed, dy * self.speed)
        self.opacity = 50

        Bullet.instances.append(self)

    def update(self, dt):
        self.vpos += self.dpos * dt
        if self.opacity < 255:
            self.opacity = min(255, self.opacity + 1024 * dt)
        if self.vscale < 0.3:
            self.vscale = min(0.3, self.vscale + 1 * dt)

    def out_of_bounds(self, bounds):
        return self.vpos.x < bounds[0].x or self.vpos.x > bounds[1].x or self.vpos.y < bounds[0].y or self.vpos.y > bounds[1].y

    def check_collisions(self, enemies):
        for enemy in enemies:
            if math.sqrt((enemy.vpos.x - self.vpos.x) ** 2 + (enemy.vpos.y - self.vpos.y) ** 2) < self.r + enemy.r:
                diff1 = (enemy.vpos - self.vpos).normalized()
                #diff2 = (self.vpos - enemy.vpos).normalized()
                myforce = self.speed * self.r
                #itsforce = enemy.speed * enemy.r
                myappliedforce = (diff1 * myforce)
                #itsappliedforce = (diff2 * itsforce)
                enemy.dpos += myappliedforce / enemy.r
                #enemy.dpos -= itsappliedforce / enemy.r
                self.dpos -= myappliedforce / self.r
                #self.dpos += itsappliedforce / self.r