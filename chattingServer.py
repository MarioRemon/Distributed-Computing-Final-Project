import socket
import threading

IP = '10.1.0.110'
PORT = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))

server.listen()

clients = []
usernames = []

def broadcast(msg):
    for client in clients:
        client.send(msg)
def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            print(f"{usernames[clients.index(client)]} says {msg}")
            broadcast(msg)
        except:#el client crashed aw maba2ash fi connection
            index = clients.index(client)
            clients.remove(client) #ba remove el client w a-close el connection
            client.close()
            user=usernames[index]
            usernames.remove(user)
            break


def receive():
    while True:
        client, address =server.accept()
        print(f"connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        username = client.recv(1024)

        usernames.append(username)
        clients.append(client)

        print(f"Username of client {username}")
        broadcast(f"user 1 connected to the server! \n" .encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()


print("server running ....")
receive()