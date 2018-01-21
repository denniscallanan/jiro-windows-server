import rus

class Client(rus.Client):
    def onconnect(self):
        print "<CONNECTED>"
        self.sendr("Hello, Server!")
    def onmessage(self, event):
        print "[SERVER]",event.msg

Client("localhost", 45678)

rus.keepWindowOpen()
