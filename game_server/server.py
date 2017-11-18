import bs, time

def message(event):
    print "Got message from", event.addr, "-", event.msg
    if event.msg == "Hello, Server!":
        socket.send("Hello, Client!", ("localhost", event.addr[1]))

def clientjoin(event):
    print "Client connected -",event.addr

def clientleave(event):
    print "Client disconnected -",event.addr

socket = bs.Server(36883)
socket.onmessage(message)
socket.onclientjoin(clientjoin)
socket.onclientleave(clientleave)

print "Serving on port 36883..."

while True:
    time.sleep(5)
    socket.sendall("My name is server")
