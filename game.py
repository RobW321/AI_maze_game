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

    def _draw_grid(self):
        #TODO: needs to be implemented
        pass

    def execute(self, command):
        #TODO: needs to be implemented
        pass

    def _loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.execute("up")
                    elif event.key == pygame.K_DOWN:
                        self.execute("down")
                    elif event.key == pygame.K_LEFT:
                        self.execute("left")
                    elif event.key == pygame.K_RIGHT:
                        self.execute("right")
            self.clock.tick(60)

if __name__ == "__main__":
    game = GridGame(grid_size=6)
    game._draw_grid()
    game._loop()
