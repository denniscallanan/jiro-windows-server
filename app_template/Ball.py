import pyglet
import res, batch, group
from Camera import *
from Vector import *

class Ball(pyglet.sprite.Sprite, CameraRelativeSprite):

    instances = {}

    def __init__(self):

        pyglet.sprite.Sprite.__init__(self, res.IMG_BALL, batch=batch.main, group=group.balls)
        CameraRelativeSprite.__init__(self)
        self.vscale = 0.5

        

    
