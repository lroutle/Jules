import pygame
import sys
from .player import Player
from .bullet import Bullet
from .alien import Alien

def create_fleet(screen_width, all_sprites, aliens):
    alien_width = 40
    alien_height = 30
    available_space_x = screen_width - (2 * alien_width)
    number_aliens_x = available_space_x // (2 * alien_width)

    number_rows = 3

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            x = alien_width + 2 * alien_width * alien_number
            y = alien_height + 2 * alien_height * row_number
            alien = Alien(x, y)
            aliens.add(alien)
            all_sprites.add(alien)

def main():
    pygame.init()

    # Screen dimensions
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Window title
    pygame.display.set_caption("Space Invaders")

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()

    # Create player
    player = Player(screen_width, screen_height)
    all_sprites.add(player)

    # Create the fleet of aliens
    create_fleet(screen_width, all_sprites, aliens)

    # Alien movement settings
    alien_fleet_direction = 1
    alien_move_speed = 1
    alien_fleet_drop_speed = 10

    # Game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        # Keep loop running at the right speed
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # Update
        all_sprites.update()

        # Alien Fleet Movement
        edge_hit = False
        for alien in aliens.sprites():
            if (alien.rect.right >= screen_width and alien_fleet_direction == 1) or \
               (alien.rect.left <= 0 and alien_fleet_direction == -1):
                edge_hit = True
                break

        if edge_hit:
            alien_fleet_direction *= -1
            for alien in aliens.sprites():
                alien.rect.y += alien_fleet_drop_speed

        for alien in aliens.sprites():
            alien.rect.x += alien_move_speed * alien_fleet_direction

        # Check for collisions between bullets and aliens
        pygame.sprite.groupcollide(bullets, aliens, True, True)

        # Draw / render
        screen.fill((0, 0, 0))  # Black background
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # To run the game directly, you would need to handle the package structure.
    # For example, run as a module: python -m src.space_invaders.main
    # For simplicity, we'll assume it's run as part of a larger application.
    # A simple way to make it runnable is to add the src directory to the path.
    import os
    # This is a bit of a hack for direct execution.
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from src.space_invaders.main import main as main_game
    main_game()
