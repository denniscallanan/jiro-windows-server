from obj import *
import socket as s, time, thread, threading, errno, bitm, intervals

HERE = "localhost"
BROADCAST = "255.255.255.255"
IPV4 = s.gethostbyname(s.gethostname())
UNIQUE_BROADCAST_PORT = int(IPV4.split(".")[3])

DATA = 0
NO_DATA = 1

EMPTY = 0
CONNECT = 1
DISCONNECT = 2
DISCONNECT_WARNING = 3

NORMAL_MESSAGE = 0
RELIABLE_MESSAGE = 1
ORDERED_RELIABLE_MESSAGE = 2
MESSAGE_RECEIVED = 3

class Client:
    def __init__(self, serverip, serverport):
        self.serveraddr = (serverip, serverport)
        self.sender = Sender()
        self.clientport = self.sender.port()
        self.listener = Listener(HERE, self.clientport)
        self.listener.onmessage = self._onmessage
##        self.listener.onerror = self.onerror

        self.lastID = -1;
        self.sent_reliable_messages = {}
        self.received_reliable_messages = {}

        header = bitm.Byte()
        header.set(0, NO_DATA)
        header.set(1, 7, CONNECT)
        self._send(header.chr())

        intervals.add(1, self.every_millisecond)

    def _onmessage(self, event):
        header = bitm.Byte(bitm.ord(event.msg[0]))
        msg = event.msg[1:]

        if header.get(0) == NO_DATA:
            if header.get(1, 7) == CONNECT:
                port = int(msg)
                self.broadcastListener = Listener(BROADCAST, port)
                self.broadcastListener.onmessage = self._onmessage
                self.onconnect()

        elif header.get(0) == DATA:
            if header.get(1, 2) == MESSAGE_RECEIVED:
                self.sent_reliable_messages.pop(ord(msg[0]))
            elif header.get(1, 2) == RELIABLE_MESSAGE:
                msgid_chr = msg[0]
                msgid = ord(msgid_chr)
                new_msg = msg[1:]

                res_header = bitm.Byte()
                res_header.set(0, DATA)
                res_header.set(1, 2, MESSAGE_RECEIVED)

                self._send(res_header.chr() + msgid_chr)

                if msgid not in self.received_reliable_messages or self.received_reliable_messages[msgid][1] != new_msg:
                    self.received_reliable_messages[msgid] = [3 * 5 + 2, new_msg]

                    new_event = obj(header=header, msg=new_msg)
                    self.onmessage(new_event)
            elif header.get(1, 2) == NORMAL_MESSAGE:
                new_event = obj(header=header, msg=msg, addr=event.addr)
                self.onmessage(new_event)

    def _send(self, msg):
        self.sender.send(msg, self.serveraddr)

    def send(self, msg):
        header = bitm.Byte()
        header.set(0, DATA)
        self._send(header.chr() + msg)

    def sendr(self, msg):
        msgid = self.nextID()
        
        header = bitm.Byte()
        header.set(0, DATA)
        header.set(1, 2, RELIABLE_MESSAGE)
        message = header.chr() + chr(msgid) + msg
                                      # [ms to wait till retry, retry attempts left, message]
        self.sent_reliable_messages[msgid] = [3, 5, message]
        self._send(message)

    def resend_messages(self):
        to_delete = []
        
        for msgid in self.sent_reliable_messages:
            msg_data = self.sent_reliable_messages[msgid]
            msg_data[0] -= 1

            if msg_data[0] <= 0:
                msg_data[0] = 3
                msg_data[1] -= 1

                if msg_data[1] <= 0:
                    to_delete.append(msgid)
                    continue

                self._send(msg_data[2])

        for msgid in to_delete: self.sent_reliable_messages.pop(msgid, None)

    def every_millisecond(self):
        self.resend_messages()

        to_delete = []
        
        for msgid in self.received_reliable_messages.keys():
            msg_data = self.received_reliable_messages.get(msgid, None)

            if msg_data == None:
                continue
            
            msg_data[0] -= 1

            if msg_data[0] <= 0:
                self.received_reliable_messages.pop(msgid, None)

    def nextID(self):
        self.lastID += 1
        if self.lastID > 255: self.lastID = 0
        return self.lastID

    def onmessage(self, event):
        pass

    def onconnect(self):
        pass

class Server:
    def __init__(self, serverport, dcw=3, dct=4):
        self.clients = {}
        self.serverport = serverport
        self.listener = Listener(HERE, serverport)
        self.listener.onmessage = self._onmessage
        self.sender = Sender()

        self.dcw = dcw
        self.dct = dct
        intervals.adds(1, self.dc_timer)

        self.lastID = -1;
        self.sent_reliable_messages = {}
        self.received_reliable_messages = {}
        intervals.add(1, self.every_millisecond)

    def dc_timer(self):
        to_delete = []
          
        for client in self.clients:
            self.clients[client] += 1
            if self.clients[client] == int(self.dcw):
                header = bitm.Byte()
                header.set(0, NO_DATA)
                header.set(1, 7, DISCONNECT_WARNING)
                self.sender.send(header.chr(), client)
            if self.clients[client] == int(self.dct):
                to_delete.append(client)
              
        for client in to_delete:
            del self.clients[client]
            self.onclientleave(obj(addr=client))

    def _onmessage(self, event):
        print "Cookies crumbled!"
        
        if event.addr not in self.clients:
            self.clients[event.addr] = 0
            self.onclientjoin(obj(addr=event.addr))
        else:
            self.clients[event.addr] = 0
        
        header = bitm.Byte(bitm.ord(event.msg[0]))
        msg = event.msg[1:]
        
        if header.get(0) == NO_DATA:
            if header.get(1, 7) == CONNECT:
                res_header = bitm.Byte()
                res_header.set(0, NO_DATA)
                res_header.set(1, 7, CONNECT)
                self.sender.send(header.chr() + str(self.serverport + UNIQUE_BROADCAST_PORT), event.addr)

        elif header.get(0) == DATA:
            if header.get(1, 2) == NORMAL_MESSAGE:
                new_event = obj(header=header, msg=msg, addr=event.addr)
                self.onmessage(new_event)
            elif header.get(1, 2) == RELIABLE_MESSAGE:
                msgid_chr = msg[0]
                msgid = ord(msgid_chr)
                new_msg = msg[1:]

                res_header = bitm.Byte()
                res_header.set(0, DATA)
                res_header.set(1, 2, MESSAGE_RECEIVED)

                self.sender.send(res_header.chr() + msgid_chr, event.addr)

                tup = (event.addr, msgid)

                if tup not in self.received_reliable_messages or self.received_reliable_messages[tup][1] != new_msg:
                    self.received_reliable_messages[tup] = [3 * 5 + 2, new_msg]

                    new_event = obj(header=header, msg=new_msg, addr=event.addr)
                    self.onmessage(new_event)
            elif header.get(1, 2) == MESSAGE_RECEIVED:
                self.sent_reliable_messages.pop((event.addr, ord(msg[0])))

    def resend_messages(self):
        to_delete = []
        
        for addr, msgid in self.sent_reliable_messages:
            msg_data = self.sent_reliable_messages[(addr, msgid)]
            msg_data[0] -= 1

            if msg_data[0] <= 0:
                msg_data[0] = 3
                msg_data[1] -= 1

                if msg_data[1] <= 0:
                    to_delete.append((addr, msgid))
                    continue

                self.sender.send(msg_data[2], addr)

        for tup in to_delete: self.sent_reliable_messages.pop(tup, None)

    def nextID(self):
        self.lastID += 1
        if self.lastID > 255: self.lastID = 0
        return self.lastID
    
    def every_millisecond(self):
        self.resend_messages()
        
        to_delete = []
        
        for tup in self.received_reliable_messages.keys():
            msg_data = self.received_reliable_messages.get(tup, None)

            if msg_data == None:
                continue
            
            msg_data[0] -= 1

            if msg_data[0] <= 0:
                self.received_reliable_messages.pop(tup, None)

    def _send(self, msg, addr):
        header = bitm.Byte()
        header.set(0, DATA)
        self.sender.send(header.chr() + msg, addr)

    def send(self, msg, addr):
        self._send(msg, addr)

    def sendr(self, msg, addr):
        msgid = self.nextID()
        
        header = bitm.Byte()
        header.set(0, DATA)
        header.set(1, 2, RELIABLE_MESSAGE)
        message = header.chr() + chr(msgid) + msg
                                                   # [ms to wait till retry, retry attempts left, message]
        self.sent_reliable_messages[(addr, msgid)] = [3, 5, message]
        self.sender.send(message, addr)

    def sendall(self, msg):
        self._send(msg, (BROADCAST, self.serverport + UNIQUE_BROADCAST_PORT))

    def onmessage(self, event):
        pass

    def onclientjoin(self):
        pass

    def onclientleave(self):
        pass

class Listener:
    def __init__(self, ip, port):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        if ip == BROADCAST: ip = ""
        self.socket.bind((ip, port))
        thread.start_new_thread(self.listen_thread, ())
        #self.listenfailed_count = 0

    def listen_thread(self):
        while True:
##            try:
            data, address = self.socket.recvfrom(512)
##            self.listenfailed_count = 0
            if data:
                print "WEWEWE"
                event = obj(msg=data, addr=address)
                self.onmessage(event)
##            except s.error as err:
##                if err.errno == errno.WSAECONNRESET:
##                    self.listenfailed_count += 1
##                    self._onlistenfailed_func()
##                else:
##                    raise

    def onmessage(self):
        pass

class Sender:
    def __init__(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', 0))

    def send(self, msg, addr):
        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
        self.socket.sendto(msg, addr)
        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 0)

    def port(self):
        return int(self.socket.getsockname()[1])

def keepWindowOpen():
    while True:
        pass
