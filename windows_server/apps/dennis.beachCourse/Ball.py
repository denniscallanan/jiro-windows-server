import pyglet, math
import res, batch, group
from Camera import *
from Vector import *

class Ball(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}

    def __init__(self):

        pyglet.sprite.Sprite.__init__(self, res.IMG_BALL, batch=batch.main, group=group.balls)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.5
        self.rot = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.gravity = 0.5

    def update_acceleration_x(self, x):
        if x > -0.5 and x < 0.5:
            x = 0
        self.acceleration_x = x

    def update(self, dt):
        self.velocity_x += self.acceleration_x * dt * 40
        self.velocity_y -= self.gravity
        self.velocity_x /= 1 + (0.5 * dt)
        if self.velocity_x > 300:
            self.velocity_x = 300
        elif self.velocity_x < -300:
            self.velocity_x = -300
        self.rot += self.velocity_x * dt
        self.rotation = self.rot - 30
        self.vpos.x += math.radians(self.velocity_x * dt) * self.vwidth()
        self.vpos.y += self.velocity_y

    def check_platform_collisions(self, platforms):
        for platform in platforms:
            if self.check_platform_collision(platform):
                return True
        return False

    def check_platform_collision(self, platform):
        half_plat_width = platform.vwidth() / 2
        half_plat_height = platform.vheight() / 2
        ball_point_y = self.vpos.y - self.vheight() / 2
        if self.vpos.x >= platform.vpos.x - half_plat_width and self.vpos.x <= platform.vpos.x + half_plat_width: # x colliding
            if ball_point_y >= platform.vpos.y - half_plat_height and ball_point_y <= platform.vpos.y + half_plat_height: # y colliding
                self.vpos.y += (platform.vpos.y + half_plat_height) - (ball_point_y)
                self.velocity_y /= -1.2
                return True
        return False

    def jump(self, power):
        self.velocity_y += power

        

    
