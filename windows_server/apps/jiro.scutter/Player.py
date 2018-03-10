import pyglet, datetime, random, math
import res, batch, group, constants
from Camera import *
from Vector import *
from Poop import *
from PooIndicator import *
from Angle import *

class Player(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}
    color_tints = {
        "color_black": (0, 0, 0),
        "color_red": (237, 28, 36),
        "color_green": (34, 177, 76),
        "color_blue": (63, 72, 204),
        "color_yellow": (255, 242, 0),
        "color_purple": (163, 73, 164),
        "color_aqua": (0, 162, 232),
        "color_orange": (255, 171, 15)
    }

    def __init__(self):
        pyglet.sprite.Sprite.__init__(self, res.SHEET_SPIDER.images[5], batch=batch.main, group=group.spiders)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.5
        self.animationIndex = 5
        self.vpos = Vector(0, 0)
        self.velocity = Vector(0, 0)
        self.rot = 0
        self.rotVelocity = 0
        self.acceleration = 0.75
        self.deceleration = 1.05
        self.speedLimit = 4
        self.moving = False
        self.scuttering = False
        self.pooSpeedScalar = 1
        self.currentSpeedLimit = self.speedLimit
        self.pooSecondsLeft = 3
        self.pooIndicator = PooIndicator()
        self.collidingWithFly = False
        self.facingFlyRotAim = None

    def update(self, dt, cam):
        if self.collidingWithFly:
            pass
        else:
            self.rotate(self.rotVelocity / 1.85 * dt * 60)
        self.updateAnimation(dt)
        self.updatePoo(dt)
        self.currentSpeedLimit = self.speedLimit * self.pooSpeedScalar
        self.updateMovement(dt)
        self.wrapPlayer(cam)
        self.pooIndicator.update(self)

    def updateAnimation(self, dt):
        lastAnimationIndex = int(round(self.animationIndex))

        if self.moving:
            self.animationIndex += 1 * dt * 60
        else:
            self.animationIndex = 5

        roundedAnimationIndex = int(round(self.animationIndex))
        if roundedAnimationIndex != lastAnimationIndex:
            res.SHEET_SPIDER.updateIndex(self, roundedAnimationIndex)

    def updateMovement(self, dt):
        if self.moving:
            self.velocity.x += self.acceleration * math.cos(math.radians(-self.rot)) * dt * 60
            self.velocity.y += self.acceleration * math.sin(math.radians(-self.rot)) * dt * 60
            if self.velocity.magnitude() > self.currentSpeedLimit:  # 8
                self.velocity = self.velocity.normalized() * self.currentSpeedLimit  # 8
        else:
            self.velocity.x /= self.deceleration * dt * 60
            self.velocity.y /= self.deceleration * dt * 60

        self.vpos.x += self.velocity.x * dt * 60
        self.vpos.y += self.velocity.y * dt * 60

    def wrapPlayer(self, cam):
        bounds = cam.get_bounds()

        if self.vpos.x > bounds[1].x + self.width / 2 + 1:
            self.vpos.x = bounds[0].x - self.width / 2

        elif self.vpos.x < bounds[0].x - self.width / 2 - 1:
            self.vpos.x = bounds[1].x + self.width / 2

        if self.vpos.y > bounds[1].y + self.height / 2 + 1:
            self.vpos.y = bounds[0].y - self.height / 2

        elif self.vpos.y < bounds[0].y - self.height / 2 - 1:
            self.vpos.y = bounds[1].y + self.height / 2

    def updatePoo(self, dt):
        if self.moving:
            if self.scuttering and self.pooSecondsLeft > 0:
                thisPooTime = datetime.datetime.now()
                pooDt = (thisPooTime - self.lastPooTime).total_seconds()
                self.velocity *= 5.8 / 4.4
                self.speedLimit = 5.8
                while pooDt >= constants.ONE_OVER_SIXTEY:
                    self.createPoo()
                    pooDt -= constants.ONE_OVER_SIXTEY
                    self.lastPooTime = self.lastPooTime + datetime.timedelta(0, constants.ONE_OVER_SIXTEY)
                self.pooSecondsLeft -= dt
            else:
                self.speedLimit = 4.4

    def createPoo(self):
        offset = random.randint(-10, 10)
        poop = Poop(self.vpos.x + offset, self.vpos.y + offset)
        Poop.instances[(poop.vpos.x, poop.vpos.y)] = poop

    def rotate(self, amount):
        self.rot += amount  # 1.5
        self.rotation = self.rot + 90

    def set_rot(self, value):
        self.rot = value
        self.rotation = self.rot + 90

    # Collision Checking

    def checkPoopCollisions(self, poop):
        self.pooSpeedScalar = 1
        if not self.scuttering or self.pooSecondsLeft <= 0:
            for p in poop:
                poo = poop[p]
                if poo.collidesWithPlayer(self):
                    val = 0.1 * poo.opacity / 255
                    self.pooSpeedScalar *= 1 - val

    def checkFlyCollision(self, fly, dt):
        dist = fly.distanceFromPlayer(self)
        required_dist = 80
        if self.collidingWithFly or dist < required_dist:
            if fly.vscale <= fly.initial_scale / 1.7:
                self.collidingWithFly = False
                self.facingFlyRotAim = None
                self.pooSecondsLeft = min(self.pooSecondsLeft + 1.5, 4.5)
                return True
            else:
                if not self.collidingWithFly:
                    self.collidingWithFly = True
                    self.facingFlyRotAim = Angle.constrain(Angle.facing(self.vpos, fly.vpos, Angle.DEGREES) - 90)
                    #audio_batch.flyEat.playSound(res.AUD_POP)
                x = math.cos(math.radians(-self.rot)) * 35 * self.vscale
                y = math.sin(math.radians(-self.rot)) * 35 * self.vscale
                position_aim = Vector(self.vpos.x + x, self.vpos.y + y)
                fly.vpos += (position_aim - fly.vpos).normalized() * (dt * 200)
                fly.opacity = 255 - (required_dist - dist)
                fly.vscale -= dt / 3
                #aim = self.vpos.rotationFacing(fly.vpos, math.degrees) - 90
                #diffa = aim - self.rotation
                #diffb = diffa - 360
                #diffb = diffb + 720 if diffb < -360 else diffb
                #diff = diffa if abs(diffa) < abs(diffb) else diffb
                #self.rotate(diff / 8)
                self.set_rot((Angle.constrain(self.rot) * 3 + self.facingFlyRotAim) / 4)
        return False

    # Overrided function

    def relative_to_cam(self, cam):
        CameraRelativeSprite.relative_to_cam(self, cam)
        self.pooIndicator.relative_to_cam(cam)
