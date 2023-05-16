import random
import socket
from time import sleep
from network import Network
from player import Player
import pygame
from button import Button
import sys
import time
from obstacles import Tree
from obstacles import Pr
from obstacles import Raindrop
from obstacles import FinishLine
# from MainMenu import MainMenu

#define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255,255,255)
grey = (211,211,211)

clock = pygame.time.Clock()
FPS = 10


class CarRacing:
    def __init__(self):

        pygame.init()

        self.is_raining = False
        self.rain_particles = []

        self.display_width = 800
        self.display_height = 700
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.bg = (204, 102, 0)
        self.red = (255, 0, 0)
        self.grey = (211, 211, 211)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.font = pygame.font.Font(None, 64)

        self.initialize()

    def initialize(self):


        self.crashed = False

        self.carImg = pygame.image.load('Img/cars/1.png')
        self.carImg = pygame.transform.scale(self.carImg, (80,120))
        self.car_x_coordinate = 300
        self.car_y_coordinate = 550
        self.car_width = 49
        self.car_rect = self.carImg.get_rect()
        self.car_rect.y = 0

        self.is_running = True
        self.is_paused = False


        # Background
        self.gardenBrown = pygame.image.load("Img/bg.png")
        self.gardenBrown = pygame.transform.scale(self.gardenBrown, (self.display_width, self.display_height))
        self.bgImg = pygame.image.load("Img/road.png")
        self.bgImg = pygame.transform.scale(self.bgImg, (self.display_width -220, self.display_height))
        self.BG = pygame.image.load("Img/intro.jpg")
        self.BG = pygame.transform.scale(self.BG, (self.display_width, self.display_height))
        self.bg_x1 = (self.display_width / 2) - (800 / 2)
        self.bg_x2 = (self.display_width / 2) - (800 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 10
        self.count = 0

        self.tree_group = pygame.sprite.Group()
        self.Pr_group = pygame.sprite.Group()

        #Finish Line
        self.finish_line_image_path = "finish_line.png"
        self.finish_line_width = 165
        self.finish_line_height = 50
        self.finish_line_x = self.display_width // 2
        self.finish_line_y = 100

        self.finish_line = FinishLine(self.finish_line_x, self.finish_line_y, self.finish_line_image_path)


    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("Img/font.ttf", size)

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Super Racing Car')
        self.main_menu()
        # self.run_car(playerName)

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

    ###### Countdown ######
    def countdown(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        font2 = pygame.font.Font('freesansbold.ttf', 85)
        three = font2.render('3', True, (187, 30, 16))
        two = font2.render('2', True, (255, 255, 0))
        one = font2.render('1', True, (51, 165, 50))
        go = font2.render('GO!!!', True, (0, 255, 0))

        ##### displaying blank background #####

        self.gameDisplay.blit(self.gardenBrown, (0, 0))
        self.gameDisplay.blit(self.bgImg, (self.bg_x1 + 120, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2 + 120, self.bg_y2))
        pygame.display.update()


        ###### Displaying  three (3) ######
        self.gameDisplay.blit(three, (350, 250))
        pygame.display.update()
        time.sleep(1)


        ##### displaying blank background #####
        self.gameDisplay.blit(self.gardenBrown, (0, 0))
        self.gameDisplay.blit(self.bgImg, (self.bg_x1 + 120, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2 + 120, self.bg_y2))
        pygame.display.update()
        time.sleep(1)

        ###### Displaying  two (2) ######
        self.gameDisplay.blit(two, (350, 250))
        pygame.display.update()
        time.sleep(1)

        ##### displaying blank background #####
        self.gameDisplay.blit(self.gardenBrown, (0, 0))
        self.gameDisplay.blit(self.bgImg, (self.bg_x1 + 120, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2 + 120, self.bg_y2))
        pygame.display.update()
        time.sleep(1)

        ###### Displaying  one (1) ######
        self.gameDisplay.blit(one, (350, 250))
        pygame.display.update()
        time.sleep(1)

        ##### displaying blank background #####
        self.gameDisplay.blit(self.gardenBrown, (0, 0))
        self.gameDisplay.blit(self.bgImg, (self.bg_x1 + 120, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2 + 120, self.bg_y2))
        pygame.display.update()
        #time.sleep(1)

        ###### Displaying  Go!!! ######
        self.gameDisplay.blit(go, (300, 250))
        pygame.display.update()
        time.sleep(1)
        self.run_car(self.playerName)
        # calling the gameloop so that our game can start after the countdown
        pygame.display.update()



    def back_ground_raod(self):
        self.gameDisplay.blit(self.gardenBrown, (0, 0))
        self.gameDisplay.blit(self.bgImg, (self.bg_x1 + 120, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2 + 120, self.bg_y2))

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

    # def rankers(self, rankers):
    #     font = pygame.font.SysFont("arial", 20)
    #     text = font.render(str(rankers[0]), True, self.white)
    #     self.gameDisplay.blit(text, (0, 80))
    #     text = font.render(str(rankers[1]), True, self.white)
    #     self.gameDisplay.blit(text, (0, 100))
    #     text = font.render(str(rankers[2]), True, self.white)
    #     self.gameDisplay.blit(text, (0, 120))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (600, 520))

    def main_menu(self):

        while not self.crashed:

            self.gameDisplay.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(50).render("MAIN MENU", True, white)
            MENU_RECT = MENU_TEXT.get_rect(center=(400, 150))
            # Create the mute/unmute button
            self.speaker_image = pygame.image.load('Img/unmute.png')
            self.speaker_image = pygame.transform.scale(self.speaker_image, (170,170))
            self.speaker_muted_image = pygame.image.load('Img/mute.png')
            self.speaker_muted_image = pygame.transform.scale(self.speaker_muted_image, (170,170))

            speaker_button = Button(
                image=self.speaker_image,
                pos=(80, 80),
                text_input="",
                font=pygame.font.Font(None, 24),
                base_color="#d7fcd4", hovering_color="White"
            )

            PLAY_BUTTON = Button(image=pygame.image.load("Img/Options Rect.png"), pos=(150, 580),
                                 text_input="PLAY", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("Img/Options Rect.png"), pos=(400, 580),
                                    text_input="OPTIONS", font=self.get_font(30), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("Img/Options Rect.png"), pos=(650, 580),
                                 text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4", hovering_color="White")

            self.gameDisplay.blit(MENU_TEXT, MENU_RECT)
            self.music_paused = False
            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON,speaker_button]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.gameDisplay)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if speaker_button.checkForInput(pygame.mouse.get_pos()):
                        if self.music_paused:
                            pygame.mixer.music.unpause()  # Unpause music
                            self.music_paused = False
                            speaker_button.image = self.speaker_image
                        else:
                            pygame.mixer.music.pause()  # Pause music
                            self.music_paused = True
                            speaker_button.image = self.speaker_muted_image
                    speaker_button.update(self.gameDisplay)
                    pygame.display.update()

                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        #self.run_car(self.playerName)
                        self.countdown()
                    # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #     #options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    # Game over screen function

    def show_game_over_screen(self):
        # Clear the screen
        self.gameDisplay.fill(black)

        # Render the game over message

        game_over_text = self.font.render("GAME OVER!", True, white)
        game_over_rect = game_over_text.get_rect(center=(400, 300))
        self.gameDisplay.blit(game_over_text, game_over_rect)

        # Render the final score
        score_text = self.font.render("Score: " + str(self.count), True, white)
        score_rect = score_text.get_rect(center=(400, 400))
        self.gameDisplay.blit(score_text, score_rect)

        # Update the display
        pygame.display.flip()

    # Function to retrieve high scores from the server
    def get_high_scores_from_server(self):
        # Connect to the server
        host = 'your_server_address'
        port = 12345
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Send request for high scores
        client_socket.sendall(b"GET_HIGH_SCORES")

        # Receive high scores from the server
        high_scores_data = client_socket.recv(1024).decode()

        # Close the connection
        client_socket.close()

        # Parse and return the high scores data
        high_scores = high_scores_data.split(",")
        return high_scores

    #gameloop
    def run_car(self,playerName):

        network = Network()  # initliazed connection to server
        # mafrod a receive ana rkm kam mn el network w ahotha fi class el player

        player = Player(network.getId(), playerName, self.car_x_coordinate, self.car_y_coordinate, self.car_width,
                        100, 'Blue', 0, 0)
        print(player.mapComplete)

        # Load the music file
        pygame.mixer.music.load('Img/My_Life_Be_Like.mp3')
        pygame.mixer.music.play()

        # Load the speaker images


        while not self.crashed:
            #for switch
            self.gameDisplay.fill("black")
            self.gameDisplay.blit(self.gardenBrown, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True


                if (event.type == pygame.KEYDOWN):
                    # Check if the mute button was clicked
                    if event.key == pygame.K_r:
                        self.is_raining = not self.is_raining
                        pygame.display.update()

                    if event.key == pygame.K_SPACE:
                        self.is_paused = not self.is_paused  # Toggle pause/play state
                        # Clear the screen
                        self.gameDisplay.fill(black)
                        # Render the pause message
                        pygame.display.update()
                        pause_text = self.font.render("Paused!", True, white)
                        pygame.mixer.music.pause()
                        pause_rect = pause_text.get_rect(center=(400, 300))
                        self.gameDisplay.blit(pause_text, pause_rect)
                        pygame.display.update()


                    if (event.key == pygame.K_LEFT):
                        self.car_x_coordinate -= 120

                        #send("x position for car here")
                        print("CAR X COORDINATES: %s" % self.car_x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car_x_coordinate += 120

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
            # Update and render main menu
           # self.main_menu.main_menu()


            if self.is_paused:
                while self.is_paused:  # Stop the game loop while paused
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.is_running = False
                            self.is_paused = False  # Exit the pause loop
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.is_paused = False  # Exit the pause loop
                                pygame.mixer.music.play()

            if self.is_raining:
                if random.random() < 0.6:  # Adjust the rain frequency as desired
                    x = random.randint(0, self.display_width)
                    y = random.randint(-100, -10)
                    speed = random.randint(5, 50)
                    raindrop = Raindrop(x, y, speed)
                    self.rain_particles.append(raindrop)

                for raindrop in self.rain_particles:
                    raindrop.update()

                    if raindrop.y > self.display_height:
                        self.rain_particles.remove(raindrop)

            if self.is_raining:
                for raindrop in self.rain_particles:
                    raindrop.draw(self.gameDisplay)


            #trees
            self.count += 1
            if self.count % 20 == 0:
                self.tree = Tree(random.choice([-5, self.display_width - 35]), -70)
                self.tree_group.add(self.tree)
            self.tree_group.update(self.bg_speed)
            self.tree_group.draw(self.gameDisplay)

            self.count += 1
            if self.count % 20 == 0:
                self.tree = Tree(random.choice([-5, self.display_width - 35]), -70)
                self.tree_group.add(self.tree)
            self.tree_group.update(self.bg_speed)
            self.tree_group.draw(self.gameDisplay)

             #obstacles
            if self.count % 45 == 0:
                self.obs = random.choices([1,2,3],weights=[6,2,2],k=1) [0]
                self.obee = Pr(self.obs)
                self.Pr_group.add(self.obee)
            self.Pr_group.update(self.bg_speed)
            self.Pr_group.draw(self.gameDisplay)

            #finish line
            if self.count >= 1600:
                self.finish_line.draw()
                self.crashed = True


                self.display_message("Game Over !!!")
                pygame.display.update()

            network.getUpdateMapComplete('20')
            print(player.mapComplete)
            #print(network.getOtherPlayersPos((self.car_x_coordinate, self.car_y_coordinate)))
            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.playerName(playerName)
            self.mapCompletePerecentage(player.id)
            self.playersNumber(network.getNumberOfPlayers())
            self.highscore(self.count)
        #    self.rankers(network.getGameRankers())


            if self.car_x_coordinate < 150 or self.car_x_coordinate > 550:
                self.crashed = True
                self.display_message("Game Over !!!")

            pygame.display.update()

            #   Check for collisions with the car rect

            for obstacle in self.Pr_group:
                self.car_rect.y = self.car_y_coordinate
                self.car_rect.x = self.car_x_coordinate
                if self.car_rect.colliderect(obstacle.rect):
                    #    if pygame.sprite.collide_mask(self.Pr_group,self.car_rect):
                    self.crashed = True
                    pygame.mixer.music.load('Img/music_crash.wav')
                    pygame.mixer.music.play()
                    print("3rbya")
                    self.show_game_over_screen()
                    pygame.time.wait(3000)

            if self.car_x_coordinate < 150 or self.car_x_coordinate > 550:
                self.crashed = True
                self.display_message("Game Over !!!")

            pygame.display.update()
            self.clock.tick(60)
if __name__ == '__main__':
   car_racing = CarRacing()
   car_racing.racing_window()
