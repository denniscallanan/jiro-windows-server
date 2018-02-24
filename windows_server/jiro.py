########################################
# IMPORTS
########################################

import thread, socket, time, random, rus, glob, json, os, subprocess, sys, signal

########################################
# CONSTANTS
########################################

BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 17417
CONSOLE_SERVER_PORT = 11026

########################################
# GLOBAL VARIABLES
########################################

apps = {}
app_list = []
app = None
current_app = None
current_app_process = None
current_app_name = "NO_APP"

########################################
# FUNCTIONS
########################################

def get_ipv4():
    return socket.gethostbyname(get_hostname())

def get_hostname():
    return socket.gethostname()

def populate_apps_list():
    dirs = glob.glob("apps/*/")
    for d in dirs:
        with open(d + "japp.json", "r") as f:
            data = json.load(f)
        apps[d[5:].replace("\\", "")] = {'dir': d, 'info': data}
        app_list.append((d[5:].replace("\\", ""), {'dir': d, 'info': data}))                  #fix

def change_app(ap):
    global current_app, current_app_name, app, current_app_process
    if ap == None:
        app = None
        current_app = None
        current_app_process = None
        current_app_name = "NO_APP"
        return

    app = apps[ap]
    current_app = ap
    current_app_name = "\"" + app["info"][u"name"].replace(" ", "_")
    current_app_process = subprocess.Popen([sys.executable, app["info"][u"run"]], cwd=os.path.join(os.getcwd(), app["dir"]))

def stop_app():
    os.kill(current_app_process.pid, signal.CTRL_C_EVENT)
    change_app(None)

def pretty_ip(addr):
    return addr[0].split(".")[-1]+":"+str(addr[1])

########################################
# BROADCASTER
########################################

def broadcaster():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print "\n   Connect your controller in the Jiro app\n\n"

    while True:
        time.sleep(1)
        message = "jiroc " + get_ipv4() + " " + get_hostname() + " " + str(len(server.players)) + " " + current_app_name
        s.sendto(message, (BROADCAST_IP, BROADCAST_PORT))

########################################
# CONSOLE SERVER
########################################

class Server(rus.Server):
    def __init__(self, port):
        rus.Server.__init__(self, port)
        self.players = []
    def onmessage(self, event):
        data = event.msg.split(" ")
        cmd, args = data[0], data[1:]

        if cmd == "app":
            if len(args) == 2 and args[0] == "start":
                if current_app != None:
                    print "Changing app to " + args[1] + "..."
                    stop_app()
                    thread.start_new_thread(lambda: (time.sleep(3), change_app(args[1])), ())
                else:
                    print "Starting app " + args[1] + "..."
                    change_app(args[1])
                for con in self.clients:
                    self.sendr("app ready", con)
                self.sendr("app yourInCharge", self.players[0])
            elif len(args) == 1 and args[0] == "stop":
                print "Stopping app..."
                stop_app()
            elif len(args) == 2 and args[0] == "getNext":
                index = int(args[1])
                if index < len(apps):
                    app = app_list[index]
                    #app haveInfo <appName> <displayName> <fancyIconUrl> FUTURE: <...>
                    print "Sending app info..."
                    self.sendr("app haveInfo " + app[0] + " " + app[1]["info"][u"name"].encode("ascii", "ignore").replace(" ", "_") + "   ", event.addr) #temp
                else:
                    print "Couldn't get app index that doesn't exist"

            else:
                print "Invalid app sub-command"
        elif cmd == "ready":
            print "Game is ready!"
        elif cmd == "join":
            if event.addr not in self.players:
                self.players.append(event.addr)
                #print event.addr, "joined!"
                print pretty_ip(event.addr), "connected to console"
                if current_app == None:
                    if len(self.players) == 1:
                        self.sendr("app gimme", event.addr)
                    else:
                        self.sendr("app beingSelected", event.addr)
                else:
                    self.sendr("app ready", event.addr)

        else:
            print "Invalid command"

    def onclientjoin(self, event):
        #print event.addr, "connected!"
        pass

    def onclientleave(self, event):
        if event.addr in self.players:
            self.players.remove(event.addr)
            if len(self.players) > 0:
                self.sendr("app yourInCharge", self.players[0])
            if len(self.players) == 0:
                if current_app_process != None:
                    stop_app()
            #print event.addr, "left!"
            print pretty_ip(event.addr), "disconnected from console"
        #print event.addr, "disconnected!"

########################################
# PROGRAM STARTS HERE
########################################

populate_apps_list()

server = Server(CONSOLE_SERVER_PORT)
print "\n\n   Console ready"
thread.start_new_thread(broadcaster, ())

raw_input()
