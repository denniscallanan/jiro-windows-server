import jgsapi, pyglet, random, math

queue = []

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
        player.phoneAngle = event.y

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
        self.texture = IMG_BALL
        super(Player, self).__init__(self.texture, batch=sprite_batch)
        self.x = random.randint(50, window.width - 50)
        self.y = random.randint(50, window.height - 100)
        self.scale = random.randint(3, 7) / 80.0
        self.fx = 0
        self.fy = 0
        self.angle = 0
        self.moving = False
        self.phoneAngle = 0
    def update(self):
        self.incrementAngle(self.phoneAngle)
        self.calcForce()
        if self.moving:
            self.x += self.fx
            self.y += self.fy
    def calcForce(self):
        self.fx = 3 * math.cos(math.radians(-self.angle))
        self.fy = 3 * math.sin(math.radians(-self.angle))
    def incrementAngle(self, amount):
        self.angle += amount / 4
        self.rotation = self.angle + 90

print "Welcome to Podium Bounce!"

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()
pyglet.gl.glClearColor(1, 1, 1, 1)

IMG_BALL = pyglet.image.load('res/spider.png')
IMG_BALL.anchor_x = 785
IMG_BALL.anchor_y = 439

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
    #ball.position = (ball.position[0] + movementState, 200)

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
