import pygame
from pygame import Rect
import time

class GridGame:
    def __init__(self, cell_height=30, cell_width=30, render_delay=0.1):
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.screen_size = (1500, 800)
        self.delay = render_delay

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

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


    def execute(self, command):
        #TODO: needs to be implemented
        pass

    def _loop(self):
        #TODO: needs to be implemented
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
