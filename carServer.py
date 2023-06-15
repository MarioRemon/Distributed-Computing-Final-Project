import socket
from _thread import *

from bson import ObjectId

from ip import *

import mongo as mongo

from player import Player
from pymongo import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
import pickle
from ip import *
server = ip
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

uri = "mongodb+srv://Mario:123@cluster0.msy4ut4.mongodb.net/?retryWrites=true&w=majority"
###uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.9.1"
#client = ReplicaSetConnection('172.31.25.155:27017', replicaSet='replica_demo')
#Create a new client and connect to the server
#client = MongoClient()
#client = MongoClient('mongodb://mario:123@54.167.45.206:27017/test?replicaSet=replica_demo&w=majority', server_api=ServerApi('1'))
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
activity = []
def threaded_client(conn, playerId):
    player = Player(playerId, '', '(0, 0)', 0, 0, 0, len(players), 0, 0)
    newPos = [[playerId, '(0, 0)']]
    mapScore = [[playerId, 1, 2]]
    rankPlayers.append(mapScore)
    namo = [[playerId, '']]
    playersName.append(namo)
    positionOfPlayers.append(newPos)
    activity.append([playerId, True])
    rankPlayers[playerId][0][1] = 5
    players.append(player)
    global numOfPlayers
    numOfPlayers += 1
    conn.send(pickle.dumps(players[playerId]))
    reply = ""
    reply1 = []

    try:
        mydb = client['Car_Racing_Car']
        data = mydb['game']
        if(data.count_documents({}) > 0):
            #data = mydb.game
            lastGame = data.find().sort([('time', -1)]).limit(1)
            last_game = lastGame.next()
            if int(last_game['numberOfPlayers']) < 8:
                print('less than 8 players')
                recordUpdate = {
                    'numberOfPlayers': numOfPlayers,
                }
                recordInsert = {
                    'players': {
                            'id': player.id,
                            'userName': player.userName,
                            'position': player.position,
                            # 'x_coordinate': player.x,
                            # 'y_coordinate': player.y,
                            'mapComplete': player.mapComplete,
                            'active': player.active,
                            'score': player.score,
                    }
                }
                data.update_many({'GameId': last_game['GameId']}, {"$set": recordUpdate})
                print('1')
                data.update_many({'GameId': last_game['GameId']}, {"$addToSet": recordInsert})
                print('2')
            else:
                print('more than 8 players')
                record = {
                    'GameId': 1,#int(last_game['GameId']) + 1,
                    'server': 1, # if int(last_game['server']) == 1 else 2,
                    'time': time.ctime(),
                    'numberOfPlayers': numOfPlayers,
                    'chatOfTheGame': '',
                    'players': [{
                        'id': player.id,
                        'userName': player.userName,
                        'position': player.position,
                        # 'x_coordinate': player.x,
                        # 'y_coordinate': player.y,
                        'mapComplete': player.mapComplete,
                        'active': player.active,
                        'score': player.score,
                    }]
                }
                data.insert_one(record)
        else:
            print('No Previous Database')
            record = {
                'GameId': 1,  # int(last_game['GameId']) + 1,
                'server': 1,  # if int(last_game['server']) == 1 else 2,
                'time': time.ctime(),
                'numberOfPlayers': numOfPlayers,
                'chatOfTheGame': '',
                'players': [{
                    'id': player.id,
                    'userName': player.userName,
                    'position': player.position,
                    # 'x_coordinate': player.x,
                    # 'y_coordinate': player.y,
                    'mapComplete': player.mapComplete,
                    'active': player.active,
                    'score': player.score,
                }]
            }
            data.insert_one(record)
    except:
        print('error')
    dbTime = 0
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            print('Data Received')
            dbTime += 1

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
                    sorted_rankPlayers = sorted(rankPlayers, key=lambda x: x[0][2], reverse=True)
                    newSorted = []
                    for item in sorted_rankPlayers:
                        newSorted.append(playersName[item[0][0]])

                    conn.send(pickle.dumps(newSorted))
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
                    player.position = clientRequest[1]
                    conn.send(pickle.dumps(positionOfPlayers))
                    print("Received: ", data)
                    print("Sending : ", reply1)
                elif clientRequest[0] == '5':
                    playersName[playerId] = clientRequest[1]
                    player.userName = clientRequest[1]
                elif clientRequest[0] == '6':
                    conn.send(pickle.dumps(activity))
                elif clientRequest[0] == '7':
                    if(clientRequest[1] == 'True'):
                        player.active = True
                        activity[playerId][1] = True
                    else:
                        player.active = False
                        activity[playerId][1] = False
                    print('updaaaaaaaaate')
                    print(bool(clientRequest[1]))
                    print(activity[playerId][1])
            if (dbTime % 1500) == 0:
                mydb = client['Car_Racing_Car']
                data = mydb['game']
                # data = mydb.game
                lastGame = data.find().sort([('time', -1)]).limit(1)
                last_game = lastGame.next()
                recordUpdate = {
                    'numberOfPlayers': numOfPlayers,
                }
                data.update_one({'GameId': last_game['GameId']}, {"$set": recordUpdate})
                update = {"$set":{f"players.{player.id}.userName": player.userName,
                          f"players.{player.id}.position": player.position,
                          f"players.{player.id}.score": player.score,
                          f"players.{player.id}.mapComplete": player.mapComplete}
                }
                data.update_one({"_id": ObjectId(last_game['_id'])}, update)
                print('passed')
        except:
            print('error')
            break
    print("Lost connection")
    conn.close()
    player.active = False
    activity[playerId][1] = False
    numOfPlayers -= 1
    mydb = client['Car_Racing_Car']
    data = mydb['game']
    # data = mydb.game
    lastGame = data.find().sort([('time', -1)]).limit(1)
    last_game = lastGame.next()
    recordUpdate = {
        'numberOfPlayers': numOfPlayers,
    }
    data.update_one({'GameId': last_game['GameId']}, {"$set": recordUpdate})
    update = {"$set": {f"players.{player.id}.position": player.position,
                       f"players.{player.id}.score": player.score,
                       f"players.{player.id}.mapComplete": player.mapComplete,
                       f"players.{player.id}.active": player.active}
              }
    data.update_one({"_id": ObjectId(last_game['_id'])}, update)
    print('passed')
currentPlayer = 0
#connectDb()
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1