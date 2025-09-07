import pygame
import sys
from block import Block
from player import Player

def main():
    pygame.init()

    # Screen dimensions
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Window title
    pygame.display.set_caption("Minecraft")

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()

    # World generation
    for x in range(0, screen_width, 32):
        for y in range(screen_height - 32, screen_height - 32 * 4, -32):
            block = Block(x, y, 'dirt')
            all_sprites.add(block)
            blocks.add(block)
        block = Block(x, screen_height - 32 * 4, 'grass')
        all_sprites.add(block)
        blocks.add(block)

    # Create player
    player = Player(screen_width / 2, screen_height - 32 * 5)
    all_sprites.add(player)

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        # Keep loop running at the right speed
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if event.button == 1:  # Left click to break
                    for block in blocks:
                        if block.rect.collidepoint(pos):
                            block.kill()
                if event.button == 3:  # Right click to place
                    # Snap to grid
                    grid_x = (pos[0] // 32) * 32
                    grid_y = (pos[1] // 32) * 32
                    # Check if a block already exists here
                    can_place = True
                    for block in blocks:
                        if block.rect.topleft == (grid_x, grid_y):
                            can_place = False
                            break
                    if can_place:
                        new_block = Block(grid_x, grid_y, 'dirt')
                        all_sprites.add(new_block)
                        blocks.add(new_block)

        # Update
        player.update(blocks)

        # Draw / render
        screen.fill((135, 206, 235))  # Sky blue background
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
