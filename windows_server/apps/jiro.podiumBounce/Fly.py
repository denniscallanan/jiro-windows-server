import pyglet, random, math
import res, batch
from Vector import *
from Camera import *

class Fly(pyglet.sprite.Sprite, CameraRelativeSprite):

    def __init__(self):
        pyglet.sprite.Sprite.__init__(self, res.IMG_FLY, batch=batch.poop)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.3

    def random_pos(self, cam):
        self.vscale = 0.3
        self.opacity = 255
        bounds = cam.get_bounds()
        width_div_2 = self.width / 2
        height_div_2 = self.height / 2
        self.vpos.x = float(random.randint(int(bounds[0].x) + width_div_2, int(bounds[1].x) - width_div_2))
        self.vpos.y = float(random.randint(int(bounds[0].y) + height_div_2, int(bounds[1].y) - height_div_2))

    def update_rot(self, nearest_player):
        diff = nearest_player.vpos - self.vpos
        if   diff.x >= 0 and diff.y >= 0: additional = 0
        elif diff.x >= 0 and diff.y <  0: additional = 180
        elif diff.x <  0 and diff.y <  0: additional = 180
        elif diff.x <  0 and diff.y >= 0: additional = 0
        self.rotation = math.degrees(math.atan(diff.x / float(diff.y))) + additional

    def distanceFromPlayer(self, player):
        return Vector(player.vpos.x - self.vpos.x, player.vpos.y - self.vpos.y).magnitude()