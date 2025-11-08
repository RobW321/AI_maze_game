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
        self.white = (255, 255, 255)
        self.gray = (200, 200, 200)
        self.player_color = (0, 255, 0)

        # Player position
        self.pos = [0, 0]

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Simple Grid Game")
        self.clock = pygame.time.Clock()

    def _draw_grid(self):
        #TODO: needs to be implemented
        
        pass

    def execute(self, command):
        #TODO: needs to be implemented
        if command == "UP" and self.pos[1] > 0:
            self.pos[1] -= 1
        elif command == "DOWN" and self.pos[1] < self.grid_size - 1:
            self.pos[1] += 1
        elif command == "LEFT" and self.pos[0] > 0:
            self.pos[0] -= 1
        elif command == "RIGHT" and self.pos[0] < self.grid_size - 1:
            self.pos[0] += 1 
         

    def _loop(self):
        #TODO: needs to be implemented

        pass

if __name__ == "__main__":
    game = GridGame(grid_size=6)
    game._draw_grid()
    ##game._loop()