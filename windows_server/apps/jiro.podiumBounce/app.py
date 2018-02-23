import jgsapi

def onPlayerJoin(addr):
    jiro.switchController("test", addr)

jiro = jgsapi.GameServer()
jiro.importController("controllers/test.xml")
jiro.onPlayerJoin = onPlayerJoin
buttonOne = jiro.getInteractable("test", "buttonOne")
buttonTwo = jiro.getInteractable("test", "buttonTwo")
def print3(arg):
    print arg
buttonOne.addEventListener("tap", lambda:print3("ButtonOnePress"))
buttonTwo.addEventListener("tap", lambda:print3("ButtonTwoPress"))

print "Welcome to Podium Bounce!"
#for x in jiro.controllers["test"].interactables:
#    print jiro.controllers["test"].interactables[x].interactions
while True:
    pass
