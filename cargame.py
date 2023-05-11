import random
from time import sleep
from network import Network
from player import Player
import pygame

class CarRacing:
    def __init__(self):

        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.initialize()

    def initialize(self):

        self.crashed = False

        self.carImg = pygame.image.load('.\\img\\car.png')
        self.car_x_coordinate = (self.display_width * 0.47)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car_position = [((self.display_width * 0.47) - 80), (self.display_width * 0.47), ((self.display_width * 0.47) + 80) ]
        self.enemy_car = pygame.image.load('.\\img\\enemy_car_1.png')
        #self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_startx =  random.choice(self.enemy_car_position) #((self.display_width * 0.47) - 100)#random.choice(enemy_car_position)
        self.enemy_car_starty = -600#(self.display_height * 0.8) #-600
        self.enemy_car_speed = 3
        self.enemy_car_width = 49
        self.enemy_car_height = 98

        # Background
        self.bgImg = pygame.image.load(".\\img\\back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self, playerName):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Super Racing Car')
        self.run_car(playerName)


    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
        sleep(1)
        self.initialize()
        self.racing_window(None)

    def back_ground_raod(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def playerName(self, playerName):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Player Name: " + str(playerName), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def mapCompletePerecentage(self, percent):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Complete : " + str(percent), True, self.white)
        self.gameDisplay.blit(text, (0, 20))

    def playersNumber(self, number):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Players Number : " + str(number), True, self.white)
        self.gameDisplay.blit(text, (0, 40))

    def highscore(self, count):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (0, 60))

    def rankers(self, rankers):
        font = pygame.font.SysFont("arial", 20)
        text = font.render(str(rankers[0]), True, self.white)
        self.gameDisplay.blit(text, (0, 80))
        text = font.render(str(rankers[1]), True, self.white)
        self.gameDisplay.blit(text, (0, 100))
        text = font.render(str(rankers[2]), True, self.white)
        self.gameDisplay.blit(text, (0, 120))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (600, 520))

    def run_enemy_car(self, thingx, thingy):
       self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def run_car(self, playerName):
        network = Network() #initliazed connection to server
        #mafrod a receive ana rkm kam mn el network w ahotha fi class el player
        player = Player(network.getId(), playerName, self.car_x_coordinate, self.car_y_coordinate, self.car_width, 100, 'Blue', 0, 0)
        print(player.mapComplete)
        print("/////////////////////////////////////////////////////////////////")
        while not self.crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        self.car_x_coordinate -= 80

                        #send("x position for car here")
                        print("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car_x_coordinate += 80

                        #send("x position for car here")
                        print ("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    print ("x: {x}, y: {y}".format(x=self.car_x_coordinate, y=self.car_y_coordinate))
                    #network.send((self.car_x_coordinate, self.car_y_coordinate))
                    if(event.key == pygame.K_UP and self.bg_speed < 15.0):
                        self.bg_speed = self.bg_speed + 0.15
                        print('increase')
                        print(self.bg_speed)

                    if(event.key == pygame.K_DOWN and self.bg_speed > 2.0):
                        self.bg_speed -= 0.15
                        print('decrease bmzagy')
            self.gameDisplay.fill(self.black)
            self.back_ground_raod()
            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
               self.enemy_car_starty = 0 - self.enemy_car_height
               #self.enemy_car_startx = random.randrange(310, 450)
               self.enemy_car_startx = random.choice(self.enemy_car_position)
            network.getUpdateMapComplete('20')
            #print(player.mapComplete)
            print("/////////////////////////////////////////////////////////////////")
            #print(network.getOtherPlayersPos((self.car_x_coordinate, self.car_y_coordinate)))
            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.playerName(playerName)
            self.mapCompletePerecentage(player.id)
            self.playersNumber(network.getNumberOfPlayers())
            self.highscore(self.count)
            self.rankers(network.getGameRankers())
            self.count += 1
            #if (self.count % 100 == 0):
                #self.enemy_car_speed += 1
                #self.bg_speed += 1
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")
                    print("OVERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")

            if self.car_x_coordinate < 290 or self.car_x_coordinate > 460:
                self.crashed = True
                self.display_message("Game Over !!!")

            pygame.display.update()
            self.clock.tick(60)
#if __name__ == '__main__':
#    car_racing = CarRacing()
#    car_racing.racing_window()
