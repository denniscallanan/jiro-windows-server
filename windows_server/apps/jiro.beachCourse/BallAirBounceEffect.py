import pyglet, math
import res, batch, group
from Camera import *
from Vector import *

class BallAirBounceEffect(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}
    next_instance_id = 0

    def __init__(self, x, y):

        BallAirBounceEffect.instances[BallAirBounceEffect.next_instance_id] = self
        pyglet.sprite.Sprite.__init__(self, res.IMG_BALL_AIR_BOUNCE_EFFECT, batch=batch.main, group=group.bg_effects)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.5
        self.vpos.x = x
        self.vpos.y = y
        self.id = BallAirBounceEffect.next_instance_id

        BallAirBounceEffect.next_instance_id += 1

    def update(self, dt):
        self.opacity -= dt * 700
        self.vscale += dt * 1.7
        if self.opacity <= 0:
            self.opacity = 0
            self.delete()
            BallAirBounceEffect.instances[self.id] = None