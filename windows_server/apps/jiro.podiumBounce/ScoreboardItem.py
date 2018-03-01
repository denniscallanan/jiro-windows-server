import pyglet
import res, batch
from Vector import *

class ScoreboardItem(pyglet.sprite.Sprite):

    def __init__(self, name, y):
        pyglet.sprite.Sprite.__init__(self, res.IMG_COLOR_BLACK, batch=batch.overlay1)
        self.y = y
        self.scale_y = 30
        self.name = name
        self.score = 0
        self.nameLabel = pyglet.text.Label(name, font_name='Tahoma', y=self.y+8, font_size=12, batch=batch.overlay2, height=self.scale_y)
        self.scoreLabel = pyglet.text.Label("0", font_name='Tahoma', y=self.y+8, font_size=12, batch=batch.overlay2, height=self.scale_y, anchor_x="right", bold=True)
        #self.scale_x = 200 #self.nameLabel->retrieve:width

    def reposition(self, x, width):
        self.x = x
        self.scale_x = width
        self.nameLabel.x = x + 10
        self.scoreLabel.x = x + width - 10