import socket
from _thread import *
import pickle
server = 'ec2-13-51-176-3.eu-north-1.compute.amazonaws.com'
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
    try:
        if numberOfPlayers <= 8:
            carServerIp = 'ec2-13-49-72-238.eu-north-1.compute.amazonaws.com'
            challengeServerIp = 'ec2-13-48-24-217.eu-north-1.compute.amazonaws.com'
            carServerPort = 5555
            challengeServerPort = 4444
        elif numberOfPlayers > 8 and numberOfPlayers <16:
            carServerIp = 'ec2-16-16-65-120.eu-north-1.compute.amazonaws.com'
            challengeServerIp = 'ec2-16-171-57-141.eu-north-1.compute.amazonaws.com'
            carServerPort = 9999
            challengeServerPort = 3333
        if numberOfPlayers == 16:
            numberOfPlayers = 0
        conn.send(pickle.dumps([carServerPort, challengeServerPort, carServerIp, challengeServerIp]))
    except:
        print('error')



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))