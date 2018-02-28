import jgsapi, pyglet, random, math, os, sys

queue = []

#######################################
# CLASSES
#######################################

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def magnitude(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def normalized(self):
        mag = self.magnitude()
        return Vector(self.x / mag, self.y / mag)

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

class Poop(pyglet.sprite.Sprite):

    def __init__(self, x, y):
        super(Poop, self).__init__(IMG_POOP, batch=poop_batch)
        self.x = x
        self.y = y
        self.scale = random.randint(5, 20) / 10.0
        #self.vanishSpeed = random.randint(7, 8) / 20.0
        self.timer = 250
        darkness = random.randint(155, 255)
        self.color = (darkness, darkness, darkness)

    def vanished(self):
        self.timer -= 1
        if self.timer < 0:
            self.opacity -= 2
        return self.opacity <= 0

    def checkCollisionWithPlayer(self, player):
        selfRad = self.scale * 4 * 5
        playerRad = player.scale * (player.width / 3)
        return Vector(player.x - self.x, player.y - self.y).magnitude() <= playerRad + selfRad

class Player(pyglet.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__(SHEET_SPIDER.images[5], batch=sprite_batch)
        self.scale = 0.5
        self.animationIndex = 5
        self.x = random.randint(50, window.width - 50)
        self.y = random.randint(50, window.height - 100)
        self.velocity = Vector(0, 0)
        self.rot = 0
        self.rotVelocity = 0
        self.acceleration = 0.75
        self.deceleration = 1.05
        self.speedLimit = 4
        self.moving = False
        self.scuttering = False
        self.pooSpeedScalar = 1
        self.currentSpeedLimit = self.speedLimit
        self.pooSecondsLeft = 9
        self.pooCircle = pyglet.sprite.Sprite(IMG_REDCIRCLE, batch=circle_batch)
        self.pooCircle.opacity = 230

    def update(self, dt):
        self.rotate(self.rotVelocity)
        self.updateAnimation()
        self.updatePoo(dt)
        self.currentSpeedLimit = self.speedLimit * self.pooSpeedScalar
        self.updateMovement()
        self.wrapPlayer()
        self.updatePooCircle()

    def updateAnimation(self):
        lastAnimationIndex = self.animationIndex

        if self.moving:
            self.animationIndex += 1
        else:
            self.animationIndex = 5

        if self.animationIndex != lastAnimationIndex:
            SHEET_SPIDER.updateIndex(self, self.animationIndex)

    def updateMovement(self):
        if self.moving:
            self.animationIndex += 1
            self.velocity.x += self.acceleration * math.cos(math.radians(-self.rot))
            self.velocity.y += self.acceleration * math.sin(math.radians(-self.rot))
            if self.velocity.magnitude() > self.currentSpeedLimit:  # 8
                self.velocity = self.velocity.normalized() * self.currentSpeedLimit # 8
        else:
            self.animationIndex = 5
            self.velocity.x /= self.deceleration
            self.velocity.y /= self.deceleration

        self.x += self.velocity.x
        self.y += self.velocity.y

    def wrapPlayer(self):
        if self.x > window.width + self.width / 2 + 1:
            self.x = -self.width / 2

        if self.x < -self.width / 2 - 1:
            self.x = window.width + self.width / 2

        if self.y > window.height + self.height / 2 + 1:
            self.y = -self.height / 2

        if self.y < -self.height / 2 - 1:
            self.y = window.height + self.height / 2

    def updatePoo(self, dt):
        if self.moving:
            if self.scuttering and self.pooSecondsLeft > 0:
                self.velocity *= 7 / 4
                self.speedLimit = 7
                offset = random.randint(-10, 10)
                poop = Poop(self.x + offset, self.y + offset)
                poops[(poop.x, poop.y)] = poop
                self.pooSecondsLeft -= dt
            else:
                self.speedLimit = 4

    def updatePooCircle(self):
        self.pooCircle.rotation = self.rotation
        self.pooCircle.scale = self.scale * self.pooSecondsLeft / 14
        self.scale = 0.5 + self.pooSecondsLeft / 50.0

        x = math.cos(math.radians(-self.rot)) * 35 * self.scale
        y = math.sin(math.radians(-self.rot)) * 35 * self.scale

        self.pooCircle.x = self.x - x
        self.pooCircle.y = self.y - y

    def rotate(self, amount):
        self.rot += amount / 1.75  # 1.5
        self.rotation = self.rot + 90

#######################################
# JIRO CODE
#######################################

# Create Game Server

jiro = jgsapi.GameServer()
jiro.importController("controllers/spider.xml")

# Server Events

@jiro.event
def on_player_join(addr):
    print jgsapi.pretty_ip(addr), "joined app"
    jiro.switchController("spider", addr)
    queue.append({"type": "createPlayer", "addr": addr})

@jiro.event
def on_player_leave(addr):
    print jgsapi.pretty_ip(addr), "left app"
    players.pop(addr, None)

@jiro.event
def cleanup():
    window.close()
    pyglet.app.exit()
    print "Podium Bounce server stopped!"
    sys.exit(0)

# Spider Controller Events

spider_controller = jiro.getController("spider")
btn_move = spider_controller.getInteractable("move")
btn_poo = spider_controller.getInteractable("poo")
    
@spider_controller.event
def accelerometer(event):
    player = players.get(event.addr, None)
    if player != None:
        player.rotVelocity = event.y

@btn_move.event
def tapStart(event):
    player = players.get(event.addr, None)
    if player != None:
        player.moving = True

@btn_move.event
def tapEnd(event):
    player = players.get(event.addr, None)
    if player != None:
        player.moving = False

@btn_poo.event
def tapStart(event):
    player = players.get(event.addr, None)
    if player != None:
        player.scuttering = True

@btn_poo.event
def tapEnd(event):
    player = players.get(event.addr, None)
    if player != None:
        player.scuttering = False

##################################
# MAIN PROGRAM CODE
##################################

players = {}
poops = {}
poop_batch = pyglet.graphics.Batch()
sprite_batch = pyglet.graphics.Batch()
circle_batch = pyglet.graphics.Batch()

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(1, 1, 1, 1)

SHEET_SPIDER = SpriteSheet("res/spider")

IMG_BG = pyglet.image.load("res/bg.jpg")
IMG_POOP = pyglet.image.load("res/poop.png")
IMG_REDCIRCLE = pyglet.image.load("res/redcircle.png")
IMG_REDCIRCLE.anchor_x = IMG_REDCIRCLE.width / 2
IMG_REDCIRCLE.anchor_y = IMG_REDCIRCLE.height / 2

SPR_BG = pyglet.sprite.Sprite(IMG_BG)
SPR_BG.opacity = 100

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    SPR_BG.draw()
    poop_batch.draw()
    sprite_batch.draw()
    circle_batch.draw()
    #label.draw()

def update(dt):
    #p = next(players.iterkeys(), None)
    #if p != None:
    #    label.text = jiro.getPlayerName(p)
    while len(queue) != 0:
        action = queue.pop(0)
        if action["type"] == "createPlayer":
            players[action["addr"]] = Player()
    for addr in players:
        player = players[addr]
        player.pooSpeedScalar = 1
        if not player.scuttering:
            for tup in poops:
                poo = poops[tup]
                if poo.checkCollisionWithPlayer(player):
                    val = 0.1 * poo.opacity / 255
                    player.pooSpeedScalar *= 1 - val

    for p in players:
        players[p].update(dt)
    to_delete = []
    for p in poops:
        if poops[p].vanished():
            to_delete.append(p)
    for p in to_delete:
        poops.pop(p, None)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
