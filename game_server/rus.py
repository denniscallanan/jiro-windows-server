import bs, math, threading

NORMAL_MESSAGE = 0
RELIABLE_MESSAGE = 1
RELIABLE_MESSAGE_ORDERED = 2
RECEIVED_MESSAGE = 3

class Client:
    def __init__(self, serverip, serverport):
        self.messages_to_resend = {}
        self.socket = bs.Client(serverip, serverport)
        self.socket.onmessage(self._onmessage)
        self.socket.onconnect(self._onconnect)
        self.socket.ondisconnect(self._ondisconnect)
        self.socket.onconnectionfailed(self._onconnectionfailed)
        self.nextids()
        threading.Timer(0.004, self.resend_messages).start()

    def nextids(self):
        self.nextids = {}
        for i in range(16):
            self.nextids[i] = 0

    def nextid(self, og=0):
        nxt = self.nextids[og]
        self.nextids[og] += 1
        if self.nextids[og] == 65536:
            self.nextids[og] = 0
        return nxt

    def formatid(self, msgid):
        sega = math.floor(msgid / 256) 
        segb = msgid % 256
        return chr(int(sega)) + chr(int(segb))

    def send(self, msg):
        self.socket.send(msg, extra=NORMAL_MESSAGE)

    def sendr(self, msg, og=0):
        if og == False: og = 0
        if og == True: og = 1
        og = min(max(og,0),15)

        msgid = self.nextid(og)
        msgidf = self.formatid(msgid)

        self.messages_to_resend[(msgid, og)] = msgidf + msg
        
        if og == 0:
            self.socket.send(msgidf + msg, extra=RELIABLE_MESSAGE)
        else:
            self.socket.send(msgidf + msg, extra=RELIABLE_MESSAGE_ORDERED + og*4)

    def _onmessage_func(self, event):
        pass

    def _onconnect_func(self):
        pass

    def _onconnectionfailed_func(self):
        pass

    def _onmessage(self, event):
        msg_reliability, og = split_extra(event.extra)
        if msg_reliability == RECEIVED_MESSAGE:
            self.messages_to_resend.pop((get_msg_id(event.msg), og), None)
            return
        self._onmessage_func(event)

    def _onconnect(self):
        self._onconnect_func()

    def _onconnectionfailed(self):
        self._onconnectionfailed_func()

    def _ondisconnect(self):
        self.socket.reconnect()

    def onmessage(self, func):
        self._onmessage_func = func

    def onconnect(self, func):
        self._onconnect_func = func

    def onconnectionfailed(self, func):
        self._onconnectionfailed_func = func

    def resend_messages(self):
        for key in self.messages_to_resend.keys():
            msg = self.messages_to_resend.get(key, None)
            if msg:
                msgid, og = key

                if og == 0:
                    self.socket.send(msg, extra=RELIABLE_MESSAGE)
                else:
                    self.socket.send(msg, extra=RELIABLE_MESSAGE_ORDERED + og*4)

        threading.Timer(0.004, self.resend_messages).start()

class Server:
    def __init__(self, serverport):
        self.socket = bs.Server(serverport)
        self.socket.onmessage(self._onmessage)
        self.socket.onclientjoin(self._onclientjoin)
        self.socket.onclientleave(self._onclientleave)
        self.client_messages()

    def client_messages(self):
        self.client_messages = {}
        for i in range(16):
            self.client_messages[i] = {}

    def _onmessage_func(self, event):
        pass

    def _onclientjoin_func(self, event):
        pass

    def _onclientleave_func(self, event):
        pass

    def _onmessage(self, event):
        #print "Just informing you that i got some message"
        msg_reliability, og = split_extra(event.extra)
        if msg_reliability == NORMAL_MESSAGE:
            self._onmessage_func(event)
            return
        msg_id_f = event.msg[0:2]
        msg_id = get_msg_id(event.msg)
        msg = event.msg = event.msg[2:]
        msg_hash = hash(msg)
        client_messages = self.client_messages[og]
        key = (msg_id, event.addr)
        if msg_hash == client_messages.get(key, None):
            self.socket.send(msg_id_f, event.addr, extra=RECEIVED_MESSAGE + og * 4)
            return
        client_messages[key] = msg_hash
        pop_msg_id = msg_id - 128
        if pop_msg_id < 0: pop_msg_id += 65536
        client_messages.pop(pop_msg_id, None)
        if msg_reliability == RELIABLE_MESSAGE_ORDERED:
            pass
        self._onmessage_func(event)
        self.socket.send(msg_id_f, event.addr, extra=RECEIVED_MESSAGE + og * 4)

    def _onclientjoin(self, event):
        self._onclientjoin_func(event)

    def _onclientleave(self, event):
        self._onclientleave_func(event)

    def onmessage(self, func):
        self._onmessage_func = func

    def onclientjoin(self, func):
        self._onclientjoin_func = func

    def onclientleave(self, func):
        self._onclientleave_func = func

    def send(self, msg, addr):
        self.socket.send(msg, addr, extra=NORMAL_MESSAGE)

    def sendr(self, msg, addr, og=0):
        if og == False: og = 0
        if og == True: og = 1
        og = min(max(og,0,15))

        msgid = self.nextid(og)
        msgidf = self.formatid(msgid)
        
        if og == 0:
            self.socket.send(msgidf + msg, addr, extra=RELIABLE_MESSAGE)
        else:
            self.socket.send(msgidf + msg, addr, extra=RELIABLE_MESSAGE_ORDERED + og*4)

    def sendall(self, msg):
        self.socket.sendall(msg, extra=NORMAL_MESSAGE)

    def sendallr(self, msg, og=0):
        for addr in self.socket.clients:
            self.sendr(msg, addr, og)

def split_extra(extra):
    a = extra % 4
    b = (extra - a) / 4
    return a, b

def get_msg_id(msg):
    return ord(msg[0]) * 256 + ord(msg[1])

keepWindowOpen = bs.keepWindowOpen
