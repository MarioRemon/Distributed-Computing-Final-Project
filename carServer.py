import socket
from _thread import *
from player import Player


import pickle

server = "10.1.0.110"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")


#players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]
players = []
numOfPlayers = 0
rank = [[]]
#rankPlayers = []
positionOfPlayers = []
def threaded_client(conn, playerId):
    player = Player(playerId, '', 0, 0, 0, 0, 0, len(players), 0, 0)
    #rank.append([playerId, 0])
    print(playerId)
    newPos = [[playerId, '(0, 0)']]
    mapScore = [[0, 0]]
    #rankPlayers.append(mapScore)
    positionOfPlayers.append(newPos)
    print("Poooooooooooosition")
    print(positionOfPlayers)
    print(positionOfPlayers[playerId])
    print(positionOfPlayers[playerId][0][0])
    print(positionOfPlayers[playerId][0][1])
    #rankPlayers[playerId] = 0
    print("rankooooooooooooooooooooooooooooooo")
    players.append(player)
    #print(rank)
    global numOfPlayers
    numOfPlayers += 1
    conn.send(pickle.dumps(players[playerId]))
    first3Rankers = []
    reply = ""
    reply1 = []
    while True:
        #rankPlayers = sorted(rankPlayers, key=lambda col: col[1], reverse=True)
        print('Maaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaario')
        #rankPlayers.sort(key=lambda x: x[0], reverse=True)
        #print(rankPlayers)
        print('mariooooooooooooooooooooooooooooooooo')
        #rankPlayers = sorted(rankPlayers, key=itemgetter(1))
        #rankers.reverse()
        #print(rankers)
        try:
            data = pickle.loads(conn.recv(2048))
            #players[player] = data
            print('Data Received')
            print(data)

            if not data:
                print("Disconnected")
                print('maaaaaaaaaaaaaaaaaaaaaaaaaaaaaafis')
                break
            else:
                clientRequest = data.split(':', 2)
                if clientRequest[0] == '0':
                    conn.sendall(pickle.dumps(numOfPlayers))
                    print(len(players))
                elif clientRequest[0] == '1':
                    # idPlayer = 0
                    # maxMapComplete = '0'
                    # maxScore = '0'
                    # for element in rankPlayers:
                    #     print('foooooooooooooooooor')
                    #     print(element)
                    #     print(element[0][1])
                    #     print(element[0][2])
                    #     if ((float(element[0][1]) >= float(maxMapComplete)) and (
                    #             float(element[0][2]) >= float(maxScore))):
                    #         # and (float(element[0][2]) >= float(maxScore))):
                    #         # if (int(element[0][1]) >= int(maxScore)):
                    #         print('yalaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                    #         idPlayer = element
                    #         print(idPlayer)
                    #         maxMapComplete = element[0][1]
                    #         print(maxMapComplete)
                    #         maxScore = element[0][2]
                    #         print(maxScore)
                    conn.send(pickle.dumps('1'))
                    #conn.send(pickle.dumps(rankPlayers[0]))
                elif clientRequest[0] == '2':
                        #conn.send(pickle.dumps('1'))
                        print("Update the map complete")
                        player.mapComplete = clientRequest[1]
                        player.score = clientRequest[2]
                        #rankPlayers[playerId][0][1] = (clientRequest[1])
                        #rankPlayers[playerId][0][2] = clientRequest[2]
                        conn.send(pickle.dumps('1'))
                        #conn.send(pickle.dumps(idPlayer))
                        # #rank[playerId][1] = int(clientRequest[1])
                        # print("yaaaaaaaaaaaaaaaaaaaaaa MARIOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                        # print(rankPlayers)
                elif clientRequest[0] == '4':
                    conn.sendall(pickle.dumps(playerId))
                elif clientRequest[0] == '3':
                    #x = tuple(map(int, clientRequest[1].split(', ')))
                    positionOfPlayers[playerId][0][1] = clientRequest[1]
                    print(positionOfPlayers[playerId])
                    print('hena el serverrrrrrrrrrrrr')
                    print(clientRequest[1])
                    #sendall to him (id,coordinates)
                    #store him
                    conn.send(pickle.dumps(positionOfPlayers))
                    #for value in set(players) - {playerId}:
                    #    print("value")
                    ##    print(value)
                    #    reply1.append(value)
                    #    print("reply")
                    #    print(*reply1)
                    print("Received: ", data)
                    print("Sending : ", reply1)



        # conn.sendall(pickle.dumps(len(players)))
        except:
            break
    print("Lost connection")
    conn.close()
    player.active = False
    numOfPlayers -= 1

#clients = []
#usernames = []
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
##########################################################################################/////////
# import socket
# import threading
#
# IP = '10.1.0.110'
# PORT = 5555
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((IP, PORT))
#
# server.listen()
#
# clients = []
# usernames = []
#
# def broadcast(msg):
#     for client in clients:
#         client.send(msg)
# def handle(client):
#     while True:
#         try:
#             msg = client.recv(1024)
#             print(f"{usernames[clients.index(client)]} says {msg}")
#             broadcast(msg)
#         except:#el client crashed aw maba2ash fi connection
#             index = clients.index(client)
#             clients.remove(client) #ba remove el client w a-close el connection
#             client.close()
#             user=usernames[index]
#             usernames.remove(user)
#             break
#
#
# def receive():
#     while True:
#         client, address =server.accept()
#         print(f"connected with {str(address)}!")
#
#         client.send("NICK".encode('utf-8'))
#         username = client.recv(1024)
#
#         usernames.append(username)
#         clients.append(client)
#
#         print(f"Username of client {username}")
#         broadcast(f"user 1 connected to the server! \n" .encode('utf-8'))
#         client.send("Connected to the server".encode('utf-8'))
#
#         thread=threading.Thread(target=handle,args=(client,))
#         thread.start()
#
#
# print("server running ....")
# receive()