import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 64))  # Player dimensions (2 blocks high)
        self.image.fill((255, 0, 0))  # Red color for the player
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, blocks):
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15

        # Gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        # Collision detection
        self.on_ground = False
        self.rect.x += dx
        # Check for collision in x-direction
        for block in pygame.sprite.spritecollide(self, blocks, False):
            if dx > 0:
                self.rect.right = block.rect.left
            if dx < 0:
                self.rect.left = block.rect.right

        self.rect.y += dy
        # Check for collision in y-direction
        for block in pygame.sprite.spritecollide(self, blocks, False):
            if dy > 0:
                self.rect.bottom = block.rect.top
                self.vel_y = 0
                self.on_ground = True
            if dy < 0:
                self.rect.top = block.rect.bottom
                self.vel_y = 0
