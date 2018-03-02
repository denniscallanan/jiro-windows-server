import pyglet, datetime, random
import res, batch, math, constants
from Camera import *
from Vector import *
from Poop import *
from PooIndicator import *

class Player(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}

    def __init__(self):
        pyglet.sprite.Sprite.__init__(self, res.SHEET_SPIDER.images[5], batch=batch.main)
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
        self.pooSecondsLeft = 9
        self.pooIndicator = PooIndicator()

    def update(self, dt, cam):
        self.rotate(self.rotVelocity / 1.75 * dt * 60)
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
                self.velocity *= 7 / 4
                self.speedLimit = 7
                while pooDt >= constants.ONE_OVER_SIXTEY:
                    self.createPoo()
                    pooDt -= constants.ONE_OVER_SIXTEY
                    self.lastPooTime = self.lastPooTime + datetime.timedelta(0, constants.ONE_OVER_SIXTEY)
                self.pooSecondsLeft -= dt
            else:
                self.speedLimit = 4

    def createPoo(self):
        offset = random.randint(-10, 10)
        poop = Poop(self.vpos.x + offset, self.vpos.y + offset)
        Poop.instances[(poop.vpos.x, poop.vpos.y)] = poop

    def checkPoopCollisions(self, poop):
        self.pooSpeedScalar = 1
        if not self.scuttering or self.pooSecondsLeft <= 0:
            for p in poop:
                poo = poop[p]
                if poo.collidesWithPlayer(self):
                    val = 0.1 * poo.opacity / 255
                    self.pooSpeedScalar *= 1 - val

    def rotate(self, amount):
        self.rot += amount  # 1.5
        self.rotation = self.rot + 90

    def relative_to_cam(self, cam):
        CameraRelativeSprite.relative_to_cam(self, cam)
        self.pooIndicator.relative_to_cam(cam)
