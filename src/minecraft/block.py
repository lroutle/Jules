import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, block_type='grass'):
        super().__init__()
        self.block_type = block_type

        # Define block properties based on type
        if self.block_type == 'grass':
            color = (0, 255, 0)  # Green
        elif self.block_type == 'dirt':
            color = (139, 69, 19)  # Brown
        else:
            color = (128, 128, 128) # Grey for undefined blocks

        self.image = pygame.Surface((32, 32)) # Standard block size
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
