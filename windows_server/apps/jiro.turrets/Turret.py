import pyglet
import res, batch, group
from Camera import *
from Vector import *

class Turret(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}

    def __init__(self, bounds):

        pyglet.sprite.Sprite.__init__(self, res.IMG_TURRET, batch=batch.main, group=group.turrets)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.4
        self.vpos.y = bounds[0].y
        self.rot = -90
        self.rot_velocity = 0
        #self.target_rot = -90
        self.shoot_end_time = 0
        self.next_turret_image = {"value": res.IMG_TURRET_FL}
        self.next_turret_image["next"] = {"value": res.IMG_TURRET_FR, "next": self.next_turret_image}
        self.shooting = 0 # 0 : False, 1 : Normal Shooting, 2 : Power Shooting
        self.ammo = 15

    def update(self, dt):
        #self.rot += (self.target_rot - self.rot) * dt * 1.5
        self.rot += self.rot_velocity * dt * 10
        self.rotation = self.rot + 90

    def shoot(self, dt):
        if self.shooting == 1:
            if self.shoot_end_time > 0:
                self.shoot_end_time -= dt
            else:
                self.image = self.next_turret_image["value"]
                self.next_turret_image = self.next_turret_image["next"]
                self.shoot_end_time += 0.1
        elif self.shooting == 2:
            self.shoot_end_time -= dt
            if self.shoot_end_time <= 0:
                self.shooting = 0
                self.image = res.IMG_TURRET
        elif self.shooting == 0:
            self.shooting = -1
            self.image = res.IMG_TURRET

    def power_shoot(self):
        self.shooting = 2
        self.shoot_end_time = 0.15
        return res.IMG_TURRET_FP

    def increase_ammo(self):
        self.ammo = min(self.ammo + 1, 15)