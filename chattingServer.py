import socket
import threading
import pickle
from ip import *
import socket
from _thread import *
from bson import ObjectId
from ip import *
import mongo as mongo
from player import Player
from pymongo import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pickle


IP = ip
PORT = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

server.listen()

clients = []
usernames = []

uri = "mongodb+srv://Mario:123@cluster0.msy4ut4.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
   client.admin.command('ping')
   print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
   print(e)

Message = ''
count = 0
def broadcast(msg):
    global Message
    global count
    global client
    for cliento in clients:
        #client.send(msg)
        cliento.sendall(pickle.dumps(msg))
    print(msg)
    Message += msg
    count += 1
    if count % 5 == 0:
        try:
            mydb = client['Car_Racing_Car']
            data = mydb['game']
            lastGame = data.find().sort([('time', -1)]).limit(1)
            last_game = lastGame.next()
            recordUpdate = {
                'chatOfTheGame': Message,
            }
            data.update_many({'GameId': last_game['GameId']}, {"$set": recordUpdate})
            count = 0
            Message = ''
        except:
            print('error')
def handle(client):
    while True:
        try:
            #msg = client.recv(1024)
            msg = pickle.loads(client.recv(2048))
            #print(usernames[clients.index(client)] + 'says'+ {msg})
            broadcast(msg)
        except:                                 #el client crashed aw maba2ash fi connection
            index = clients.index(client)
            clients.remove(client)              #ba remove el client w a-close el connection
            client.close()
            user = usernames[index]
            usernames.remove(user)
            print('bazt')
            break


def receive():
    while True:
        client, address = server.accept()
        print('connected with'+str(address))
        client.sendall(pickle.dumps('NICK'))
        #client.send("NICK")#.encode('utf-8'))
        #username = client.recv(1024)
        username = pickle.loads(client.recv(2048))
        usernames.append(username)
        clients.append(client)

        #print(f"Username of client {username}")
        #broadcast(f"user 1 connected to the server! \n" )#.encode('utf-8'))
        broadcast("A user connected to the server!")
        #client.send("Connected to the server")#.encode('utf-8'))
        client.sendall(pickle.dumps("Connected to the server"))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server running ....")
receive()