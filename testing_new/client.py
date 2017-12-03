import rus

class Client(rus.Client):
    def onmessage(self, event):
        print "SERVER says", event.msg
        self.sendr("Hello, Server!")

    def onconnect(self):
        print "Connected to 36883!"

client = Client("localhost", 36883)

rus.keepWindowOpen()
