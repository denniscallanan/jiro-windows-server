import rus

class Client(rus.Client):
    def onmessage(self, event):
        print "Got message!"
        print event.msg

    def onconnect(self):
        print "Connected!!!!!!!"

Client("192.168.1.109", 36883)

rus.keepWindowOpen()
