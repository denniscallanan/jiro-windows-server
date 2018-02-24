from obj import *
import socket as s, time, thread, threading, errno, bitm, intervals

HERE = "localhost"
ALL = ""
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
        self.socket = SLSocket()
        self.socket.onmessage = self._onmessage

        self.lastID = -1;
        self.sent_reliable_messages = {}
        self.received_reliable_messages = {}

        header = bitm.Byte()
        header.set(0, NO_DATA)
        header.set(1, 7, CONNECT)
        self._send(header.chr())

        self.intervalId = intervals.add(10, self.every_ten_milliseconds)

    def _onmessage(self, event):
        header = bitm.Byte(bitm.ord(event.msg[0]))
        msg = event.msg[1:]

        if header.get(0) == NO_DATA:
            if header.get(1, 7) == CONNECT:
                port = int(msg)
                self.broadcastListener = Listener(BROADCAST, port)
                self.broadcastListener.onmessage = self._onmessage
                self.onconnect()
            elif header.get(1, 7) == DISCONNECT_WARNING:
                header = bitm.Byte()
                header.set(0, NO_DATA)
                header.set(1, 7, EMPTY)
                self._send(header.chr())

        elif header.get(0) == DATA:
            if header.get(1, 2) == MESSAGE_RECEIVED:
                self.sent_reliable_messages.pop(ord(msg[0]), None)
            elif header.get(1, 2) == RELIABLE_MESSAGE:
                msgid_chr = msg[0]
                msgid = ord(msgid_chr)
                new_msg = msg[1:]

                res_header = bitm.Byte()
                res_header.set(0, DATA)
                res_header.set(1, 2, MESSAGE_RECEIVED)

                self._send(res_header.chr() + msgid_chr)

                if msgid not in self.received_reliable_messages or self.received_reliable_messages[msgid][1] != new_msg:
                    #                                     prev: 3 * 5 + 2
                    self.received_reliable_messages[msgid] = [100, new_msg]

                    new_event = obj(header=header, msg=new_msg)
                    self.onmessage(new_event)
            elif header.get(1, 2) == NORMAL_MESSAGE:
                new_event = obj(header=header, msg=msg, addr=event.addr)
                self.onmessage(new_event)

    def _send(self, msg):
        self.socket.send(msg, self.serveraddr)

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
                                      # [ms * 10 to wait till retry, retry attempts left, message]
        self.sent_reliable_messages[msgid] = [1, 5, message]
        self._send(message)

    def resend_messages(self):
        for msgid in self.sent_reliable_messages.keys():
            msg_data = self.sent_reliable_messages.get(msgid, None)
            if msg_data == None: continue
            
            msg_data[0] -= 1

            if msg_data[0] <= 0:
                #ms * 10 to wait till retry
                msg_data[0] = 1
                msg_data[1] -= 1

                if msg_data[1] <= 0:
                    self.sent_reliable_messages.pop(msgid, None)
                    continue

                self._send(msg_data[2])

    def every_ten_milliseconds(self):
        self.resend_messages()
        
        for msgid in self.received_reliable_messages.keys():
            msg_data = self.received_reliable_messages.get(msgid, None)
            if msg_data == None: continue
            
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

    def close(self):
        intervals.stop(self.intervalId)
        self.socket.close()
        if hasattr(self, 'broadcastListener'):
            self.broadcastListener.close()

class Server:
    def __init__(self, serverport, dcw=3, dct=4):
        self.clients = {}
        self.serverport = serverport
        self.socket = SLSocket(serverport)
        self.socket.onmessage = self._onmessage
        self.intervalIds = []

        self.dcw = dcw
        self.dct = dct
        self.intervalIds.append(intervals.adds(1, self.dc_timer))

        self.lastID = -1;
        self.sent_reliable_messages = {}
        self.received_reliable_messages = {}
        self.intervalIds.append(intervals.add(1, self.every_ten_milliseconds))

    def dc_timer(self):
        to_delete = []
          
        for client in self.clients:
            self.clients[client] += 1
            if self.clients[client] == int(self.dcw):
                header = bitm.Byte()
                header.set(0, NO_DATA)
                header.set(1, 7, DISCONNECT_WARNING)
                self.socket.send(header.chr(), client)
            if self.clients[client] == int(self.dct):
                to_delete.append(client)
              
        for client in to_delete:
            del self.clients[client]
            self.onclientleave(obj(addr=client))

    def _onmessage(self, event):
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
                self.socket.send(header.chr() + str(self.serverport + UNIQUE_BROADCAST_PORT), event.addr)

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

                self.socket.send(res_header.chr() + msgid_chr, event.addr)

                tup = (event.addr, msgid)

                if tup not in self.received_reliable_messages or self.received_reliable_messages[tup][1] != new_msg:
                    #                                   prev: 3*5+2
                    self.received_reliable_messages[tup] = [100, new_msg]

                    new_event = obj(header=header, msg=new_msg, addr=event.addr)
                    self.onmessage(new_event)
            elif header.get(1, 2) == MESSAGE_RECEIVED:
                self.sent_reliable_messages.pop((event.addr, ord(msg[0])), None)

    def resend_messages(self):
        for k in self.sent_reliable_messages.keys():
            addr, msgid = k
            msg_data = self.sent_reliable_messages.get(k, None)
            if msg_data == None: continue
            
            msg_data[0] -= 1

            if msg_data[0] <= 0:
                msg_data[0] = 1
                msg_data[1] -= 1

                if msg_data[1] <= 0:
                    self.sent_reliable_messages.pop(k, None)
                    continue

                self.socket.send(msg_data[2], addr)

    def nextID(self):
        self.lastID += 1
        if self.lastID > 255: self.lastID = 0
        return self.lastID
    
    def every_ten_milliseconds(self):
        self.resend_messages()
        
        to_delete = []
        
        for tup in self.received_reliable_messages.keys():
            msg_data = self.received_reliable_messages.get(tup, None)

            if msg_data == None:
                continue
            
            msg_data[0] -= 1

            if msg_data[0] <= 0:
                to_delete.append(tup)

        for tup in to_delete:
                self.received_reliable_messages.pop(tup, None)

    def _send(self, msg, addr):
        header = bitm.Byte()
        header.set(0, DATA)
        self.socket.send(header.chr() + msg, addr)

    def send(self, msg, addr):
        self._send(msg, addr)

    def sendr(self, msg, addr):
        msgid = self.nextID()
        
        header = bitm.Byte()
        header.set(0, DATA)
        header.set(1, 2, RELIABLE_MESSAGE)
        message = header.chr() + chr(msgid) + msg
                                                   # [ms * 10 to wait till retry, retry attempts left, message]
        self.sent_reliable_messages[(addr, msgid)] = [1, 5, message]
        self.socket.send(message, addr)

    def sendall(self, msg):
        self._send(msg, (BROADCAST, self.serverport + UNIQUE_BROADCAST_PORT))

    def onmessage(self, event):
        pass

    def onclientjoin(self, event):
        pass

    def onclientleave(self, event):
        pass

    def close(self):
        for intervalId in self.intervalIds:
            intervals.stop(intervalId)
        self.socket.close()

class SLSocket:
    def __init__(self, port=0):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.socket.bind(('', port))
        self.exiting = False
        thread.start_new_thread(self.listen_thread, ())

    def send(self, msg, addr):
        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
        self.socket.sendto(msg, addr)
        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 0)

    def listen_thread(self):
        while True:
            if self.exiting:
                break
            try:
                data, address = self.socket.recvfrom(512)
            except Exception as e:
                print e
                continue
            if data:
                event = obj(msg=data, addr=address)
                self.onmessage(event)

    def onmessage(self, event):
        pass

    def close(self):
        self.exiting = True
        self.socket.close()

class Listener:
    def __init__(self, ip, port):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        if ip == BROADCAST: ip = ""
        self.socket.bind((ip, port))
        self.exiting = False
        thread.start_new_thread(self.listen_thread, ())
        
    def listen_thread(self):
        while True:
            if self.exiting:
                break
            data, address = self.socket.recvfrom(512)
            if data:
                event = obj(msg=data, addr=address)
                self.onmessage(event)

    def onmessage(self):
        pass

    def close(self):
        self.exiting = True
        self.socket.close()

##class Sender:
##    def __init__(self, port=0):
##        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
##        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
##        self.socket.bind(('', port))
##
##    def send(self, msg, addr):
##        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
##        self.socket.sendto(msg, addr)
##        if addr[0] == BROADCAST: self.socket.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 0)

def keepWindowOpen():
    while True:
        pass
