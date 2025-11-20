from game import GridGame
import gymnasium as gym

class MazeEnvironment:
    def __init__(self, grid_game=GridGame()):


        self.max_steps = 1000
        self.steps_taken = 0

        
