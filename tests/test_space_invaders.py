import pytest
import sys
import os

# Add src directory to the python path
# This allows us to import the game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from space_invaders.alien import Alien
from space_invaders.bullet import Bullet
from space_invaders.player import Player
import pygame

# A fixture to initialize pygame once for the whole test session
@pytest.fixture(scope="session")
def pygame_init():
    """Initializes pygame and quits it after the test session."""
    pygame.init()
    yield
    pygame.quit()

def test_alien_creation(pygame_init):
    """Tests that an Alien is created at the correct coordinates."""
    alien = Alien(100, 50)
    assert alien.rect.x == 100
    assert alien.rect.y == 50

def test_bullet_creation(pygame_init):
    """Tests that a Bullet is created at the correct coordinates."""
    bullet = Bullet(200, 300)
    assert bullet.rect.x == 200
    assert bullet.rect.y == 300

def test_bullet_update(pygame_init):
    """Tests that the bullet moves upwards when update() is called."""
    bullet = Bullet(200, 300)
    initial_y = bullet.rect.y
    bullet.update()
    assert bullet.rect.y < initial_y
    assert bullet.rect.y == initial_y - bullet.speed

def test_player_creation(pygame_init):
    """Tests that the Player is created at the correct initial position."""
    screen_width = 800
    screen_height = 600
    player = Player(screen_width, screen_height)
    # Player should start in the bottom center of the screen
    expected_x = (screen_width - player.width) / 2
    expected_y = screen_height - player.height - 10
    assert player.rect.x == expected_x
    assert player.rect.y == expected_y

def test_player_shoot(pygame_init):
    """Tests that the player's shoot() method creates a bullet in the correct location."""
    player = Player(800, 600)
    bullet = player.shoot()
    assert isinstance(bullet, Bullet)
    # The bullet should be created at the top-center of the player's rectangle
    assert bullet.rect.centerx == player.rect.centerx
    assert bullet.rect.bottom == player.rect.top
