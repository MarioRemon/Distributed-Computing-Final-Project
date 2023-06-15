import socket
import threading
import tkinter
import tkinter.scrolledtext

import cargame
from ip import *
import pickle
from tkinter import simpledialog
from cargame import *
IP = ip
PORT = 4444


class Chat:
    oldUser = False
    #global received_a_message
    #message = ''
    #count = 0

    def __init__(self, userName):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = IP
        self.userName = userName
        self.sock.connect((ip, PORT))
        self.running = True
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        #conn.sendall(pickle.dumps(numOfPlayers))

    def write(self, msg):
        #msg = f"{self.username}:{self.input_area.get('1.0', 'end')}"
        # self.message += msg
        try:
            self.sock.sendall(pickle.dumps(msg))
        except:
            print('no write')
        #self.sock.send(msg)#.encode('utf-8'))
        #self.input_area.delete('1.0', 'end')


    def receive(self):
        global chat_messages
        while self.running:
            try:
                 msg = pickle.loads(self.sock.recv(2048))
                 # msg = self.sock.recv(1024).decode('utf-8')
                 if msg == 'NICK':
                     self.sock.sendall(pickle.dumps(self.userName))
                     #self.sock.send(str(self.username))#.encode('utf-8'))
                 else:
                     print('ccccccccccccccccccccccccccccccccccccccccccc')
                     cargame.chat_messages = msg
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break
