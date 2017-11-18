from obj import *
import socket as s, time, thread

HERE = "localhost"
BROADCAST = "255.255.255.255"
IPV4 = s.gethostbyname(s.gethostname())
UNIQUE_BROADCAST_PORT = int(IPV4.split(".")[3])

DATA = 0 * 64
CONNECT = 1 * 64
DISCONNECT = 2 * 64
OTHER = 3 * 64
NO_EXTRA = 0

class Client:
    def __init__(self, serverip, serverport):
        self.sender = Sender()
        self.clientport = self.sender.getPort()
        self.listener = Listener(HERE, self.clientport)
        self.serveraddr = (serverip, serverport)
        self.listener.onmessage(self._onmessage)

        self.send("", typ = CONNECT)

    def _onmessage_func(self, event):
        pass

    def _ready_func(self):
        pass

    def _onmessage(self, event):
        if event.type == CONNECT:
            broadcastport = int(event.msg)
            self.broadcastListener = Listener(BROADCAST, broadcastport)
            self.broadcastListener.onmessage(self._onmessage)
            self._ready_func()
        else:
            self._onmessage_func(event)

    def onmessage(self, func):
        self._onmessage_func = func

    def onconnect(self, func):
        self._ready_func = func

    def send(self, msg, typ=DATA, extra=NO_EXTRA):
        self.sender.send(msg, self.serveraddr, typ, extra)

class Server:
    def __init__(self, serverport):
        self.serverport = serverport
        self.listener = Listener(HERE, serverport)
        self.sender = Sender()

        self.listener.onmessage(self._onmessage)

    def _onmessage_func(self, event):
        pass

    def _onmessage(self, event):
        if event.type == CONNECT:
            self.send(str(self.serverport + UNIQUE_BROADCAST_PORT), event.addr, typ=CONNECT)
        else:
            self._onmessage_func(event)

    def onmessage(self, func):
        self._onmessage_func = func

    def send(self, msg, addr, typ=DATA, extra=NO_EXTRA):
        self.sender.send(msg, addr, typ, extra)

    def sendall(self, msg, typ=DATA, extra=NO_EXTRA):
        self.sender.send(msg, (BROADCAST, self.serverport + UNIQUE_BROADCAST_PORT), typ, extra)

class Listener:
    def __init__(self, ip, port):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        if ip == BROADCAST: ip = ""
        self.socket.bind((ip, port))
        thread.start_new_thread(self.listen_thread, ())

    def _onmessage_func(self, event):
        pass

    def onmessage(self, func):
        self._onmessage_func = func

    def listen_thread(self):
        while True:
            data, address = self.socket.recvfrom(512)
            if data:
                head = ord(data[0])
                msg = data[1:]
                extra = head % 64
                typ = head - extra
                event = obj(msg=msg, addr=address, extra=extra, type=typ)
                self._onmessage_func(event)

class Sender:
    def __init__(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', 0))

    def send(self, msg, addr, typ=DATA, extra=NO_EXTRA):
        data = chr(min(max(typ,0),OTHER) + min(max(extra,0),63)) + msg
        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
        self.socket.sendto(data, addr)
        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 0)

    def getPort(self):
        return int(self.socket.getsockname()[1])

def keepWindowOpen():
    while True:
        pass
