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
        self.gravity = -30
        self.attempt_jump = 0
        self.bounce_state = 0 # 0 = normal, 1 = squishing, 2 = expanding
        self.HAV = 200 # static constant
        self.absorbed_vel = 0

    def update_acceleration_x(self, x):
        if x > -0.5 and x < 0.5:
            x = 0
        self.acceleration_x = x

    def update(self, dt):
        if self.bounce_state == 0: # normal
            self.update_state_normal(dt)
        '''elif self.bounce_state == 1: # squishing
            self.update_state_squishing(dt)
        elif self.bounce_state == 2: # expanding
            self.update_state_expanding(dt)'''

    def update_state_normal(self, dt):
        self.velocity_x += self.acceleration_x * dt * 40
        self.velocity_y += self.gravity * dt
        self.velocity_x /= 1 + (0.5 * dt)
        if self.velocity_x > 300:
            self.velocity_x = 300
        elif self.velocity_x < -300:
            self.velocity_x = -300
        self.rot += self.velocity_x * dt
        self.rotation = self.rot - 30
        self.vpos.x += math.radians(self.velocity_x * dt) * self.vwidth()
        self.vpos.y += self.velocity_y

    '''def update_state_squishing(self, dt):
        print self.velocity_y
        acceleration_y = -self.gravity * dt
        self.velocity_y += acceleration_y
        self.absorbed_vel += 0.8 * acceleration_y
        self.scale_y = self.HAV / (self.HAV + self.absorbed_vel)
        if self.velocity_y >= 0:
            self.velocity_y = 0
            self.bounce_state = 2 # expanding
    
    def update_state_expanding(self, dt):
        change = -self.gravity * dt
        self.absorbed_vel -= change
        self.velocity_y += change
        self.scale_y = self.HAV / (self.HAV + self.absorbed_vel)
        if self.absorbed_vel <= 0:
            self.absorbed_vel = 0
            self.bounce_state = 0 # normal'''

    def check_platform_collisions(self, platforms):
        for platform in platforms:
            if self.check_platform_collision(platform):
                return True
        return False

    def check_platform_collision(self, platform):
        half_plat_size = Vector(platform.vwidth() / 2, platform.vheight() / 2)
        if self.check_platform_collision_top(platform, half_plat_size): return True
        if self.check_platform_collision_bottom(platform, half_plat_size): return True
        return False

    def check_platform_collision_top(self, platform, half_plat_size):
        return self.check_platform_segment_collision(Vector(self.vpos.x, self.vpos.y - self.vheight() / 2), platform, -1, half_plat_size)

    def check_platform_collision_bottom(self, platform, half_plat_size):
        return self.check_platform_segment_collision(Vector(self.vpos.x, self.vpos.y + self.vheight() / 2), platform, 1, half_plat_size)

    def check_platform_segment_collision(self, ball_point, platform, dir, half_plat_size):
        if ball_point.x >= platform.vpos.x - half_plat_size.x and ball_point.x <= platform.vpos.x + half_plat_size.x: # x colliding
            if dir == -1 and self.attempt_jump > 0:
                if not self.velocity_y < 0 and ball_point.y >= platform.vpos.y - half_plat_size.y and ball_point.y <= platform.vpos.y + half_plat_size.y + 120:
                    self.attempt_jump = 0
            if ball_point.y >= platform.vpos.y - half_plat_size.y and ball_point.y <= platform.vpos.y + half_plat_size.y: # y colliding
                self.vpos.y += (platform.vpos.y - dir * half_plat_size.y) - (ball_point.y)
                #self.bounce_state = 1 # squishing
                self.velocity_y /= -1.2
                self.update_jump()
                return True
        return False

    def jump(self, power):
        self.attempt_jump = power

    def update_jump(self):
        if self.attempt_jump > 0:
            self.velocity_y += self.attempt_jump
            if self.velocity_y > self.attempt_jump:
                self.velocity_y = self.attempt_jump
            self.attempt_jump = 0

        

    
