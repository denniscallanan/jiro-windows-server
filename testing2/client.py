import bs

def message(event):
    print "Got message: " + event.msg
    socket.send("Thanks for your message, server!")

def ready():
    print "Connected to server!"
    socket.send("Hello, Server!")

socket = bs.Client('localhost', 36883)
socket.onmessage(message)
socket.onconnect(ready)

bs.keepWindowOpen()
