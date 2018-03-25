import pyglet, math
import res, batch, group
from Camera import *
from Vector import *
from Bullet import *
from BigBullet import *
from Crosshair import *

class Turret(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}

    def __init__(self, bounds):

        pyglet.sprite.Sprite.__init__(self, res.IMG_TURRET1, batch=batch.main, group=group.turrets)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.4
        self.vpos.y = bounds[0].y + 40
        self.rot = -90
        self.rot_velocity = 0
        self.shoot_end_time = 0
        self.shooting = 0 # 0 : False, 1 : Normal Shooting, 2 : Power Shooting
        self.ammo = 15

        self.crosshair = Crosshair(self.vpos.y + 20)

    def update(self, dt):
        self.rot += self.rot_velocity * dt * 10
        self.rot = min(20, max(-200, self.rot))
        self.crosshair.update(self.rot + 90, dt)

    def shoot(self, dt):
        if self.shooting == 1:
            if self.shoot_end_time > 0:
                self.shoot_end_time -= dt
            else:
                self.spawn_bullet()
                self.shoot_end_time += 0.06
        elif self.shooting == 0:
            self.shooting = -1

    def power_shoot(self):
        #self.shoot_end_time = 0.15
        self.spawn_big_bullet()

    def increase_ammo(self):
        self.ammo = min(self.ammo + 1, 15)

    def spawn_bullet(self):
        dx = math.cos(math.radians(self.rot))
        dy = -math.sin(math.radians(self.rot))
        Bullet(self.vpos.x, self.vpos.y + 20, dx, dy)

    def spawn_big_bullet(self):
        dx = math.cos(math.radians(self.rot))
        dy = -math.sin(math.radians(self.rot))
        BigBullet(self.vpos.x, self.vpos.y + 20, dx, dy)

    def relative_to_cam(self, cam):
        CameraRelativeSprite.relative_to_cam(self, cam)
        self.crosshair.relative_to_cam(cam)

    def delete(self):
        pyglet.sprite.Sprite.delete(self)
        self.crosshair.delete()