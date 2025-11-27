import heapq

def plan_next_move(player_pos, goal, goblin_pos, grid=None, fear_weight=7.0):
    rows = len(grid)
    cols = len(grid[0])

    start = tuple(player_pos)
    goal = tuple(goal)
    goblin_pos = tuple(goblin_pos) # addition ----------------

    # Moves → (delta_row, delta_col, command_string)
    moves = [
        (-1, 0, "UP"),
        (1, 0, "DOWN"),
        (0, -1, "LEFT"),
        (0, 1, "RIGHT")
    ]

    # Priority queue for A*
    pq = []
    heapq.heappush(pq, (0, start))  # (priority, position)

    came_from = {start: None}
    cost_so_far = {start: 0}

    # def heuristic(a, b):
    #     # Manhattan distance
    #     return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def heuristic(node): # addition ----------------
        # Goal attraction (standard Manhattan)
        h_goal = abs(node[0] - goal[0]) + abs(node[1] - goal[1])

        # Goblin avoidance (inverse distance)
        gdist = abs(node[0] - goblin_pos[0]) + abs(node[1] - goblin_pos[1])

        # Make danger large when goblin is close
        h_goblin = fear_weight * (1 / (gdist + 1))

        return h_goal + h_goblin

    while pq:
        _, current = heapq.heappop(pq)

        if current == goal:
            break

        for dr, dc, cmd in moves:
            nr = current[0] + dr
            nc = current[1] + dc
            nxt = (nr, nc)

            # Check bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            # Check wall
            if grid[nr][nc] == "W":
                continue

            new_cost = cost_so_far[current] + 1

            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]: 
                cost_so_far[nxt] = new_cost
                # priority = new_cost + heuristic(nxt, goal
                priority = new_cost + heuristic(nxt) # addition ----------------
                heapq.heappush(pq, (priority, nxt))
                came_from[nxt] = current

    # If goal unreachable
    if goal not in came_from:
        return None  # or choose a random safe move?

    # Reconstruct path backwards
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.reverse()

    # Determine next step
    next_row, next_col = path[0]

    # Convert next position → command
    r, c = player_pos

    if next_row == r - 1:
        return "UP"
    if next_row == r + 1:
        return "DOWN"
    if next_col == c - 1:
        return "LEFT"
    if next_col == c + 1:
        return "RIGHT"

    return None