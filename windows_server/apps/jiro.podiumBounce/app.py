import jgsapi, pyglet, random

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

def tapLeftStart(event):
    player = players.get(event.addr, None)
    if player != None:
        player.movementForce = -5

def tapRightStart(event):
    player = players.get(event.addr, None)
    if player != None:
        player.movementForce = 5

def tapLeftEnd(event):
    player = players.get(event.addr, None)
    if player != None and player.movementForce == -5:
        player.movementForce = 0

def tapRightEnd(event):
    player = players.get(event.addr, None)
    if player != None and player.movementForce == 5:
        player.movementForce = 0

def accelerometerEvent(event):
    print "Accelerometer event!"
    print "From:", event.addr
    print "X", event.x, "; Y", event.y, "; Z", event.z

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

leftButton = controller.getInteractable("left")
leftButton.addEventListener("tapStart", tapLeftStart)
leftButton.addEventListener("tapEnd", tapLeftEnd)

rightButton = controller.getInteractable("right")
rightButton.addEventListener("tapStart", tapRightStart)
rightButton.addEventListener("tapEnd", tapRightEnd)

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
        self.scale = random.randint(3, 7) / 10.0
        self.movementForce = 0
    def update(self):
        self.x += self.movementForce

print "Welcome to Podium Bounce!"

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()

IMG_BALL = pyglet.image.load('res/ball.png')

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
