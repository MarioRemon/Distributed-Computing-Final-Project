import pygame


class Player():
    def __init__(self, id, userName, position, width, height, color, rank, mapComplete, score):
        self.id = id
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.vel = 3
        self.rank = rank
        self.userName = userName
        self.mapComplete = mapComplete
        self.active = True
        self.score = score

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def updateMapComlete(self, mapComplete):
        self.mapComplete = mapComplete