import rus

class Server(rus.Server):
    def onmessage(self, event):
        print "Got message!"
        print event.msg
        print "from"
        print event.addr
        self.send("I'd like to sincerely thank you my client for sending me that wonderful message.", event.addr)
    def onclientjoin(self, event):
        print "Client joined!"
        print event.addr
        self.send("I'd like to inform you that you are recieving this message.", event.addr)
    def onclientleave(self, event):
        print "Client disconnected!"
        print event.addr

Server(36883)
print "Server listening on port 36883"

rus.keepWindowOpen()
