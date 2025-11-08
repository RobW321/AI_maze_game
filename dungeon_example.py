import pygame
import random
from pygame import Rect

class DungeonGame:
    def __init__(self, rows=50, cols=50, cell_size=14):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.screen_size = (cols * cell_size, rows * cell_size)

        # Colors
        self.COLOR_WALL = (139, 69, 19)     # brown
        self.COLOR_FLOOR = (169, 169, 169)  # gray
        self.COLOR_PLAYER = (0, 255, 0)     # green
        self.COLOR_EXIT = (255, 0, 0)       # red
        self.COLOR_GRID = (0, 0, 0)         # black grid lines

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Dungeon Crawler Prototype")
        self.clock = pygame.time.Clock()

        # Generate dungeon map
        self.grid = self._generate_dungeon()

        # Find player and exit
        self.player_pos = self._find_spawn()
        self.exit_pos = self._place_exit()

    def _generate_dungeon(self):
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

    def _find_spawn(self):
        # Player starts somewhere near left edge on a floor tile
        for row in range(self.rows):
            for col in range(5):  # only check first 5 columns
                if self.grid[row][col] == "F":
                    return [row, col]
        return [0, 0]  # fallback

    def _place_exit(self):
        # Exit spawns toward right edge on a floor tile
        for row in range(self.rows - 1, -1, -1):
            for col in range(self.cols - 1, self.cols - 6, -1):
                if self.grid[row][col] == "F":
                    return [row, col]
        return [self.rows - 1, self.cols - 1]  # fallback

    def _draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = Rect(col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size)

                # Choose color based on tile type
                tile = self.grid[row][col]
                if [row, col] == self.player_pos:
                    color = self.COLOR_PLAYER
                elif [row, col] == self.exit_pos:
                    color = self.COLOR_EXIT
                elif tile == "W":
                    color = self.COLOR_WALL
                else:
                    color = self.COLOR_FLOOR

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.COLOR_GRID, rect, width=1)

    def _loop(self):
        self.clock.tick(30)

game = DungeonGame()

if __name__ == "__main__":
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.screen.fill((0, 0, 0))
        game._draw_grid()
        pygame.display.flip()
        game._loop()

    pygame.quit()
