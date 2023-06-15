from tkinter import *
from cargame import CarRacing
from MuteButton import MuteButton
import pygame
from button import Button
import sys
from gameNetwork import GameNetwork

#define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (211, 211, 211)


car = CarRacing()

class HomePage:

    def __init__(self):
        self.crashed = False
        self.speaker_image = pygame.image.load('Img/unmute.png')
        self.speaker_image = pygame.transform.scale(self.speaker_image, (170, 170))
        self.speaker_muted_image = pygame.image.load('Img/mute.png')
        self.speaker_muted_image = pygame.transform.scale(self.speaker_muted_image, (170, 170))

        MENU_TEXT = self.get_font(50).render("MAIN MENU", True, white)
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 150))
        self.display_width = 800
        self.display_height = 700
        self.BG = pygame.image.load("Img/intro.jpg")
        self.BG = pygame.transform.scale(self.BG, (self.display_width, self.display_height))
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        self.gameDisplay.blit(self.BG, (0, 0))

        # Text box properties
        self.username = ""
        self.font = pygame.font.Font(None, 32)
        self.textbox_rect = pygame.Rect(300, 200, 200, 30)

        while not self.crashed:
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MUTE_BUTTON = MuteButton(self.speaker_muted_image, self.speaker_image, (50, 50))
            PLAY_BUTTON = Button(image=pygame.image.load("Img/Options Rect.png"), pos=(150, 580),
                                      text_input="PLAY", font=self.get_font(30), base_color="#d7fcd4",
                                      hovering_color="black")

            self.OPTIONS_BUTTON = Button(image=pygame.image.load("Img/Options Rect.png"), pos=(400, 580),
                                         text_input="OPTIONS", font=self.get_font(30), base_color="#d7fcd4",
                                         hovering_color="black")
            self.QUIT_BUTTON = Button(image=pygame.image.load("Img/Options Rect.png"), pos=(650, 580),
                                      text_input="QUIT", font=self.get_font(30), base_color="#d7fcd4",
                                      hovering_color="black")
            self.music_paused = False
            for button in [PLAY_BUTTON, self.OPTIONS_BUTTON, self.QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.gameDisplay)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                    sys.exit()
                else:
                    MUTE_BUTTON.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        car.countdown(self.username)

                    if self.QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                    # if self.speaker_button.checkForInput(pygame.mouse.get_pos()):
                    #     if self.music_paused:
                    #         pygame.mixer.music.unpause()  # Unpause music
                    #         self.music_paused = False
                    #         self.speaker_button.image = self.speaker_image
                    #     else:
                    #         pygame.mixer.music.pause()  # Pause music
                    #         self.music_paused = True
                    #         self.speaker_button.image = self.speaker_muted_image
                    # self.speaker_button.update(self.gameDisplay)
                    # pygame.display.update()
                    if self.textbox_rect.collidepoint(event.pos):
                        pygame.key.start_text_input()
                    else:
                        pygame.key.stop_text_input()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.textbox_rect.collidepoint(MENU_MOUSE_POS):
                        print(self.username)

                        pygame.key.stop_text_input()
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode

            MUTE_BUTTON.draw(self.gameDisplay)

            # Draw the text box
            pygame.draw.rect(self.gameDisplay, (0, 0, 0), (300, 200, 200, 30), 2)
            self.textbox_surface = self.font.render(self.username, True, white)
            self.gameDisplay.blit(self.textbox_surface, (self.textbox_rect.x + 5, self.textbox_rect.y + 5))



            self.gameDisplay.blit(MENU_TEXT, MENU_RECT)


            pygame.display.update()
            pygame.time.Clock().tick(60)

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
            return pygame.font.Font("Img/font.ttf", size)

