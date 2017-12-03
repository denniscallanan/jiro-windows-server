from obj import *
import socket as s, time, thread, errno

HERE = "localhost"
BROADCAST = "255.255.255.255"
IPV4 = s.gethostbyname(s.gethostname())
UNIQUE_BROADCAST_PORT = int(IPV4.split(".")[3])

DATA = 0 * 64
CONNECT = 1 * 64
DISCONNECT = 2 * 64
RECONNECT = 3 * 64
NO_EXTRA = 0

class Client:
    def __init__(self, serverip, serverport):
        self.sender = Sender()
        self.clientport = self.sender.getPort()
        self.listener = Listener(HERE, self.clientport)
        self.serveraddr = (serverip, serverport)
        self.listener.onmessage(self._onmessage)
        self.listener.onlistenfailed(self._onlistenfailed)

        self.send("", typ = CONNECT)

    def _onmessage_func(self, event):
        pass

    def _ready_func(self):
        pass

    def _ondisconnect_func(self):
        pass

    def _onconnectionfailed_func(self):
        pass

    def _onmessage(self, event):
        if event.type == CONNECT:
            broadcastport = int(event.msg)
            self.broadcastListener = Listener(BROADCAST, broadcastport)
            self.broadcastListener.onmessage(self._onmessage)
            self._ready_func()
        elif event.type == DISCONNECT:
            self._ondisconnect_func()
        elif event.type == DATA:
            self._onmessage_func(event)

    def _onlistenfailed(self):
        if self.listener.listenfailed_count < 20:
            self.send("", typ = CONNECT)
        elif self.listener.listenfailed_count == 20:
            self._onconnectionfailed_func()

    def onmessage(self, func):
        self._onmessage_func = func

    def onconnect(self, func):
        self._ready_func = func

    def ondisconnect(self, func):
        self._ondisconnect_func = func

    def onconnectionfailed(self, func):
        self._onconnectionfailed_func = func

    def send(self, msg, typ=DATA, extra=NO_EXTRA):
        self.sender.send(msg, self.serveraddr, typ, extra)

    def reconnect(self):
        self.send("", typ=RECONNECT)

class Server:
    def __init__(self, serverport, client_dc_time=7, client_rc_time=7):
        self.clients = {}
        self.serverport = serverport
        self.listener = Listener(HERE, serverport)
        self.sender = Sender()
        self.listener.onmessage(self._onmessage)

        thread.start_new_thread(self.dc_timer, ())

        self.client_dc_time = client_dc_time
        self.client_rc_time = client_rc_time

    def dc_timer(self):
        while True:
            time.sleep(1)

            to_delete = []
            
            for client in self.clients:
                self.clients[client] -= 1
                if self.clients[client] == self.client_rc_time:
                    self.send("", client, typ=DISCONNECT)
                if self.clients[client] <= 0:
                    to_delete.append(client)
                    self._onclientleave_func(obj(addr=client))

            for client in to_delete: del self.clients[client]

    def _onmessage_func(self, event):
        pass

    def _onclientjoin_func(self, event):
        pass

    def _onclientleave_func(self, event):
        pass

    def _onmessage(self, event):
        if not event.addr in self.clients:
            self._onclientjoin_func(obj(addr=event.addr))
        self.clients[event.addr] = self.client_dc_time + self.client_rc_time
        if event.type == CONNECT:
            self.send(str(self.serverport + UNIQUE_BROADCAST_PORT), event.addr, typ=CONNECT)
        elif event.type == DISCONNECT:
            del self.clients[event.addr]
            self._onclientleave_func(obj(addr=event.addr))
        elif event.type == DATA:
            self._onmessage_func(event)

    def onmessage(self, func):
        self._onmessage_func = func

    def onclientjoin(self, func):
        self._onclientjoin_func = func

    def onclientleave(self, func):
        self._onclientleave_func = func

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
        self.listenfailed_count = 0

    def _onmessage_func(self, event):
        pass

    def _onlistenfailed_func(self):
        pass

    def onmessage(self, func):
        self._onmessage_func = func

    def onlistenfailed(self, func):
        self._onlistenfailed_func = func

    def listen_thread(self):
        while True:
            try:
                data, address = self.socket.recvfrom(512)
                self.listenfailed_count = 0
                if data:
                    head = ord(data[0])
                    msg = data[1:]
                    extra = head % 64
                    typ = head - extra
                    event = obj(msg=msg, addr=address, extra=extra, type=typ)
                    self._onmessage_func(event)
            except s.error as err:
                if err.errno == errno.WSAECONNRESET:
                    self.listenfailed_count += 1
                    self._onlistenfailed_func()
                else:
                    raise

class Sender:
    def __init__(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', 0))

    def send(self, msg, addr, typ=DATA, extra=NO_EXTRA):
        data = chr(min(max(typ,0),RECONNECT) + min(max(extra,0),63)) + msg
        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
        self.socket.sendto(data, addr)
        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 0)

    def getPort(self):
        return int(self.socket.getsockname()[1])

def keepWindowOpen():
    while True:
        pass
