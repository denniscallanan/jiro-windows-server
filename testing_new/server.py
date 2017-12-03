import rus, time

class Server(rus.Server):
    def onmessage(self, event):
        print event.addr, "says", event.msg

    def onclientjoin(self, event):
        print event.addr, "connected!"

    def onclientleave(self, event):
        print event.addr, "disconnected!"

server = Server(36883)
print "Server created, port 36883!"

while True:
    time.sleep(2)
    server.sendall("Hello, Clients!")
    time.sleep(2)
    server.sendr("Hello, My client!", server.clients.iterkeys().next())

rus.keepWindowOpen()
