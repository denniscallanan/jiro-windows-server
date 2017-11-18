from obj import *
import socket as s, time, thread

class Broadcaster:
    def __init__(self, port):
        self.ip, self.port = self.address = ('255.255.255.255', port)
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)

    def broadcast(self, message):
        self.socket.sendto(message, self.address)

    def broadcast_interval(self, interval, msg):
        thread.start_new_thread(self.broadcast_interval_thread, (interval, msg))

    def broadcast_interval_thread(self, interval, msg):
        while True:
            if type(msg) is str:
                self.broadcast(msg)
            else:
                self.broadcast(msg())
            time.sleep(interval)

class BroadcastListener:
    def __init__(self, port):
        self.ip, self.port = self.address = ('', port)
        self.on_message_func = None
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(self.address)

    def on_broadcast(self, func):
        if self.on_message_func != None:
            raise Exception("on_broadcast function already bound")
        self.on_message_func = func
        thread.start_new_thread(self.listen_thread, ())

    def listen_thread(self):
        while True:
            data, address = self.socket.recvfrom(512) 
            if data:
                self.on_message_func(obj(msg=data, addr=address, socket=self))

class SocketServer:
    def __init__(self, port):
        self.ip, self.port = self.address = ("localhost", port)
        self.on_message_func = None
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(self.address)

    def on_message(self, func):
        if self.on_message_func != None:
            raise Exception("on_message function already bound")
        self.on_message_func = func
        thread.start_new_thread(self.listen_thread, ())

    def listen_thread(self):
        while True:
            data, address = self.socket.recvfrom(512) 
            if data:
                e = obj(msg=data, addr=address, socket=self)
                self.on_recv_message(e)
                self.on_message_func(e)

    def send(self, address, message):
        self.socket.sendto(message, address)

    def on_recv_message(self, event):
        pass

class BetterSocketServer(SocketServer):
    clients = []

    def on_recv_message(self, event):
        print event

class Socket:
    def __init__(self, ip, port):
        self.ip, self.port = self.address = (ip, port)
        self.on_message_func = None
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

    def on_message(self, func):
        #if self.on_message_func != None:
        #    raise Exception("on_message function already bound")
        #self.on_message_func = func
        #thread.start_new_thread(self.listen_thread, ())
        pass

    def listen_thread(self):
        while True:
            data, address = self.socket.recvfrom(512) 
            if data:
                self.on_message_func(obj(msg=data, addr=address, socket=self))

    def send(self, message):
        self.socket.sendto(message, self.address)

###

def ipv4():
    return s.gethostbyname(hostname())

def hostname():
    return s.gethostname()

        
            

##class Socket:
##    def __init__(self, port, broadcast=False):
##        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
##        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
##        if (broadcast == False):
##            self.ip, self.port = self.address = ('localhost', port)
##            self.host()
##        elif (broadcast == True):
##            self.ip, self.port = self.address = ('255.255.255.255', port)
##            self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
##        else:
##            self.ip, self.port = self.address = (broadcast, port)
##
##    def host(self):
##        self.socket.bind(self.address)
##
##    def on_message(self, func):
##        self.on_message_func = func
##        thread.start_new_thread(self.listen_thread, ())
##
##    def listen_thread(self):
##        while True:
##            data, address = self.socket.recvfrom(512) 
##            if data:
##                self.on_message_func(obj(msg=data, addr=address, socket=self))
##
##    def send(self, message, address=None):
##        if (address == None): address = self.address
##        self.socket.sendto(message, address)
##    
##    def broadcast(self, message):
##        self.send(message)
