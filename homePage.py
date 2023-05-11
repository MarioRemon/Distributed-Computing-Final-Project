from tkinter import *
from cargame import CarRacing

class HomePage:

    def __init__(self):
        self.root = Tk()     # create a root widget
        self.root.title("Super Racing Car")
        self.root.configure(background="Blue")
        self.root.maxsize(800, 600)
        self.root.geometry("300x300+50+50")  # width x height + x + y
        self.welcomeText = Label(self.root, text="Welcome to our Super Racing Game")
        self.welcomeText.pack()
        self.userNameLabel = Label(self.root, text="UserName")
        self.userNameLabel.pack()

        self.userName = Entry(self.root, width=50, borderwidth=5)
        self.userName.insert(0, "Enter Your UserName")
        self.userName.bind("<FocusIn>", self.temp_text)
        self.userName.pack()
        self.startGameButton = Button(self.root, text="Start", command=self.startGame)
        self.startGameButton.pack()
        self.root.mainloop()
    def startGame(self):
        playerName = self.userName.get()
        self.root.destroy()
        car_racing = CarRacing()
        car_racing.racing_window(playerName)

    def temp_text(self, e):
        self.userName.delete(0, "end")