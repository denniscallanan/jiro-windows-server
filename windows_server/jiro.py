########################################
# IMPORTS
########################################

import thread, socket, time, random, rus

########################################
# CONSTANTS
########################################

BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 17417
SERVER_PORT = 11026
#GAME_PORT = 36883

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
# CONSOLE SERVER
########################################

class Server(rus.Server):
    def onmessage(self, event):
        print event.addr, "says", event.msg

    def onclientjoin(self, event):
        print event.addr, "connected!"

    def onclientleave(self, event):
        print event.addr, "disconnected!"

########################################
# BROADCASTER
########################################

def broadcaster():
    global game_running
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print "Sending broadcasts..."

    while True:
        time.sleep(1)
        message = "jiroc " + get_ipv4() + " " + get_hostname() + " " + str(0) + " " + game_running
        #print message
        s.sendto(message, (BROADCAST_IP, BROADCAST_PORT))

        if random.randint(0, 3) == 0:
            game_running = random.choice(GAMES)

########################################
# PROGRAM STARTS HERE
########################################

thread.start_new_thread(broadcaster, ())
server = Server(SERVER_PORT)
print "Windows server running..."

raw_input()
