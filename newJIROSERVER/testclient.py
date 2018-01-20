import rus

class Client(rus.Client):
    def onmessage(self, event):
        print "Got message!"
        print event.msg

    def onconnect(self):
        print "Connected!!!!!!!"

Client("localhost", 36883)

rus.keepWindowOpen()
