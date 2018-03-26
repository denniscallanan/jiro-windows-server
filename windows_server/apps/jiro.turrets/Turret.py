import pyglet, math
import res, batch, group
from Camera import *
from Vector import *
from Bullet import *
from BigBullet import *
from Crosshair import *
from AmmoSprite import *

class Turret(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}

    def __init__(self, bounds):

        pyglet.sprite.Sprite.__init__(self, res.IMG_TURRET1, batch=batch.main, group=group.turrets)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.5
        self.vpos.y = bounds[0].y + 60
        self.rot = -90
        self.rot_velocity = 0
        self.shoot_end_time = 0
        self.shooting = 0 # 0 : False, 1 : Normal Shooting, 2 : Power Shooting
        self.ammo = 15
        self.max_ammo = 15

        self.crosshair = Crosshair(self.vpos.y + 20)
        self.ammosprite = AmmoSprite(self.vpos.x / 2 - self.vwidth() / 2, self.vpos.y - self.vscale * 55, self.width)
        self.ammosprite.vscale = self.vscale

    def update(self, dt):
        self.rot += self.rot_velocity * dt * 20
        self.rot = min(20, max(-200, self.rot))
        self.crosshair.update(self.rot + 90, dt)

    def shoot(self, dt):
        if self.shooting == 1:
            if self.shoot_end_time > 0:
                self.shoot_end_time -= dt
            else:
                if self.ammo >= 1:
                    self.spawn_bullet()
                    self.ammo -= 1
                    self.ammosprite.ammo(self.ammo / float(self.max_ammo))
                self.shoot_end_time += 0.06
        elif self.shooting == 0:
            self.shooting = -1

    def power_shoot(self):
        #self.shoot_end_time = 0.15
        if self.ammo >= 6:
            self.ammosprite.ammo(self.ammo / float(self.max_ammo))
            self.ammo -= 6
            self.spawn_big_bullet()

    def increase_ammo(self, dt):
        self.ammo = min(self.ammo + dt * 5, self.max_ammo)
        self.ammosprite.ammo(self.ammo / float(self.max_ammo))

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
        self.ammosprite.relative_to_cam(cam)

    def delete(self):
        pyglet.sprite.Sprite.delete(self)
        self.crosshair.delete()
        self.ammosprite.delete()
    
    @staticmethod
    def reposition_turrets():
        count = len(Turret.instances)
        if count > 0:
            spacing = 120
            pos = - (count-1) * spacing / 2
            for t in Turret.instances:
                turret = Turret.instances[t]
                turret.vpos.x = pos
                print turret.vwidth()
                turret.crosshair.vpos.x = pos
                turret.ammosprite.vpos.x = pos - turret.vwidth() / 2
                pos += spacing