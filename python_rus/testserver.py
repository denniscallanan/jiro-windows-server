import rus, time

class Server(rus.Server):
    def onmessage(self, event):
        print "[",event.addr,"]",event.msg
        self.sendr("Hello, Client!", event.addr)
    def onclientjoin(self, event):
        print "< JOIN",event.addr,">"
    def onclientleave(self, event):
        print "< LEAVE",event.addr,">"

server = Server(45678)
print "Server started!"

while True:
    server.sendall("This is a broadcast!")
    time.sleep(5)

rus.keepWindowOpen()
