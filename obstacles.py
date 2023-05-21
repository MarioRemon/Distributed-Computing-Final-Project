import random

import pygame.sprite
lan_pos = [205,285,370,450,525, 610 ,700,780] #,300,430,548
display_height = 700
display_width = 800
window = pygame.display.set_mode((display_width, display_height))
class Tree(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Tree,self).__init__()
        type = random.randint(1,4)
        self.image = pygame.image.load(f'Img/trees/{type}.png',)
        self.image = pygame.transform.scale(self.image, (70, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed):
        self.rect.y += speed
        if self.rect.y >= display_height:
            self.kill()

    def draw(self,win):
        win.blit(self.image,self.rect)


class FinishLine:
    def __init__(self, x, y):
        self.image = pygame.image.load('Img/small_horizontal.png')
        self.image = pygame.transform.scale(self.image, (690, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        window.blit(self.image, self.rect)


# Raindrop class
class Raindrop:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.line(surface, (202, 255, 251), (self.x, self.y), (self.x, self.y + 10), 2)



class Pr(pygame.sprite.Sprite):
    def __init__(self,type):
        super(Pr,self).__init__()
        self.type = type
        if type == 1:
            ctype =  random.randint(2,8)
            self.image = pygame.image.load(f'Img/cars/{ctype}.png')
            self.image = pygame.transform.flip(self.image,False,True)
            self.image = pygame.transform.scale(self.image,(70, 110))

        if type == 2:
            self.image = pygame.image.load(f'Img/barrel.png')
            self.image = pygame.transform.scale(self.image, (70, 85))

        if type == 3:
            self.image = pygame.image.load(f'Img/roadblock.png')
            self.image = pygame.transform.scale(self.image, (70, 80))

        self.rect = self.image.get_rect()
        self.rect.x = random.choice(lan_pos)
        self.rect.y = -100

    def update(self, speed):
            self.rect.y += speed
            self.mask = pygame.mask.from_surface(self.image)
    def draw(self, win):
            win.blit(self.image, self.rect)
