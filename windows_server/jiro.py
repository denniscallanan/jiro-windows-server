########################################
# IMPORTS
########################################

import thread, socket, time, random, rus

########################################
# CONSTANTS
########################################

BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 17417
CONSOLE_SERVER_PORT = 11026
#GAME_SERVER_PORT = 36883

GAMES = [
    "NO_GAME",
    "\"Doodle_Jump",
    "\"Pokemon",
    "\"Brawlhalla",
    "\"Crash_Bandicoot"
]

########################################
# GLOBAL VARIABLES
########################################

game_running = "NO_GAME"

########################################
# FUNCTIONS
########################################

def get_ipv4():
    return socket.gethostbyname(get_hostname())

def get_hostname():
    return socket.gethostname()

########################################
# BROADCASTER
########################################

def broadcaster():
    global game_running
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print
    print "   Connect your controller in the Jiro app"
    print
    print
    print
    print "LOGS"
    print "===="
    print

    while True:
        time.sleep(1)
        message = "jiroc " + get_ipv4() + " " + get_hostname() + " " + str(0) + " " + game_running
        #print message
        s.sendto(message, (BROADCAST_IP, BROADCAST_PORT))

        #if random.randint(0, 3) == 0:
        #    game_running = random.choice(GAMES)

########################################
# CONSOLE SERVER
########################################

class Server(rus.Server):
    def onmessage(self, event):
        global game_running
        data = event.msg.split(" ")
        cmd, args = data[0], data[1:]

        if cmd == "change_game" and len(args) >= 1:
            game_running = GAMES[int(args[0])]

    def onclientjoin(self, event):
        print event.addr, "connected!"

    def onclientleave(self, event):
        print event.addr, "disconnected!"

########################################
# PROGRAM STARTS HERE
########################################

server = Server(CONSOLE_SERVER_PORT)
print
print
print "   Console ready"
thread.start_new_thread(broadcaster, ())

raw_input()
