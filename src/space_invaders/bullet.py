import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 5
        self.height = 10
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))  # White color for the bullet
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill() # remove the bullet if it goes off screen
