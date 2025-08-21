import pygame
from . import constants as C

class Maze:
    def __init__(self):
        self.layout = [
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "X............XX............X",
            "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
            "XoX  X.X   X.XX.X   X.X  XoX",
            "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
            "X..........................X",
            "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
            "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
            "X......XX....XX....XX......X",
            "XXXXXX.XXXXX XX XXXXX.XXXXXX",
            "     X.XXXXX XX XXXXX.X     ",
            "     X.XX   -  -   XX.X     ",
            "     X.XX XXXXXXXX XX.X     ",
            "XXXXXX.XX X      X XX.XXXXXX",
            "      .   X      X   .      ",
            "XXXXXX.XX X      X XX.XXXXXX",
            "     X.XX XXXXXXXX XX.X     ",
            "     X.XX   -  -   XX.X     ",
            "     X.XXXXX XX XXXXX.X     ",
            "XXXXXX.XXXXX XX XXXXX.XXXXXX",
            "X............XX............X",
            "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
            "XoXXXX.XXXXX.XX.XXXXX.XXXXoX",
            "X...XX.......P .......XX...X",
            "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
            "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
            "X......XX....XX....XX......X",
            "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
            "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
            "X..........................X",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        ]
        self.tile_width = C.SCREEN_WIDTH // len(self.layout[0])
        self.tile_height = C.SCREEN_HEIGHT // len(self.layout)
        self.wall_color = C.BLUE

    def draw(self, screen):
        for row_idx, row in enumerate(self.layout):
            for col_idx, char in enumerate(row):
                if char == 'X':
                    x = col_idx * self.tile_width
                    y = row_idx * self.tile_height
                    # Adjust wall drawing to be lines for a more classic look
                    # This is a simplified version. A more advanced version would
                    # check neighbors to draw connected walls.
                    pygame.draw.rect(screen, self.wall_color, pygame.Rect(x, y, self.tile_width, self.tile_height), 1)
