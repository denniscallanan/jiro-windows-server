import pyglet

IMG_BALL = pyglet.image.load("res/ball.png")
IMG_BALL.anchor_x = IMG_BALL.width / 2
IMG_BALL.anchor_y = IMG_BALL.height / 2

IMG_PLATFORM = pyglet.image.load("res/platform.png")
IMG_PLATFORM.anchor_x = IMG_PLATFORM.width / 2
IMG_PLATFORM.anchor_y = IMG_PLATFORM.height / 2

IMG_BALL_AIR_BOUNCE_EFFECT = pyglet.image.load("res/ball_air_bounce_effect.png")
IMG_BALL_AIR_BOUNCE_EFFECT.anchor_x = IMG_BALL_AIR_BOUNCE_EFFECT.width / 2
IMG_BALL_AIR_BOUNCE_EFFECT.anchor_y = IMG_BALL_AIR_BOUNCE_EFFECT.height / 2