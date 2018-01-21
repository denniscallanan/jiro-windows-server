import rus, time

class Server(rus.Server):
    def onmessage(self, event):
        #print "Got", event.msg, "from", event.addr
        self.send("I'd like to sincerely thank you my client for sending me that wonderful message.", event.addr)
        #print "Sent thank you message to", event.addr
    def onclientjoin(self, event):
        #print "Client joined:", event.addr
        #time.sleep(3)
        self.send("I'd like to inform you that you have joined.", event.addr)
        #print "Informed", event.addr,"that they joined"
    def onclientleave(self, event):
        pass#print "Client disconnected:", event.addr

Server(36883)
print "Server listening on port 36883..."

rus.keepWindowOpen()
