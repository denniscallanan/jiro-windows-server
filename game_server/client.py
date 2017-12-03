import rus, time

def message(event):
    print "Got message: " + event.msg
    #socket.send("Thanks for your message, server!")

def ready():
    print "Connected to server!"
    socket.sendr("Hello, Server!")

def failed():
    print "Failed to connect to server!"

socket = rus.Client('localhost', 36883)
socket.onmessage(message)
socket.onconnect(ready)
socket.onconnectionfailed(failed)

for i in range(100):
    socket.sendr(str(i))

rus.keepWindowOpen()
