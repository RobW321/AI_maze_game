import pygame
import time

class GridGame:
    def __init__(self, grid_size=15, cell_size=40, render_delay=0.1):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.screen_size = grid_size * cell_size
        self.delay = render_delay

        # Colors
        self.black = (0, 0, 0)

        # Player position
        self.pos = [0, 0]

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Simple Grid Game")
        self.clock = pygame.time.Clock()
