########################################
# MODULES
########################################

import bs, time, thread

########################################
# CONSTANTS
########################################

BROADCAST_PORT = 36883
SERVER_PORT = 11026

########################################
# GLOBAL VARIABLES
########################################

player_count = 0
game_running = "~none"

########################################
# FUNCTIONS
########################################

def on_message(event):
    print event.msg

########################################
# PROGRAM STARTS HERE
########################################

bc = bs.Broadcaster(BROADCAST_PORT)
bc.broadcast_interval(1, lambda:"jiro " + bs.ipv4() + " " + bs.hostname() + " " + str(player_count) + " " + game_running.replace(" ", "%20"))

s = bs.BetterSocketServer(SERVER_PORT)
s.on_message(on_message)


input()
