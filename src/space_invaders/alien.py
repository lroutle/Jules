import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 30
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 0, 0))  # Red color for the alien
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
