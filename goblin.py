import random
from heapq import heappop, heappush

def manhattan_distance_bad(pos1, pos2):
    """
    - This function calculates an intentionally suboptimal heuristic for the A* algorithm.
    - In the case of this program, we ensure a suboptimal heuristic by adding noise(20-40% error) to the heuristic.
    - The goal of this "bad" heuristic is to make the goblin's pathfinding more "imperfect" so that there's some variance
      in the A* algorithms of the agent and the goblin, making the game more interesting visually.

    :param pos1: position of first agent
    :param pos2: position of second agent
    :return: Manhattan distance between the two agents
    """
    dx = abs(pos1[0] - pos2[0])
    dy = abs(pos1[1] - pos2[1])
    manhattan = dx + dy


    # The reason uniform distribution was used was so that we have a variance in random noise chance
    # This is the main reason the "noise" works, making the goblin stupid
    noise = random.uniform(0.2, 0.4) * manhattan
    return manhattan + noise

def move_goblin_towards_agent(self, random_chance):
    """
    Moves the goblin towards the player agent using a modified A* algorithm with an intentional chance of random movement.
    
    :param self: The GridGame instance for accessing the goblin, player, and grid. 
    :param random_chance: An integer (1-100) defining the percentage probability (e.g., 20 = 20%) 
                          for the goblin to make a random valid move instead of following the heuristic path.
    :return: The updated position of the goblin.
    """

    if random.randint(1, 100) <= random_chance:
        goblin_row, goblin_column = self.goblin_pos
        potential_moves = [
            ([goblin_row - 1, goblin_column], "UP"),
            ([goblin_row + 1, goblin_column], "DOWN"),
            ([goblin_row, goblin_column - 1], "LEFT"),
            ([goblin_row, goblin_column + 1], "RIGHT")
        ]

        valid_moves = [
            cmd for pos, cmd in potential_moves
            if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.cols and self.grid[pos[0]][pos[1]] != "W"
        ]

        if valid_moves:
            return random.choice(valid_moves)
        return None #No random moves

    # A* implementation:
    start = tuple(self.goblin_pos)
    player_position = tuple(self.player_pos)


    open_set = []
    heappush(open_set, (manhattan_distance_bad(start, player_position), 0, start, [start]))

    visited = set()

    while open_set:
        f_score, g_score, current, path = heappop(open_set)

        # If we reached the agent, return only the first move in the path
        if current == player_position:
            if len(path) > 1:
                # Take only the first step from the path
                next_pos = path[1]
                current_pos = self.goblin_pos

                if next_pos[0] < current_pos[0]:
                    return "UP"
                elif next_pos[0] > current_pos[0]:
                    return "DOWN"
                elif next_pos[1] < current_pos[1]:
                    return "LEFT"
                elif next_pos[1] > current_pos[1]:
                    return "RIGHT"
                return None  # Already at goal

        if current in visited:
            continue
        visited.add(current)

        # Explore possible neighbors
        row, column = current
        neighbors = [
            (row - 1, column),  # Up
            (row + 1, column),  # Down
            (row, column - 1),  # Left
            (row, column + 1)  # Right
        ]

        for neighbor in neighbors:
            n_row, n_column = neighbor

            # Check if neighbor is valid
            if (0 <= n_row < self.rows and
                    0 <= n_column < self.cols and
                    self.grid[n_row][n_column] != "W" and
                    neighbor not in visited):
                new_g_score = g_score + 1
                new_f_score = new_g_score + manhattan_distance_bad(neighbor, player_position)
                new_path = path + [neighbor]

                heappush(open_set, (new_f_score, new_g_score, neighbor, new_path))

    # If no path found, the goblin stays in place
    return None
