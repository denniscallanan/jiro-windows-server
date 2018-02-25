import jgsapi, pyglet

##################################
# JIRO API CODE
##################################

# Functions

def onPlayerJoin(addr):
    print jgsapi.pretty_ip(addr),"joined app"
    jiro.switchController("test", addr)

def onPlayerLeave(addr):
    print jgsapi.pretty_ip(addr),"left app"

def cleanup():
    window.close()
    pyglet.app.exit()
    print "Podium Bounce server stopped!"

def tapLeft(event):
    print "Left tapped!"

def tapRight(event):
    print "Right tapped!"

# Create game server
jiro = jgsapi.GameServer()
jiro.importController("controllers/main.xml")

# Server events
jiro.onPlayerJoin = onPlayerJoin
jiro.onPlayerLeave = onPlayerLeave
jiro.cleanup = cleanup

# Controller events
jiro.getInteractable("main", "left").addEventListener("tap", tapLeft)
jiro.getInteractable("main", "right").addEventListener("tap", tapRight)

##################################
# MAIN PROGRAM CODE
##################################

print "Welcome to Podium Bounce!"

window = pyglet.window.Window(fullscreen=True)
window.set_exclusive_mouse()

label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()
