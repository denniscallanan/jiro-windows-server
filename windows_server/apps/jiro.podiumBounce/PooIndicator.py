import pyglet
import res, batch, math
from Camera import *
from Vector import *

class PooIndicator(pyglet.sprite.Sprite, CameraRelativeSprite):

    def __init__(self):
        pyglet.sprite.Sprite.__init__(self, res.IMG_REDCIRCLE, batch=batch.indicators)
        CameraRelativeSprite.__init__(self)
        self.opacity = 230

    def update(self, player):
        self.rotation = player.rotation
        player.vscale = 0.5 + player.pooSecondsLeft / 50.0
        self.vscale = player.vscale * player.pooSecondsLeft / 14

        x = math.cos(math.radians(-player.rot)) * 35 * player.vscale
        y = math.sin(math.radians(-player.rot)) * 35 * player.vscale

        self.vpos.x = player.vpos.x - x
        self.vpos.y = player.vpos.y - y
