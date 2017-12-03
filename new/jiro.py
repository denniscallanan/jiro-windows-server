########################################
# IMPORTS
########################################

import thread, socket, time, random

########################################
# CONSTANTS
########################################

#17417

BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 17417
CSERVER_IP = "localhost"
CSERVER_PORT = 11026

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

    print "Sending broacasts"

    while True:
        time.sleep(1)
        message = "jiroc " + get_ipv4() + " " + get_hostname() + " " + str(0) + " " + game_running
        print message
        s.sendto(message, (BROADCAST_IP, BROADCAST_PORT))

        if random.randint(0, 3) == 0:
            game_running = random.choice(GAMES)

########################################
# PROGRAM STARTS HERE
########################################

thread.start_new_thread(broadcaster, ())

raw_input()
