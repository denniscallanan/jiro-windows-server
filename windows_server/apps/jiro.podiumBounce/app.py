import jgsapi, pyglet, random, math, os

queue = []

spider_images = []

##################################
# JIRO API CODE
##################################

# Functions

def onPlayerJoin(addr):
    print jgsapi.pretty_ip(addr),"joined app"
    jiro.switchController("main", addr)
    queue.append({"type": "createPlayer", "addr": addr})

def onPlayerLeave(addr):
    print jgsapi.pretty_ip(addr),"left app"
    players.pop(addr, None)

def cleanup():
    window.close()
    pyglet.app.exit()
    print "Podium Bounce server stopped!"

def tapMoveStart(event):
    player = players.get(event.addr, None)
    if player != None:
        player.moving = True

def tapMoveEnd(event):
    player = players.get(event.addr, None)
    if player != None:
        player.moving = False

def accelerometerEvent(event):
    player = players.get(event.addr, None)
    if player != None:
        player.rotationVelocity = event.y


# CLASSES ########

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

##################

# Create game server
jiro = jgsapi.GameServer()
jiro.importController("controllers/main.xml")

# Server events
jiro.onPlayerJoin = onPlayerJoin
jiro.onPlayerLeave = onPlayerLeave
jiro.cleanup = cleanup

# Main controller events
controller = jiro.getController("main")
controller.addEventListener("accelerometer", accelerometerEvent)

moveButton = controller.getInteractable("move")
moveButton.addEventListener("tapStart", tapMoveStart)
moveButton.addEventListener("tapEnd", tapMoveEnd)

##################################
# MAIN PROGRAM CODE
##################################

players = {}
sprite_batch = pyglet.graphics.Batch()

class Player(pyglet.sprite.Sprite):
    def __init__(self):
        self.animationIndex = 0
        super(Player, self).__init__(spider_images[self.animationIndex], batch=sprite_batch)
        self.x = random.randint(50, window.width - 50)
        self.y = random.randint(50, window.height - 100)
        self.velocity = Vector(0,0)
        self.scale = 3 / 40.0
        self.angle = 0
        self.moving = False
        self.rotationVelocity = 0
    def update(self):
        self.incrementAngle(self.rotationVelocity)
        if self.moving:
            self.velocity.x += 0.75 * math.cos(math.radians(-self.angle))
            self.velocity.y += 0.75 * math.sin(math.radians(-self.angle))
            if self.velocity.magnitude() > 8:
                self.velocity = self.velocity.normalized() * 8
        else:
            self.velocity.x /= 1.05
            self.velocity.y /= 1.05

        self.x += self.velocity.x
        self.y += self.velocity.y 

        if self.x > window.width:
            self.x = 0

        if self.y > window.height:
            self.y = 0

        
    def incrementAngle(self, amount):
        self.angle += amount / 1.5
        self.rotation = self.angle + 90


window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(1, 1, 1, 1)


for filename in os.listdir('res/spider'):

    IMG_SPIDER = pyglet.image.load('res/spider/'+filename)
    IMG_SPIDER.anchor_x = 785
    IMG_SPIDER.anchor_y = 439

    spider_images.append(IMG_SPIDER)



@window.event
def on_draw():
    window.clear()
    sprite_batch.draw()

def update(dt):
    while len(queue) != 0:
        action = queue.pop(0)
        if action["type"] == "createPlayer":
            players[action["addr"]] = Player()
    for p in players:
        players[p].update()

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
