import socket
from _thread import *
from player import Player

import pickle

server = "192.168.1.11"
port = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")
numberOfPlayers = 0
def threaded_client(conn):
    global numberOfPlayers
    numberOfPlayers += 1
    #while True:
    try:
        print(numberOfPlayers)
        if numberOfPlayers <= 8:
            print('#################################')
            carServerPort = 5555
            challengeServerPort = 4444
        else:
            print('------------------------------------------------')
            carServerPort = 9999
            challengeServerPort = 3333
        if numberOfPlayers == 16:
            numberOfPlayers = 0
        conn.send(pickle.dumps([carServerPort, challengeServerPort]))
        #conn.send(pickle.dumps([5555, 4444]))
    except:
        print('error')



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))


