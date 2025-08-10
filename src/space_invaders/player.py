import pygame
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.width = 50
        self.height = 25
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((0, 255, 0))  # Green color for the player
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width - self.width) / 2
        self.rect.y = screen_height - self.height - 10
        self.speed = 5
        self.screen_width = screen_width

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.bottom = self.rect.top
        return bullet
