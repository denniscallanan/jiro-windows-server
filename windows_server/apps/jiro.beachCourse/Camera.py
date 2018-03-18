from Vector import *

class Camera:

    def __init__(self, w, h, fixedheight=False):
        self.window_size = Vector(w, h)
        self.pos = Vector(0, 0)
        if fixedheight:
            self.vw = 720.0 / h * w
        else:
            self.vw = 1280
        self.zoom = 1.0
        self.zoom_time = 3
        self.the_target_zoom = None
        self.pos_time_x = 3
        self.pos_time_y = 3
        self.the_target_pos = None

    def rc(self, c):  # real coordinate
        return (c / self.vw * self.window_size.x) * self.zoom

    def rx(self, x):
        return (self.rc(x - self.pos.x) + self.window_size.x / 2)

    def ry(self, y):
        return (self.rc(y - self.pos.y) + self.window_size.y / 2)

    def rs(self, s):  # real scale
        return self.rc(s)

    def get_width(self):
        return self.vw

    def get_height(self):
        return self.vw * self.window_size.y / self.window_size.x

    def get_bounds(self):
        width_div_2 = self.get_width() / 2
        height_div_2 = self.get_height() / 2
        return (Vector((-width_div_2 + self.pos.x) / self.zoom, (-height_div_2 + self.pos.y) / self.zoom), Vector((width_div_2 + self.pos.x) / self.zoom, (height_div_2 + self.pos.y) / self.zoom))

    def target_zoom(self, zoom, t=3):
        self.zoom_time = t
        self.the_target_zoom = zoom

    def target_pos(self, pos, tx=3, ty=3):
        self.pos_time_x = tx
        self.pos_time_y = ty
        self.the_target_pos = pos

    def update(self, dt):
        if self.the_target_zoom != None: self.zoom += (self.the_target_zoom - self.zoom) / self.zoom_time
        if self.the_target_pos != None:
            self.pos.x += (self.the_target_pos.x - self.pos.x) / (self.pos_time_x / dt)
            self.pos.y += (self.the_target_pos.y - self.pos.y) / (self.pos_time_y / dt)

class CameraRelativeSprite:

    def __init__(self):
        self.vscale = 1
        self.vpos = Vector(0, 0)

    def relative_to_cam(self, cam):
        self.scale = cam.rs(float(self.vscale))
        self.x = cam.rx(float(self.vpos.x))
        self.y = cam.ry(float(self.vpos.y))

    def vwidth(self):
        return self.image.width * self.vscale * self.scale_x

    def vheight(self):
        return self.image.height * self.vscale * self.scale_y
