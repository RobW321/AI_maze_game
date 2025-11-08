import pygame
from pygame import Rect
import time
import random

class GridGame:
    def __init__(self, cell_height=30, cell_width=30, render_delay=0.1):
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.screen_size = (1500, 800)
        self.delay = render_delay

        # Colors
        self.COLOR_WALL = (139, 69, 19)     # brown
        self.COLOR_FLOOR = (169, 169, 169)  # gray
        self.COLOR_PLAYER = (0, 255, 0)     # green
        self.COLOR_EXIT = (255, 0, 0)       # red
        self.COLOR_GRID = (0, 0, 0)         # black grid lines
        self.BLACK = self.COLOR_GRID
        self.WHITE = (255, 255, 255)        # white

        # Player position
        self.pos = [0, 0]

        # Pygame setup
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Maze")
        self.clock = pygame.time.Clock()

    def _draw_grid(self):
        number_of_rows = self.screen_size[1] // self.cell_height
        number_of_columns = self.screen_size[0] // self.cell_width

        for row in range(number_of_rows):
            for col in range(number_of_columns):

                rect = Rect(col * self.cell_width,
                            row * self.cell_height,
                            self.cell_width,
                            self.cell_height)
                
                pygame.draw.rect(self.screen, self.white, rect)
                pygame.draw.rect(self.screen, self.black, rect, width=1)

    def _generate_dungeon(self):
        """
        Generates 
        """
        grid = []
        for row in range(self.rows):
            grid_row = []
            for col in range(self.cols):
                # Randomly choose wall or floor
                if random.random() < 0.25:  # 25% chance of wall
                    grid_row.append("W")
                else:
                    grid_row.append("F")
            grid.append(grid_row)
        return grid


    def execute(self, command):
        #TODO: needs to be implemented
        pass

    def _loop(self):
        #TODO: needs to be implemented
        pass

    def _generate_maze():
        pass


game = GridGame()
if __name__ == "__main__":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game._draw_grid()
        pygame.display.flip()
        game._loop()
