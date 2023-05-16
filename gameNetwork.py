import socket
import pickle
from network import Network
from chat import Client

class GameNetwork:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.1.0.110"
        self.port = 9090
        self.addr = (self.server, self.port)
        self.port1, self.port2 = self.connect()

    def connect(self):
        try:
            print("connect mariooooo")
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass
    def startTheGame(self):
        n = Network(self.port1)
        client = Client(self.port2)
        return n, client