import bs, time

end_broadcast = False
s = None

def on_broadcast(event):
    global end_broadcast
    if (end_broadcast):
        return
    end_broadcast = True
    print event.msg
    print "Connecting..."
    connect(event.msg.split(" "))

def connect(data):
    global s
    ip = data[1]
    s = bs.Socket(ip, 11026)
    s.send("connect")
    print "Connected."
    s.on_message(on_message)

def on_message(event):
    print "pooppooo"

bc = bs.BroadcastListener(36883)
bc.on_broadcast(on_broadcast)

input()
