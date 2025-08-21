import pygame
import time
from . import constants as C
from .maze import Maze
from .player import Player
from .pellet import Pellet
from .ghost import Ghost

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(C.SCREEN_SIZE)
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.state = C.START
        self.score = 0
        self.lives = 3

        self.maze = Maze()
        self.player_start_pos = (0, 0)
        self.ghost_start_pos = []

        self.pellet_group = pygame.sprite.Group()
        self.ghost_group = pygame.sprite.Group()

        self.player = self.create_player()
        self.create_pellets()
        self.create_ghosts()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.pellet_group, self.ghost_group)

        self.power_pellet_timer = -1
        self.vulnerable_duration = 7000 # 7 seconds in milliseconds


    def create_player(self):
        for row_idx, row in enumerate(self.maze.layout):
            for col_idx, char in enumerate(row):
                if char == 'P':
                    self.player_start_pos = (col_idx * C.TILE_WIDTH + C.TILE_WIDTH // 2, row_idx * C.TILE_HEIGHT + C.TILE_HEIGHT // 2)
                    return Player(self.player_start_pos[0], self.player_start_pos[1])
        self.player_start_pos = (C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2)
        return Player(self.player_start_pos[0], self.player_start_pos[1])

    def create_pellets(self):
        for row_idx, row in enumerate(self.maze.layout):
            for col_idx, char in enumerate(row):
                pos = (col_idx * C.TILE_WIDTH + C.TILE_WIDTH // 2, row_idx * C.TILE_HEIGHT + C.TILE_HEIGHT // 2)
                if char == '.':
                    self.pellet_group.add(Pellet(pos[0], pos[1], 'small'))
                elif char == 'o':
                    self.pellet_group.add(Pellet(pos[0], pos[1], 'power'))

    def create_ghosts(self):
        positions = [ (13, 11), (14, 14), (12, 14), (15, 14) ] # Centered around the ghost house
        colors = [C.RED, C.PINK, C.CYAN, C.ORANGE]
        for i in range(4):
            pos_x = positions[i][0] * C.TILE_WIDTH + C.TILE_WIDTH // 2
            pos_y = positions[i][1] * C.TILE_HEIGHT + C.TILE_HEIGHT // 2
            self.ghost_start_pos.append((pos_x, pos_y))
            self.ghost_group.add(Ghost(pos_x, pos_y, colors[i], i))

    def run(self):
        self.state = C.PLAYING
        while self.state != C.GAMEOVER:
            if self.state == C.PLAYING:
                self.events()
                self.update()
                self.draw()
            elif self.state == C.WINNER:
                self.show_win_screen()
        self.show_game_over_screen()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.state = C.GAMEOVER
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: self.player.set_direction(pygame.Vector2(-1, 0))
                elif event.key == pygame.K_RIGHT: self.player.set_direction(pygame.Vector2(1, 0))
                elif event.key == pygame.K_UP: self.player.set_direction(pygame.Vector2(0, -1))
                elif event.key == pygame.K_DOWN: self.player.set_direction(pygame.Vector2(0, 1))

    def update(self):
        self.all_sprites.update(self.maze)
        self.check_pellet_collision()
        self.check_ghost_collision()
        self.check_power_pellet_timer()
        self.check_game_state()

    def check_pellet_collision(self):
        eaten_pellets = pygame.sprite.spritecollide(self.player, self.pellet_group, True)
        for pellet in eaten_pellets:
            self.score += pellet.value
            if pellet.type == 'power': self.activate_power_pellet()

    def check_ghost_collision(self):
        collided_ghosts = pygame.sprite.spritecollide(self.player, self.ghost_group, False)
        for ghost in collided_ghosts:
            if ghost.is_vulnerable:
                self.score += 200 # Bonus for eating a ghost
                ghost.reset(self.ghost_start_pos[ghost.color_index][0], self.ghost_start_pos[ghost.color_index][1])
            else:
                self.lives -= 1
                if self.lives > 0: self.reset_level()
                else: self.state = C.GAMEOVER
                return # Stop checking after one collision kills the player

    def check_power_pellet_timer(self):
        if self.power_pellet_timer > 0:
            if pygame.time.get_ticks() - self.power_pellet_timer > self.vulnerable_duration:
                self.power_pellet_timer = -1
                for ghost in self.ghost_group: ghost.set_vulnerable(False)

    def check_game_state(self):
        if not self.pellet_group: self.state = C.WINNER

    def activate_power_pellet(self):
        self.power_pellet_timer = pygame.time.get_ticks()
        for ghost in self.ghost_group: ghost.set_vulnerable(True)

    def reset_level(self):
        time.sleep(1)
        self.player.reset(self.player_start_pos[0], self.player_start_pos[1])
        for i, ghost in enumerate(self.ghost_group):
            ghost.reset(self.ghost_start_pos[i][0], self.ghost_start_pos[i][1])
        # This will also reset their vulnerability state via the ghost's reset method
        self.power_pellet_timer = -1

    def draw_text(self, text, surface, pos, color=C.WHITE):
        text_obj = self.font.render(text, 1, color)
        text_rect = text_obj.get_rect(center=pos)
        surface.blit(text_obj, text_rect)

    def draw(self):
        self.screen.fill(C.BLACK)
        self.maze.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.draw_text(f"Score: {self.score}", self.screen, (80, 20), C.YELLOW)
        self.draw_text(f"Lives: {self.lives}", self.screen, (C.SCREEN_WIDTH - 80, 20), C.YELLOW)
        pygame.display.flip()
        self.clock.tick(C.FPS)

    def show_game_over_screen(self):
        self.screen.fill(C.BLACK)
        self.draw_text("GAME OVER", self.screen, (C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2), C.RED)
        pygame.display.flip()
        time.sleep(3)

    def show_win_screen(self):
        self.screen.fill(C.BLACK)
        self.draw_text("YOU WIN!", self.screen, (C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2), C.YELLOW)
        pygame.display.flip()
        time.sleep(3)
        self.state = C.GAMEOVER

if __name__ == "__main__":
    game = Game()
    game.run()
