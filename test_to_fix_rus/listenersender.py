import socket as s
import thread
from obj import obj

class Listener:
    def __init__(self, ip, port):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind((ip, port))
        print "Listening on ip:\"", ip, "\" and port:\"", port, "\""
        thread.start_new_thread(self.listen_thread, ())

    def listen_thread(self):
        while True:
            print "LISTENING!"
            data, address = self.socket.recvfrom(512)
            print "GOT DATA from",address
            if data:
                event = obj(msg=data, addr=address)
                self.onmessage(event)

    def onmessage(self):
        pass

class Sender:
    def __init__(self, port):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', port))

    def send(self, msg, addr):
        self.socket.sendto(msg, addr)
        print "SENT DATA to", addr, "from", self.socket.getsockname()

class SenderListener:
    def __init__(self, port):
        #self.sender = Sender(port)
        self.listener = Listener("", port)
        self.listener.onmessage = self.onmessage

    def onmessage(self, event):
        print "Got message",event.msg,"from",event.addr
        #self.sender.send("Hey, Rob!", event.addr)

SenderListener(56789)

raw_input()
