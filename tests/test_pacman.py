import pytest
import pygame
from src.pacman.main import Game
from src.pacman.player import Player
from src.pacman.ghost import Ghost
from src.pacman import constants as C

# A fixture to initialize pygame once for the test session
@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def game():
    """Fixture to create a game instance for testing."""
    return Game()

def test_game_creation(game):
    """Test that the Game object can be created without errors."""
    assert game is not None
    assert game.score == 0
    assert game.lives == 3
    assert len(game.pellet_group) > 0
    assert len(game.ghost_group) == 4

def test_player_movement_no_wall(game):
    """Test basic player movement where there is no wall."""
    player = game.player
    # Find a safe spot to test movement, e.g., the starting position
    player.rect.center = game.player_start_pos
    initial_pos = player.rect.copy()

    # Move right (assuming it's a valid move from the start)
    player.set_direction(pygame.Vector2(1, 0))
    player.update(game.maze)

    assert player.rect.x > initial_pos.x, "Player should move right"

def test_pellet_collision(game):
    """Test that eating a pellet increases score and removes the pellet."""
    player = game.player
    pellet_group = game.pellet_group

    if not pellet_group:
        pytest.skip("No pellets to test collision with.")

    pellet_to_eat = pellet_group.sprites()[0]
    player.rect.center = pellet_to_eat.rect.center

    initial_score = game.score
    initial_pellet_count = len(pellet_group)

    # Manually call the collision check
    game.check_pellet_collision()

    assert game.score > initial_score, "Score should increase after eating a pellet"
    # The pellet is removed from the group, which is now smaller
    assert len(game.pellet_group) < initial_pellet_count, "Pellet should be removed after being eaten"

def test_ghost_collision_lose_life(game):
    """Test losing a life when colliding with a non-vulnerable ghost."""
    player = game.player
    ghost = game.ghost_group.sprites()[0]

    # Ensure ghost is not vulnerable
    ghost.set_vulnerable(False)
    assert not ghost.is_vulnerable

    # Move player to the ghost's position
    player.rect.center = ghost.rect.center

    initial_lives = game.lives

    game.check_ghost_collision()

    assert game.lives < initial_lives, "Player should lose a life after colliding with a ghost"

def test_power_pellet_and_eat_ghost(game):
    """Test eating a power pellet and then a vulnerable ghost."""
    player = game.player
    ghost = game.ghost_group.sprites()[0]

    # 1. Activate power mode
    game.activate_power_pellet()
    assert ghost.is_vulnerable, "Ghost should become vulnerable after power pellet is activated"

    # 2. Collide with the vulnerable ghost
    player.rect.center = ghost.rect.center
    initial_score = game.score
    initial_lives = game.lives

    game.check_ghost_collision()

    # 3. Check results
    assert game.score > initial_score, "Score should increase after eating a vulnerable ghost"
    assert game.lives == initial_lives, "Player should not lose a life when eating a vulnerable ghost"
    assert not ghost.is_vulnerable, "Ghost should reset to not vulnerable after being eaten"
