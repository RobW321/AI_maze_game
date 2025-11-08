import pygame
from pygame import Rect
import time

class GridGame:
    def __init__(self, cell_height=10, cell_width=10, render_delay=0.1):
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.screen_size = (1500, 800)
        self.delay = render_delay

        # Colors
        self.black = (0, 0, 0)

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
                # correct checkerboard: alternate by row+col parity
                if (row + col) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)

                rect = Rect(col * self.cell_width,
                            row * self.cell_height,
                            self.cell_width,
                            self.cell_height)
                pygame.draw.rect(self.screen, color, rect)
        pygame.display.flip()


    def execute(self, command):
        if command == "UP" and self.pos[1] > 0:
            self.pos[1] -= 1
        elif command == "DOWN" and self.pos[1] < self.grid_size - 1:
            self.pos[1] += 1
        elif command == "LEFT" and self.pos[0] > 0:
            self.pos[0] -= 1
        elif command == "RIGHT" and self.pos[0] < self.grid_size - 1:
            self.pos[0] += 1

    def display_move(self, move):
        self.execute(move)  # update agent position
        self._draw_grid()  # redraw the grid
        time.sleep(self.delay)


game = GridGame()


def plan_next_move(pos, goal, goblin_pos):
    pass


def move_goblin_towards_agent(goblin_pos, pos):
    pass


if __name__ == "__main__":
    # Initialize the game
    game = GridGame(cell_height=50, cell_width=50, render_delay=0.2)

    # Example goal and goblin positions
    goal = [5, 5]
    goblin_pos = [3, 3]

    running = False #false for now, cuz it keeps loading a lot
    while running:
        next_move = plan_next_move(game.pos, goal, goblin_pos)


        game.display_move(next_move)


        goblin_pos = move_goblin_towards_agent(goblin_pos, game.pos)


        if game.pos == goal:
            print("Goal reached!")
            running = False