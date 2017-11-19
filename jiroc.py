########################################
# IMPORTS
########################################

from thread import *
import socket, time

########################################
# CONSTANTS
########################################

BROADCAST_IP = "255.255.255.255"
BROADCAST_PORT = 36883
SERVER_IP = "localhost"
SERVER_PORT = 11026

########################################
# GLOBAL VARIABLES
########################################

game_running = "#no_game"

player_count = 0

conns = []
conn_ids = []

games = [
    "One in the spinner",
    "Doodle jump",
    "Epic car racers"
]

########################################
# FUNCTIONS
########################################

def get_ipv4():
    return socket.gethostbyname(get_hostname())

def get_hostname():
    return socket.gethostname()

def get_command(msg):
    data = msg.split(" ")
    if (len(data) > 0):
        command = data[0]
        args = [arg.replace("_", " ") for arg in data[1:]]
        return (command, args)
    return ("", [])

def create_socket(typ = socket.SOCK_STREAM):
    s = socket.socket(socket.AF_INET, typ)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s

def create_broadcast_socket():
    s = create_socket(socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return s

def broadcast(s, message):
    s.sendto("jiro " + message, (BROADCAST_IP, BROADCAST_PORT))

########################################
# THREADS
########################################

def broadcaster():
    
    s = create_broadcast_socket()
    
    print "Sending broadcasts"

    while True:
        
        time.sleep(1)
        message = get_ipv4() + " " + get_hostname() + " " + str(player_count) + " "
        
        message += game_running.replace(" ", "_")
        
        broadcast(s, message)

def jiro():
    global player_count

    s = create_socket()
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen(2)
    
    print "Listening for connections"

    conn, addr = s.accept()
    connid = addr[0]+":"+str(addr[1])

    conn_ids.append(connid)
    conns.append(conn)

    player_count += 1
    
    start_new_thread(client, (conn, connid))

def client(conn, connid):
    global game_running

    print "Client connected " + connid

    if (game_running == "#no_game"):
        conn.send("select_game " + " ".join([game.replace(" ", "_") for game in games]))

    game_running = "#selecting"

    while True:
        
        data = conn.recv(1024)
        if not data:
            break

        cmd, args = get_command(data)

        print(cmd, args)

########################################
# PROGRAM STARTS HERE
########################################

start_new_thread(jiro, ())
start_new_thread(broadcaster, ())

raw_input()
