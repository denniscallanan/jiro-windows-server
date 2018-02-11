import rus, thread

state = 0

class ConsoleSocket(rus.Client):
    def onmessage(self, event):
        pass

    def onconnect(self):
        print "Connected"
        thread.start_new_thread(self.message_sending, ())

    def message_sending(self):
        print
        while True:
            cmd = raw_input("Command: ")
            self.sendr(cmd)

def onBroadcast(event):
    global state
    if state == 0:
        data = event.msg.split(" ")
        print "Found " + data[2]
        if data[4] == "NO_APP":
            print "There is no game running!"
        else:
            print "Game running: " + data[4][1:].replace("_", " ")
        print "Players online: " + data[3]
        print
        print "Connecting..."
        state = 1

        consoleSocket()

def consoleSocket():
    ConsoleSocket("localhost", 11026)

broadcastListener = rus.Listener("255.255.255.255", 17417)
broadcastListener.onmessage = onBroadcast

rus.keepWindowOpen()
