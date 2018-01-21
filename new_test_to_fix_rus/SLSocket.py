import socket as s, thread
from obj import obj

class SLSocket:
    def __init__(self, port):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', port))
        thread.start_new_thread(self.listen_thread, ())

    def send(self, msg, addr):
        self.socket.sendto(msg, addr)
        print "sent"

    def listen_thread(self):
        print "listening"
        while True:
            data, address = self.socket.recvfrom(512)
            print "got"
            if data:
                event = obj(msg=data, addr=address)
                self.onmessage(event)

    def onmessage(self, event):
        pass

###############################################################

def gotmsg(event):
    print "[CLIENT]", event.msg
    client.send("Hey Client!", event.addr)

client = SLSocket(56789)
client.onmessage = gotmsg

raw_input()
