import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

#IP = '10.1.0.110'
#PORT = 4444


class Client:

    def __init__(self, port):
        ip = '10.1.0.110'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

        msg = tkinter.Tk()
        msg.withdraw()


        self.username = simpledialog.askstring("Username:", "enter username", parent=msg)
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()
    #GUI
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="purple")
        self.win.title('chatting')

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="purple",fg="white")
        self.chat_label.config(font=("Arial", 16,))
        self.chat_label.pack(side=tkinter.TOP, anchor='w', pady =5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win,width=20,height=10)
        self.text_area.pack(anchor='w',padx=5,pady =5)
        self.text_area.config(state='disabled')  # user not be able to add text to text area

        self.input_area = tkinter.Text(self.win, width=10,height=3,bg="light yellow",wrap="word")
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        msg = f"{self.username}:{self.input_area.get('1.0', 'end')}"
        self.sock.send(msg.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                print('superrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
                msg = self.sock.recv(1024).decode('utf-8')
                print('malooooooooooooooooooooooooookaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!')
                if msg == 'NICK':
                    print('mariooooooooooooooooooooooooooooooooo')
                    self.sock.send(self.username.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', msg)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')


            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break


#client = Client(IP, PORT)