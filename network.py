import socket
import pickle
from ip import *

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

class Network:
    def __init__(self, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.id = self.connect()
        self.getMyNumberId = self.getMyNumberId()

    def getId(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            #print(pickle.loads(self.client.recv(2048)))
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def getMyNumberId(self):
        try:
            self.client.send(pickle.dumps('4:'))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("error")
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(str(data) + ':'))
            return pickle.loads(self.client.recv(2048))
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
    def getUpdateMapComplete(self, mapComplete, score):
        try:
            self.client.send(pickle.dumps('2:' + str(mapComplete) + ':' + str(score)))  # + str(Pos)))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("error")
            print(e)

    def getOtherPlayersPos(self, Pos):
        try:
            self.client.send(pickle.dumps('3:' + str(Pos)))
            return pickle.loads(self.client.recv(2048 * 16))
        except socket.error as e:
            print("error")
            print(e)

    def sendPlayerName(self, playerName):
        try:
            self.client.send(pickle.dumps('5:' + str(playerName)))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("error")
            print(e)

    def getIsActive(self):
        try:
            self.client.send(pickle.dumps('6:'))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("error")
            print(e)

    def sendMyActivity(self, active):
        try:
            self.client.send(pickle.dumps('7:' + str(active)))
        except socket.error as e:
            print("error")
            print(e)