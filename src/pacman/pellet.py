import pygame
from . import constants as C

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y, pellet_type='small'):
        super().__init__()
        self.type = pellet_type
        if self.type == 'small':
            self.radius = 2
            self.value = 10
        else:  # power pellet
            self.radius = 6
            self.value = 50

        # Create the image for the pellet
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill(C.BLACK)
        self.image.set_colorkey(C.BLACK)
        pygame.draw.circle(self.image, C.YELLOW, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))
