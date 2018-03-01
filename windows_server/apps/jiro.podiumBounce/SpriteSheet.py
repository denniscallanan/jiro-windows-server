import pyglet, os
from Camera import *

class SpriteSheet:

    def __init__(self, dir, ext=".png"):
        files = os.listdir(dir)
        self.dir = dir
        self.images = []

        for fn in files:
            if fn.endswith(ext):
                img = pyglet.image.load('res/spider/' + fn)
                #tex.anchor_x = 785
                #tex.anchor_y = 439
                img.anchor_x = img.width / 2
                img.anchor_y = img.height / 2
                self.images.append(img)

        self.count = len(self.images)

    def updateIndex(self, spr, i):
        i = i % self.count
        spr.image = self.images[i]
