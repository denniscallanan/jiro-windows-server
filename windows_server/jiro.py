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

    #p = subprocess.Popen(app["info"][u"run"], cwd=app["dir"], shell=True)
    #p.wait()
    #os.startfile(app["dir"] + app["info"][u"run"])
    current_app_process = subprocess.Popen([sys.executable, app["info"][u"run"]], cwd=os.path.join(os.getcwd(), app["dir"]))

def stop_app():
    '''change_app(None)
    cl = rus.Client("localhost", 36883)
    def onconnect():
        cl.sendr("e") #exit
        cl.close()
        if func != None:
            func()
    cl.onconnect = onconnect'''
    
    os.kill(current_app_process.pid, signal.CTRL_C_EVENT)
    change_app(None)


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
        message = "jiroc " + get_ipv4() + " " + get_hostname() + " " + str(0) + " " + current_app_name
        s.sendto(message, (BROADCAST_IP, BROADCAST_PORT))

########################################
# CONSOLE SERVER
########################################

class Server(rus.Server):
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
            elif len(args) == 1 and args[0] == "stop":
                print "Stopping app..."
                stop_app()
            else:
                print "Invalid app sub-command"
        elif cmd == "ready":
            print "Game is ready!"
        else:
            print "Invalid command"

    def onclientjoin(self, event):
        print event.addr, "connected!"

    def onclientleave(self, event):
        print event.addr, "disconnected!"

########################################
# PROGRAM STARTS HERE
########################################

populate_apps_list()

server = Server(CONSOLE_SERVER_PORT)
print "\n\n   Console ready"
thread.start_new_thread(broadcaster, ())

raw_input()
