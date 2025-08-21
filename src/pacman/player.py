import pygame
from . import constants as C

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = C.TILE_WIDTH // 2 - 2
        self.speed = 2
        self.direction = pygame.Vector2(0, 0)
        self.target_direction = pygame.Vector2(0, 0)
        self.last_direction = pygame.Vector2(1, 0) # Start facing right

        # Animation attributes
        self.images = []
        self.mouth_angle = 40
        self.anim_speed = 4 # smaller is faster
        self.anim_timer = 0
        self.current_frame = 0
        self.anim_direction = 1 # 1 for opening, -1 for closing
        self.load_images()

        self.image = self.images[self.current_frame]
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(x, y))

    def load_images(self):
        # Generates the animation frames for Pac-Man's mouth
        self.images = []
        for i in range(self.mouth_angle, -1, -10):
            img = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            # Draw circle
            pygame.draw.circle(img, C.YELLOW, (self.radius, self.radius), self.radius)
            # Draw mouth (a wedge that gets smaller)
            if i > 0:
                start_angle = pygame.math.Vector2(1, 0).angle_to((1, -1)) + i
                end_angle = pygame.math.Vector2(1, 0).angle_to((1, 1)) - i
                pygame.draw.polygon(img, C.BLACK, [(self.radius, self.radius),
                                                   (self.radius + self.radius * pygame.math.Vector2(1,0).rotate(start_angle).x, self.radius + self.radius * pygame.math.Vector2(1,0).rotate(start_angle).y),
                                                   (self.radius + self.radius * pygame.math.Vector2(1,0).rotate(end_angle).x, self.radius + self.radius * pygame.math.Vector2(1,0).rotate(end_angle).y)])
            self.images.append(img)
        # Add a fully closed frame
        img_closed = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(img_closed, C.YELLOW, (self.radius, self.radius), self.radius)
        self.images.append(img_closed)


    def update(self, maze):
        old_rect = self.rect.copy()

        # Movement logic
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if self.is_colliding(self.rect, maze):
            self.rect = old_rect

        self.animate()
        self.rotate()

    def animate(self):
        self.anim_timer += 1
        if self.direction.length() == 0: # Stop animation when still
            self.current_frame = 0
            return

        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.current_frame += self.anim_direction
            if self.current_frame >= len(self.images) -1 or self.current_frame <= 0:
                self.anim_direction *= -1

    def rotate(self):
        if self.direction.length() > 0:
            self.last_direction = self.direction.copy()

        angle = self.last_direction.angle_to(pygame.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.images[self.current_frame], angle)
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def is_colliding(self, rect, maze):
        for row_idx, row in enumerate(maze.layout):
            for col_idx, char in enumerate(row):
                if char == 'X':
                    wall_rect = pygame.Rect(col_idx * C.TILE_WIDTH, row_idx * C.TILE_HEIGHT, C.TILE_WIDTH, C.TILE_HEIGHT)
                    if rect.colliderect(wall_rect):
                        return True
        return False

    def set_direction(self, direction):
        # A simple check to see if the new direction is valid
        test_rect = self.rect.copy()
        test_rect.x += direction.x * self.speed
        test_rect.y += direction.y * self.speed
        # We need access to the maze here to check for wall collisions before turning
        # For now, we will just set the direction. A better implementation would check turns at intersections.
        self.direction = direction

    def reset(self, x, y):
        self.rect.center = (x, y)
        self.direction = pygame.Vector2(0, 0)
        self.target_direction = pygame.Vector2(0, 0)
        self.current_frame = 0 # Reset animation
        self.rotate() # Reset rotation to default
