import pyglet
from SpriteSheet import *

# SPRITE SHEETS

SHEET_SPIDER = SpriteSheet("res/spider")

# IMAGES

IMG_BG = pyglet.image.load("res/bg.jpg")
IMG_POOP = pyglet.image.load("res/poop.png")
IMG_FLY = pyglet.image.load("res/fly.png")
IMG_FLY.anchor_x = IMG_FLY.width / 2
IMG_FLY.anchor_y = IMG_FLY.height / 2
IMG_REDCIRCLE = pyglet.image.load("res/redcircle.png")
IMG_REDCIRCLE.anchor_x = IMG_REDCIRCLE.width / 2
IMG_REDCIRCLE.anchor_y = IMG_REDCIRCLE.height / 2
IMG_COLOR_BLACK = pyglet.image.load("res/color_black_100.png")

# SPRITES

SPR_BG = pyglet.sprite.Sprite(IMG_BG)
SPR_BG.opacity = 100

# AUDIO

#AUD_POP = pyglet.resource.media("res/audio/pop.mp3")