import jgsapi, pyglet

def onPlayerJoin(addr):
    print "Switching controller for", jgsapi.pretty_ip(addr)
    jiro.switchController("test", addr)

def cleanup():
    print "Podium Bounce server stopped!"

jiro = jgsapi.GameServer()
jiro.importController("controllers/test.xml")
jiro.onPlayerJoin = onPlayerJoin
jiro.cleanup = cleanup
#buttonOne = jiro.getInteractable("test", "buttonOne")
#buttonTwo = jiro.getInteractable("test", "buttonTwo")
#def printFunc(arg):
#    print arg
#buttonOne.addEventListener("tap", lambda:printFunc("ButtonOnePress"))
#buttonTwo.addEventListener("tap", lambda:printFunc("ButtonTwoPress"))

print "Welcome to Podium Bounce!"

window = pyglet.window.Window(fullscreen=True)

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
