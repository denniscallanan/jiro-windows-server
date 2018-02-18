import jgsapi, os

jiro = jgsapi.GameServer()
jiro.importController("controllers/test.xml")

print "Welcome to testapp!"
#for x in jiro.controllers["test"].interactables:
#    print jiro.controllers["test"].interactables[x].interactions
os.system("start notepad.exe")
while True:
    pass
