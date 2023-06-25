import threading
import socket
from pymongo.mongo_client import MongoClient
import pickle


IP = 'ec2-13-48-24-217.eu-north-1.compute.amazonaws.com'
PORT = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

server.listen()

clients = []
usernames = []


#Send a ping to confirm a successful connection
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

Message = ''
count = 0
def broadcast(msg):
    global Message
    global count
    global client
    for cliento in clients:
        cliento.sendall(pickle.dumps(msg))
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
            msg = pickle.loads(client.recv(2048))
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
        username = pickle.loads(client.recv(2048))
        usernames.append(username)
        clients.append(client)

        broadcast("A user connected to the server!")
        client.sendall(pickle.dumps("Connected to the server"))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server running ....")
receive()