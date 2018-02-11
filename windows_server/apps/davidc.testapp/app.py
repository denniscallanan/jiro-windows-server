import jgsapi

jiro = jgsapi.GameServer()
jiro.importController("controllers/test.xml")

print "Welcome to testapp!"
for x in jiro.controllers["test"].interactables:
    print jiro.controllers["test"].interactables[x].interactions
while True:
    pass
