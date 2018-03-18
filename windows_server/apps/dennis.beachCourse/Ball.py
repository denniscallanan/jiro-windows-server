import pyglet, math
import res, batch, group
from Camera import *
from Vector import *
from BallAirBounceEffect import *

class Ball(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}

    def __init__(self):

        pyglet.sprite.Sprite.__init__(self, res.IMG_BALL, batch=batch.main, group=group.balls)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.5
        self.vpos.y = 250
        self.rot = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.gravity = -30
        self.target_jump_power = 0
        self.allow_air_jump = False
        self.jumped = False
        self.ACCEL_SPEED = 80
        self.MAX_SPEED = 500
        #self.bounce_state = 0 # 0 = normal, 1 = squishing, 2 = expanding
        #self.HAV = 200 # static constant
        #self.absorbed_vel = 0

    def update_acceleration_x(self, x):
        if x > -0.5 and x < 0.5:
            x = 0
        self.acceleration_x = x

    def update(self, dt):
        #if self.bounce_state == 0: # normal
        self.update_state_normal(dt)
        '''elif self.bounce_state == 1: # squishing
            self.update_state_squishing(dt)
        elif self.bounce_state == 2: # expanding
            self.update_state_expanding(dt)'''

    def update_state_normal(self, dt):
        if self.velocity_y < 0:
            self.jumped = False
        self.velocity_x += self.acceleration_x * dt * self.ACCEL_SPEED
        self.velocity_x /= 1 + (0.5 * dt)
        self.velocity_y += self.gravity * dt
        if self.velocity_x > self.MAX_SPEED:
            self.velocity_x = self.MAX_SPEED
        elif self.velocity_x < -self.MAX_SPEED:
            self.velocity_x = -self.MAX_SPEED
        self.rot += self.velocity_x * dt
        self.rotation = self.rot - 30
        self.vpos.x += math.radians(self.velocity_x * dt) * self.vwidth()
        self.vpos.y += self.velocity_y
        
    def update_top_bounce(self, bounds):
        if self.vpos.y > bounds[1].y and self.velocity_y > 0:
            self.velocity_y /= -1.5

    def update_air_jumps(self, dt):
        #if not (self.allow_air_jump and self.jump(air=True)) and not self.jumped:
        if self.allow_air_jump:
            self.jump(air=True)
        #elif not self.jumped:
        #    self.velocity_y -= self.target_jump_power * dt * 2

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
            #if dir == -1 and self.attempt_jump > 0:
            #    if not self.velocity_y < 0 and ball_point.y >= platform.vpos.y - half_plat_size.y and ball_point.y <= platform.vpos.y + half_plat_size.y + 120:
            #        self.attempt_jump = 0
            if ball_point.y >= platform.vpos.y - half_plat_size.y and ball_point.y <= platform.vpos.y + half_plat_size.y: # y colliding
                self.vpos.y += (platform.vpos.y - dir * half_plat_size.y) - (ball_point.y)
                #self.bounce_state = 1 # squishing
                self.velocity_y /= -1.5#-1.2
                if dir == -1:
                    if not self.jump():
                        self.allow_air_jump = True
                return True
        return False

    def jump(self, air=False):
        if self.target_jump_power > 0:
            self.velocity_y = 0
            self.velocity_y = min(self.velocity_y + self.target_jump_power, self.target_jump_power)
            self.jumped = True
            self.allow_air_jump = False
            self.target_jump_power = 0
            if air:
                BallAirBounceEffect(self.vpos.x, self.vpos.y - 10)
            return True
        return False

    def wrap(self, bounds):
        vheight_div_2 = self.vheight() / 2
        if self.vpos.y <= bounds[0].y - vheight_div_2:
            #self.vpos.x -= 150
            self.vpos.y = bounds[1].y + vheight_div_2
            self.velocity_y /= 3
            
    def is_out_of_bounds(self, bounds):
        return self.vpos.x < bounds[0].x or self.vpos.y < bounds[0].y
        

    
