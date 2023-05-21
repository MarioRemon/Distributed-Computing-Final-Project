import socket
import pickle


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

class Network:
    def __init__(self):
        print("init")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.1.0.210"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print("id")
        print(self.id)

    def getId(self):
        print("get id")
        print(self.id)
        return self.id

    def connect(self):
        try:
            print("connect mariooooo")
            self.client.connect(self.addr)
            #print(pickle.loads(self.client.recv(2048)))
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    # # Function to send car position update to the server
    # def send_position_update(position):
    #     update = pickle.dumps(position)  # Serialize the position data
    #     client_socket.sendall(update)
    #
    # # Continuously update the car position and send updates to the server
    # while True:
    #     # Update the car position (replace this with your own logic)
    #     car_position = (x, y)  # Example position data
    #
    #     # Send the position update to the server
    #     send_position_update(car_position)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(str(data) + ':'))
            return pickle.loads(self.client.recv(2048))
            #self.client.send(str.encode(str(data))) #("Amirtyyyyyyyyyyy")) #make_pos(data)
            #return self.client.recv(2048).decode()
        except socket.error as e:
            print("error")
            print(e)

    def getNumberOfPlayers(self):
        try:
            return self.send(0)
        except socket.error as e:
            print(e)

    def getGameRankers(self):
        try:
            return self.send(1)
        except socket.error as e:
            print(e)
    def getUpdateMapComplete(self, mapComplete):
        try:
            print("d5l map")
            self.client.send(pickle.dumps('2:' + str(mapComplete)))  # + str(Pos)))
            return pickle.loads(self.client.recv(2048))
            # self.client.send(str.encode(str(data))) #("Amirtyyyyyyyyyyy")) #make_pos(data)
            # return self.client.recv(2048).decode()
        except socket.error as e:
            print("error")
            print(e)

    def getOtherPlayersPos(self, Pos):
        try:
            self.client.send(pickle.dumps('3:'))# + str(Pos)))
            return pickle.loads(self.client.recv(2048))
            # self.client.send(str.encode(str(data))) #("Amirtyyyyyyyyyyy")) #make_pos(data)
            # return self.client.recv(2048).decode()
        except socket.error as e:
            print("error")
            print(e)