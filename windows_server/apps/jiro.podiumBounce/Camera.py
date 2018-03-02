from Vector import *

class Camera:

    def __init__(self, w, h):
        self.window_size = Vector(w, h)
        self.pos = Vector(0, 0)
        self.vw = 1280
        self.zoom = 1.0

    def rc(self, c):  # real coordinate
        return (c / self.vw * self.window_size.x) * self.zoom

    def rx(self, x):
        return (self.rc(x) + self.window_size.x / 2) - self.pos.x

    def ry(self, y):
        return (self.rc(y) + self.window_size.y / 2) - self.pos.y

    def rs(self, s):  # real scale
        return self.rc(s)

    def get_width(self):
        return self.vw

    def get_height(self):
        return self.vw * self.window_size.y / self.window_size.x

    def get_bounds(self):
        width_div_2 = self.get_width() / 2
        height_div_2 = self.get_height() / 2
        return (Vector((-width_div_2 - self.pos.x) / self.zoom, (-height_div_2 - self.pos.y) / self.zoom), Vector((width_div_2 - self.pos.x) / self.zoom, (height_div_2 - self.pos.y) / self.zoom))

class CameraRelativeSprite:

    def __init__(self):
        self.vscale = 1
        self.vpos = Vector(0, 0)

    def relative_to_cam(self, cam):
        self.scale = cam.rs(self.vscale)
        self.x = cam.rx(self.vpos.x)
        self.y = cam.ry(self.vpos.y)
