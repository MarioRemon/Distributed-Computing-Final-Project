from network import Network
from chat import Client
from chatty import *

class GameNetwork:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'ec2-13-51-176-3.eu-north-1.compute.amazonaws.com'
        self.port = 9090
        self.addr = (self.server, self.port)
        self.port1, self.port2, self.carServerIp, self.chattingServerIp = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass
    def startTheGame(self):
        n = Network(self.port1, self.carServerIp)
        return n
    def startChat(self, userName):
        client = Client(self.port2, userName, self.chattingServerIp)
        return client

    def startChatty(self, playerName):
        chat = Chat(playerName, self.chattingServerIp)
        return chat