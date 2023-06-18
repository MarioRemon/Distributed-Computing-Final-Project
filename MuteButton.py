import pygame
class MuteButton:
    def __init__(self, mute_image, unmute_image, pos):
        self.mute_image = mute_image
        self.unmute_image = unmute_image
        self.image = mute_image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.is_muted = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle_mute()

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            self.image = self.mute_image
        else:
            self.image = self.unmute_image

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
