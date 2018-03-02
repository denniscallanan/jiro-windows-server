import pyglet
import res, batch, math, random
from Camera import *
from Vector import *

class Poop(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}

    def __init__(self, x, y):
        pyglet.sprite.Sprite.__init__(self, res.IMG_POOP, batch=batch.poop)
        self.vpos = Vector(x, y)
        self.vscale = random.randint(5, 20) / 10.0
        #self.vanishSpeed = random.randint(7, 8) / 20.0
        self.timer = 200
        darkness = random.randint(155, 255)
        self.color = (darkness, darkness, darkness)

    def vanished(self, dt):
        self.timer -= dt * 60
        if self.timer < 0:
            self.opacity -= dt * 130
        return self.opacity <= 0

    def collidesWithPlayer(self, player):
        selfRad = self.vscale * 4 * 5
        playerRad = (player.width / 3) #player.vscale * (player.width / 3)
        return Vector(player.vpos.x - self.vpos.x, player.vpos.y - self.vpos.y).magnitude() <= playerRad + selfRad
