import pyglet
from SpriteSheet import *

SHEET_SPIDER = SpriteSheet("res/spider")

IMG_BG = pyglet.image.load("res/bg.jpg")
IMG_POOP = pyglet.image.load("res/poop.png")
IMG_REDCIRCLE = pyglet.image.load("res/redcircle.png")
IMG_REDCIRCLE.anchor_x = IMG_REDCIRCLE.width / 2
IMG_REDCIRCLE.anchor_y = IMG_REDCIRCLE.height / 2

SPR_BG = pyglet.sprite.Sprite(IMG_BG)
SPR_BG.opacity = 100
