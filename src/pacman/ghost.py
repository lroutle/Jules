import pygame
import random
from . import constants as C

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color, color_index):
        super().__init__()
        self.original_color = color
        self.color = color
        self.color_index = color_index

        self.is_vulnerable = False
        self.vulnerable_color = C.BLUE

        self.anim_timer = 0
        self.anim_frame = 0

        self.direction = random.choice([pygame.Vector2(1, 0), pygame.Vector2(-1, 0), pygame.Vector2(0, 1), pygame.Vector2(0, -1)])
        self.image = pygame.Surface([C.TILE_WIDTH, C.TILE_HEIGHT], pygame.SRCALPHA)
        self.draw_body()

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1.5

    def draw_body(self):
        # Clear surface
        self.image.fill((0,0,0,0)) # Transparent background

        w = C.TILE_WIDTH
        h = C.TILE_HEIGHT

        # Main body (dome shape)
        pygame.draw.circle(self.image, self.color, (w/2, h/2), w/2, draw_top_left=True, draw_top_right=True)
        pygame.draw.rect(self.image, self.color, (0, h/2, w, h/2))

        # Wavy bottom
        # This alternates based on an animation timer
        offset = self.anim_frame * (h/8)
        pygame.draw.circle(self.image, self.color, (w/4, h - h/4 + offset), w/4)
        pygame.draw.circle(self.image, self.color, (w - w/4, h - h/4 + offset), w/4)

        # Eyes
        eye_w, eye_h = w/3, h/3
        eye_y = h/3
        eye_white_left = pygame.Rect(w*0.15, eye_y, eye_w, eye_h)
        eye_white_right = pygame.Rect(w*0.55, eye_y, eye_w, eye_h)
        pygame.draw.rect(self.image, C.WHITE, eye_white_left, border_radius=3)
        pygame.draw.rect(self.image, C.WHITE, eye_white_right, border_radius=3)

        # Pupils that move
        pupil_w, pupil_h = eye_w/2, eye_h/2
        pupil_offset_x = self.direction.x * (eye_w / 4)
        pupil_offset_y = self.direction.y * (eye_h / 4)

        pupil_left_pos = (eye_white_left.centerx - pupil_w/2 + pupil_offset_x, eye_white_left.centery - pupil_h/2 + pupil_offset_y)
        pupil_right_pos = (eye_white_right.centerx - pupil_w/2 + pupil_offset_x, eye_white_right.centery - pupil_h/2 + pupil_offset_y)
        pygame.draw.circle(self.image, C.BLACK, pupil_left_pos, pupil_w/1.5)
        pygame.draw.circle(self.image, C.BLACK, pupil_right_pos, pupil_w/1.5)


    def set_vulnerable(self, is_vulnerable):
        self.is_vulnerable = is_vulnerable
        if self.is_vulnerable:
            self.color = self.vulnerable_color
        else:
            self.color = self.original_color
        self.draw_body()

    def update(self, maze):
        self.animate()
        old_rect = self.rect.copy()
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.is_colliding(self.rect, maze):
            self.rect = old_rect
            self.change_direction(maze)

        self.draw_body() # Redraw every frame to update eyes/animation

    def animate(self):
        self.anim_timer += 1
        if self.anim_timer > 10:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 2

    def change_direction(self, maze):
        possible_directions = [pygame.Vector2(1, 0), pygame.Vector2(-1, 0), pygame.Vector2(0, 1), pygame.Vector2(0, -1)]
        if self.direction.length() > 0 and -self.direction in possible_directions:
            possible_directions.remove(-self.direction)

        valid_directions = []
        for direction in possible_directions:
            test_rect = self.rect.copy()
            test_rect.move_ip(direction * self.speed)
            if not self.is_colliding(test_rect, maze):
                valid_directions.append(direction)

        if valid_directions:
            self.direction = random.choice(valid_directions)
        elif self.direction.length() > 0:
            self.direction = -self.direction
        else: # Should not happen if moving
            self.direction = random.choice([pygame.Vector2(1,0), pygame.Vector2(-1,0)])


    def is_colliding(self, rect, maze):
        for row_idx, row in enumerate(maze.layout):
            for col_idx, char in enumerate(row):
                if char == 'X':
                    wall_rect = pygame.Rect(col_idx * C.TILE_WIDTH, row_idx * C.TILE_HEIGHT, C.TILE_WIDTH, C.TILE_HEIGHT)
                    if rect.colliderect(wall_rect):
                        return True
        return False

    def reset(self, x, y):
        self.rect.center = (x,y)
        self.direction = random.choice([pygame.Vector2(1, 0), pygame.Vector2(-1, 0), pygame.Vector2(0, 1), pygame.Vector2(0, -1)])
        self.set_vulnerable(False)
