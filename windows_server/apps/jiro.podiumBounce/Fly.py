import pyglet, random, math
import res, batch
from Vector import *
from Camera import *
from Angle import *

class Fly(pyglet.sprite.Sprite, CameraRelativeSprite):

    def __init__(self):
        pyglet.sprite.Sprite.__init__(self, res.IMG_FLY, batch=batch.poop)
        CameraRelativeSprite.__init__(self)
        self.initial_scale = 0.25
        self.vscale = self.initial_scale

    def random_pos(self, cam):
        self.vscale = self.initial_scale
        self.opacity = 255
        self.rotation = random.randint(0, 360)
        bounds = cam.get_bounds()
        width_div_2 = self.width / 2
        height_div_2 = self.height / 2
        self.vpos.x = float(random.randint(int(bounds[0].x) + width_div_2, int(bounds[1].x) - width_div_2))
        self.vpos.y = float(random.randint(int(bounds[0].y) + height_div_2, int(bounds[1].y) - height_div_2))

    def distanceFromPlayer(self, player):
        return Vector(player.vpos.x - self.vpos.x, player.vpos.y - self.vpos.y).magnitude()