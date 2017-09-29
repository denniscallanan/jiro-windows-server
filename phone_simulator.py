########################################################
########################################################
#                                                      #
#     ###  # #  ###  ##  #  ###                        #
#     # #  # #  # #  # # #  #                          #
#     ###  ###  # #  # # #  ###    PHONE SIMULATOR     #
#     #    # #  # #  # # #  #                          #
#     #    # #  ###  #  ##  ###                        #
#                                                      #
########################################################
########################################################

import socket, os

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 36883))

print "Looking for server..."

while True:
    m = s.recvfrom(1024)
    data = m[0].split(" ")
    ip = data[1]
    pc_name = data[2]
    player_count = data[3]
    game_name = data[4]
    break

s.close()

os.system("cls")

print "Found one server!"
print
if (game_name == "#no_game"):
    print pc_name + " has no players connected!"
elif (game_name == "#selecting"):
    print "Selecting game on " + pc_name + " with " + player_count + " players waiting!"
else:
    print game_name.replace("_", " ") + " is being played on " + pc_name + " with " + player_count + " players online!"
raw_input("Press ENTER to connect to server")

os.system("cls")

print "Connecting to server..."

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.connect(('localhost', 11026))    # DO NOT USE localhost on android, use ip recieved from broadcast!!!

os.system("cls")

print "Connected!"

def select_game(games):

    os.system("cls")

    print "You are in charge of the console!"
    print "You must chose a game..."
    print
    print "\n".join(games)

while True:
    m = s2.recvfrom(1024)
    data = m[0].split(" ")
    command = data[0]
    args = [arg.replace("_", " ") for arg in data[1:]]

    #print "RECIEVEVEGFTDEHGHY", data

    if (data[0] == "select_game"):
        select_game(args)
        
