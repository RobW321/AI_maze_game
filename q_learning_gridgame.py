from game import GridGame
from collections import deque
from agent import plan_next_move
from copy import deepcopy


class QGridGame(GridGame):
    def __init__(self, rows=50, cols=50, cell_size=14, render_delay=0.1, gui=True):
        super(QGridGame, self).__init__(rows=rows, cols=cols, cell_size=cell_size, render_delay=render_delay, gui=gui)
        # Create the Q-Table and Eta Table
        self.q_table = {}
        self.eta_table = {}

        self.original_player_spawn = deepcopy(self.player_pos)
        self.original_goblin_spawn = deepcopy(self.goblin_pos)

        self.dist_to_exit = self.compute_distance_grid(self.grid, tuple(self.exit_pos))
        _, self.optimal_path = plan_next_move(self.player_pos, self.exit_pos, self.goblin_pos, self.grid)
    

    def _get_observation(self):
        """Get Observation With 5x5 Window Centered on Agent"""
        player_x, player_y = self.player_pos
        window = {}
        goblin_in_window = False

        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                cell_x, cell_y = player_x + dx, player_y + dy

                # Check if cell is within bounds
                if 0 <= cell_x < self.rows and 0 <= cell_y < self.cols:
                    window[(dx, dy)] = {
                        'is_wall': self.grid[cell_x][cell_y] == "W",
                        'is_goblin': [cell_x, cell_y] == self.goblin_pos,
                        'is_exit': [cell_x, cell_y] == self.exit_pos,
                        'in_bounds': True
                        }
                    if [cell_x, cell_y] == self.goblin_pos:
                        goblin_in_window = True
                else:
                    window[(dx, dy)] = {
                        'is_wall': False,
                        'is_goblin': False,
                        'is_exit': False,
                        'in_bounds': False
                    }
        
        obs = {
            'player_pos': self.player_pos,
            'goblin_pos': self.goblin_pos,
            'exit_pos': self.exit_pos,
            'window': window,
            'at_goblin': window[(0, 0)]['is_goblin'],
            'at_exit': window[(0, 0)]['is_exit']
        }
        return obs, goblin_in_window
    
    
    def get_goblin_observation(self):
        """Get Observation With 5x5 Window Centered on Goblin"""
        goblin_x, goblin_y = self.goblin_pos
        window = {}
        player_in_window = False

        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                cell_x, cell_y = goblin_x + dx, goblin_y + dy

                # Check if cell is within bounds
                if 0 <= cell_x < self.rows and 0 <= cell_y < self.cols:
                    window[(dx, dy)] = {
                        'is_wall': self.grid[cell_x][cell_y] == "W",
                        'is_player': [cell_x, cell_y] == self.player_pos,
                        'is_exit': [cell_x, cell_y] == self.exit_pos,
                        'in_bounds': True
                        }
                    if [cell_x, cell_y] == self.goblin_pos:
                        player_in_window = True
                else:
                    window[(dx, dy)] = {
                        'is_wall': False,
                        'is_player': False,
                        'is_exit': False,
                        'in_bounds': False
                    }
        
        obs = {
            'player_pos': self.player_pos,
            'goblin_pos': self.goblin_pos,
            'exit_pos': self.exit_pos,
            'window': window,
            'at_player': window[(0, 0)]['is_player'],
            'at_exit': window[(0, 0)]['is_exit']
        }
        return obs, player_in_window
    
        
    def execute(self, command, entity="PLAYER"):
        """Executes command on the given entity. In practice, this function is
           only ever used for the player, but it defined this way to override
           the super class' execute function. Returns the reward recieved for
           taking that action. The reward is calculated from distance to the exit,
           proximity to the optimal path out, proximity to the goblin, and
           whether or not the agent is in a terminal state."""
        reward = 0

        old_player_pos = self.player_pos
        super().execute(command, entity=entity)
        obs, goblin_nearby = self._get_observation()

        if goblin_nearby:
            reward -= 0.5
        else:
            reward += 0.5

        # Check for a terminal state
        if self.player_pos == self.exit_pos:
            return obs, 10000.0
        if self.player_pos == self.goblin_pos:
            return obs, -1000.0

        # Optimal Path Reward

        old_dist = self.dist_to_exit[old_player_pos[0]][old_player_pos[1]]
        new_dist = self.dist_to_exit[self.player_pos[0]][self.player_pos[1]]

        # 1. Distance-based reward
        if new_dist < old_dist:
            reward += 1.0
        elif new_dist > old_dist:
            reward -= 1.0

        # 2. Optimal path reward
        if tuple(self.player_pos) in self.optimal_path:
            reward += 2.0
        else:
            reward -= 2.0

        return obs, reward
    

    def goblin_execute(self, command):
        """Has the goblin execute the given command. Returns the reward recieved
           for taking that action. Reward is calculated based on proximity to
           the player and terminal states."""
        reward = 0

        self.display_move(command, entity="GOBLIN")
        obs, player_nearby = self.get_goblin_observation()

        if player_nearby:
            reward += 10

        # Check for a terminal state
        if self.goblin_pos == self.player_pos:
            return obs, 10000.0
        
        return obs, reward


    def reset(self):
        """Used to completely reset the maze at the end of an episode.
           Generates a new maze and picks new spawn tiles for the gaetn, goblin,
           and exit. Also calculates a new optimal path to the exit and distance
           grid. Returns the agent observation for its initial state and a reward
           of zero."""

        # Player position
        self.pos = [0, 0]

        while True:
            self.grid = self._generate_maze()
            self.player_pos = self._find_spawn()
            self.exit_pos = self._place_exit()
            self.goblin_pos = self._place_goblin()

            if self._validate_world():
                break   # valid maze
        self.optimal_path = plan_next_move(self.player_pos, self.exit_pos, self.goblin_pos, self.grid)

        # Precompute shortest distances from every cell to the exit (used for shaping)
        # store on self for the driver to use
        try:
            self.dist_to_exit = self.compute_distance_grid(self.grid, tuple(self.exit_pos))
        except Exception:
            # fallback: fill with None grid if extreme error
            self.dist_to_exit = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        return self._get_observation()[0], 0
    

    def single_maze_reset(self):
        """Used to reposition the agent and goblin within the 
           maze at the end of an episode. Returns the agent 
           observation for its initial state and a reward
           of zero."""
        self.player_pos = deepcopy(self.original_player_spawn)
        self.goblin_pos = deepcopy(self.original_goblin_spawn)
        return self._get_observation()[0], 0

    
    def compute_distance_grid(self, grid, goal):
            """Computes a grid detailing the length of the shortest
               path from every cell to the exit. Returns 
               dist[r][c] = shortest path length from [r,c] to goal,
               or None if unreachable."""
            rows, cols = len(grid), len(grid[0])
            dist = [[None for _ in range(cols)] for _ in range(rows)]
            q = deque()
            gr, gc = goal

            # Quick failsafe to ensure the goal isn't a wall. Should never happen
            if grid[gr][gc] == "W":
                return dist
            
            dist[gr][gc] = 0
            q.append((gr, gc))

            while q:
                r, c = q.popleft()
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "W" and dist[nr][nc] is None:
                        dist[nr][nc] = dist[r][c] + 1
                        q.append((nr, nc))
            return dist



