import socket
from _thread import *

import mongo as mongo

from player import Player
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
import pickle

server = "192.168.1.11"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

uri = "mongodb+srv://Mario:123@cluster0.msy4ut4.mongodb.net/?retryWrites=true&w=majority"
#Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
#Send a ping to confirm a successful connection
try:
   client.admin.command('ping')
   print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
   print(e)


#players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]
players = []
numOfPlayers = 0
rank = [[]]
rankPlayers = []
rankPlayers1 = []
positionOfPlayers = []
first3Rankers = []
playersName = []
def threaded_client(conn, playerId):
    player = Player(playerId, '', 0, 0, 0, 0, 0, len(players), 0, 0)
    newPos = [[playerId, '(0, 0)']]
    mapScore = [[playerId, 1, 2]]
    rankPlayers.append(mapScore)
    namo = [[playerId, '']]
    playersName.append(namo)
    positionOfPlayers.append(newPos)
    rankPlayers[playerId][0][1] = 5
    players.append(player)
    global numOfPlayers
    numOfPlayers += 1
    conn.send(pickle.dumps(players[playerId]))
    reply = ""
    reply1 = []


    try:
        mydb = client['Car_Racing_Car']
        print('1')
        data = mydb.game
        print('2')
        lastGame = mydb.game.find().sort([('time', -1)]).limit(1)
        print('3333333333333333333333333333333')
        if int(lastGame.next()['server']) == 2:# and int(lastGame.next()['numberOfPlayers']) <= 8:
            print('5555555555555')
            myquery = {'GameId': lastGame.next()['GameId']}
            print('6666666666666666666666666666666')
            #record = {
            #    'numberofPlayers': 10,#numOfPlayers,
                # '$push': {
                #     'players': {
                #         'id': player.id,
                #         'userName': player.userName,
                #         'x_coordinate': player.x,
                #         'y_coordinate': player.y,
                #         'mapComplete': player.mapComplete,
                #         'active': player.active,
                #         'score': player.score,
                # }
                # }
            #}
            #data.update_many(myquery, record)

        print('4')
        # record = {
        #     'GameId': '',
        #     'server': 2,
        #     'time': time.ctime(),
        #     'numberOfPlayers': numOfPlayers,
        #     'players': [{
        #         'id': player.id,
        #         'userName': player.userName,
        #         'x_coordinate': player.x,
        #         'y_coordinate': player.y,
        #         'mapComplete': player.mapComplete,
        #         'active': player.active,
        #         'score': player.score,
        #     }]
        # }
        #data.insert_one(record)
    except:
        print('error')


    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print('Data Received')
            print(data)

            if not data:
                print("Disconnected")
                break
            else:
                clientRequest = data.split(':', 2)
                print(clientRequest)
                if clientRequest[0] == '0':
                    conn.sendall(pickle.dumps(numOfPlayers))
                    print(len(players))
                elif clientRequest[0] == '1':
                    # rankPlayers.sort(key=lambda x: [1], reverse=True)
                    # first3Rankers.clear()
                    # for i in rankPlayers:
                    #     first3Rankers.append(i[0][0])
                    # newList = []
                    # for x in first3Rankers:
                    #     newList.append(playersName[x])
                    #     conn.send(pickle.dumps(newList))
                    conn.send(pickle.dumps('1'))
                elif clientRequest[0] == '2':
                        player.mapComplete = clientRequest[1]
                        player.score = clientRequest[2]
                        rankPlayers[playerId][0][1] = float(clientRequest[1])
                        rankPlayers[playerId][0][2] = float(clientRequest[2])
                        conn.send(pickle.dumps(rankPlayers))
                elif clientRequest[0] == '4':
                    conn.sendall(pickle.dumps(playerId))
                elif clientRequest[0] == '3':
                    positionOfPlayers[playerId][0][1] = clientRequest[1]
                    conn.send(pickle.dumps(positionOfPlayers))
                    print("Received: ", data)
                    print("Sending : ", reply1)
                elif clientRequest[0] == '5':
                    playersName[playerId] = clientRequest[1]
        except:
            break
    print("Lost connection")
    conn.close()
    player.active = False
    numOfPlayers -= 1

currentPlayer = 0
#connectDb()
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1