import socket
from _thread import *
from player import Player
from pymongo import MongoClient
import time
import pickle
server = 'ec2-16-16-65-120.eu-north-1.compute.amazonaws.com'
port = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

# Send a ping to confirm a successful connection
uri = ''
primary = False
replica1 = False
replica2 = False

#Send a ping to confirm a successful connection
try:
    client = MongoClient('ec2-54-227-79-72.compute-1.amazonaws.com', 27017)
    print(client.is_mongos)
    primary = True
except Exception as e:
    primary = False
try:
    client = MongoClient('ec2-3-94-169-95.compute-1.amazonaws.com', 27017)
    print(client.is_mongos)
    replica1 = True
except Exception as e:
    replica1 = False
try:
    client = MongoClient('ec2-54-237-235-219.compute-1.amazonaws.com', 27017)
    print(client.is_mongos)
    replica2 = True
except Exception as e:
    replica2 = False

if primary:  #primary db
    client = MongoClient('ec2-54-227-79-72.compute-1.amazonaws.com', 27017)
    uri = 'ec2-54-227-79-72.compute-1.amazonaws.com'
elif replica1:
    client = MongoClient('ec2-3-94-169-95.compute-1.amazonaws.com', 27017)
    uri = 'ec2-3-94-169-95.compute-1.amazonaws.com'
elif replica2:
    client = MongoClient('ec2-54-237-235-219.compute-1.amazonaws.com', 27017)
    uri = 'ec2-54-237-235-219.compute-1.amazonaws.com'

try:
   client.admin.command('ping')
   print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
   print(e)


players = []
numOfPlayers = 0
rankPlayers = []
positionOfPlayers = []
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

    try:
        mydb = client['Car_Racing_Car']
        data = mydb['game']
        if(data.count_documents({}) > 0):
            lastGame = data.find().sort([('time', -1)]).limit(1)
            last_game = lastGame.next()
            if int(last_game['numberOfPlayers']) < 8:
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
                data.update_many({'GameId': last_game['GameId']}, {"$addToSet": recordInsert})
            else:
                record = {
                    'GameId': int(last_game['GameId']) + 1,
                    'server': 2,    # if int(last_game['server']) == 1 else 2,
                    'time': time.ctime(),
                    'numberOfPlayers': numOfPlayers,
                    'chatOfTheGame': '',
                    'players': [{
                        'id': player.id,
                        'userName': player.userName,
                        'position': player.position,
                        'mapComplete': player.mapComplete,
                        'active': player.active,
                        'score': player.score,
                    }]
                }
                data.insert_one(record)
        else:
            record = {
                'GameId': 1,
                'server': 2,  # if int(last_game['server']) == 1 else 2,
                'time': time.ctime(),
                'numberOfPlayers': numOfPlayers,
                'chatOfTheGame': '',
                'players': [{
                    'id': player.id,
                    'userName': player.userName,
                    'position': player.position,
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
            dbTime += 1

            if not data:
                print("Disconnected")
                break
            else:
                clientRequest = data.split(':', 2)
                if clientRequest[0] == '0':
                    conn.sendall(pickle.dumps(numOfPlayers))
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
                elif clientRequest[0] == '5':
                    playersName[playerId] = clientRequest[1]
                    player.userName = clientRequest[1]
                    mydb = client['Car_Racing_Car']
                    data = mydb['game']
                    lastGame = data.find().sort([('time', -1)]).limit(1)
                    g = lastGame.next()
                    if g['numberOfPlayers'] == 1:
                        lastGame = data.find().sort([('time', -1)]).limit(2)
                        indexOfGame = 0
                        found = False
                        for game in lastGame:
                            indexOfGame += 1
                            # Check if the 'players' field exists in the document
                            if 'players' in game and indexOfGame == 1:
                                # Access the 'players' array
                                mongoPlayers = game['players']
                                # Search for the specific username within the 'players' array
                                for onePlayer in mongoPlayers:
                                    # Check if the specific username exists in the player object
                                    if player.userName == onePlayer['userName']:
                                        # Perform any actions you want with the document
                                        found = True
                                        player.id = int(onePlayer['id'])
                                        player.position = onePlayer['position']
                                        player.mapComplete = onePlayer['mapComplete']
                                        player.score = onePlayer['score']
                                        break
                            if found and indexOfGame == 2:
                                data.delete_one(game)
                    else:
                        if 'players' in g:
                            # Access the 'players' array
                            mongoPlayers = g['players']
                            # Search for the specific username within the 'players' array
                            for onePlayer in mongoPlayers:
                                # Check if the specific username exists in the player object
                                if player.userName == onePlayer['userName']:
                                    # Perform any actions you want with the document
                                    # delete the new player created
                                    query = {
                                        '_id': (g['_id'])
                                    }
                                    # Define the update operation using $pull
                                    update = {
                                        '$pull': {
                                            'players': {
                                                'id': player.id
                                            }
                                        }
                                    }
                                    data.update_one(query, update)
                                    player.id = onePlayer['id']
                                    player.position = onePlayer['position']
                                    player.mapComplete = onePlayer['mapComplete']
                                    player.score = onePlayer['score']
                                    break
                    dataToSend = '1:' + str(player.id) + ':' + str(player.position) + ':' + str(player.mapComplete) + ':' + str(player.score)
                    conn.send(pickle.dumps(dataToSend))
                elif clientRequest[0] == '6':
                    conn.send(pickle.dumps(activity))
                elif clientRequest[0] == '7':
                    if(clientRequest[1] == 'True'):
                        player.active = True
                        activity[playerId][1] = True
                    else:
                        player.active = False
                        activity[playerId][1] = False
            if (dbTime % 1500) == 0:
                mydb = client['Car_Racing_Car']
                data = mydb['game']
                lastGame = data.find().sort([('time', -1)]).limit(1)
                last_game = lastGame.next()
                recordUpdate = {
                    'numberOfPlayers': numOfPlayers,
                }
                data.update_one({'GameId': last_game['GameId']}, {"$set": recordUpdate})
                update = {"$set": {f"players.{player.id}.id": player.id,
                                   f"players.{player.id}.userName": player.userName,
                                   f"players.{player.id}.position": player.position,
                                   f"players.{player.id}.score": player.score,
                                   f"players.{player.id}.mapComplete": player.mapComplete,
                                   f"players.{player.id}.active": player.active}
                          }
                data.update_one({"_id": (last_game['_id'])}, update)
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
    lastGame = data.find().sort([('time', -1)]).limit(1)
    last_game = lastGame.next()
    recordUpdate = {
        'numberOfPlayers': numOfPlayers,
    }
    data.update_one({'GameId': last_game['GameId']}, {"$set": recordUpdate})
    update = {"$set": {f"players.{player.id}.id": player.id,
                       f"players.{player.id}.userName": player.userName,
                       f"players.{player.id}.position": player.position,
                       f"players.{player.id}.score": player.score,
                       f"players.{player.id}.mapComplete": player.mapComplete,
                       f"players.{player.id}.active": player.active}
              }
    data.update_one({"_id": last_game['_id']}, update)
currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1