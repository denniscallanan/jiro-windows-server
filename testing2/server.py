import bs, time

def message(event):
    print "Got message from", event.addr, "-", event.msg
    if event.msg == "Hello, Server!":
        socket.send("Hello, Client!", ("localhost", event.addr[1]))

socket = bs.Server(36883)
socket.onmessage(message)

print "Serving on port 36883..."

while True:
    time.sleep(5)
    socket.sendall("My name is server")
