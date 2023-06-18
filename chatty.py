import socket
import threading
import cargame
from ip import *
import pickle
from cargame import *
IP = ip
PORT = 4444


class Chat:
    oldUser = False

    def __init__(self, userName):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = IP
        self.userName = userName
        self.sock.connect((ip, PORT))
        self.running = True
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def write(self, msg):
        try:
            self.sock.sendall(pickle.dumps(msg))
        except:
            print('no write')

    def receive(self):
        global chat_messages
        while self.running:
            try:
                 msg = pickle.loads(self.sock.recv(2048))
                 if msg == 'NICK':
                     self.sock.sendall(pickle.dumps(self.userName))
                 else:
                     cargame.chat_messages = msg
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break
