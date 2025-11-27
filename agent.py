import heapq

def plan_next_move(player_pos, goal, goblin_pos, grid, fear_weight=10, danger_zone=5):
    """
    Returns the next move for the agent using A* with a fear heuristic.
    player_pos: [row, col]
    goal: [row, col]
    goblin_pos: [row, col]
    grid: 2D list of 'F' (floor) and 'W' (wall)
    fear_weight: multiplier for goblin avoidance
    danger_zone: radius around goblin considered dangerous
    """

    rows = len(grid)
    cols = len(grid[0])
    start = tuple(player_pos)
    goal = tuple(goal)

    # represents all four directions agent can move as well as their row/col changes
    directions = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]

    # Priority queue for A*
    pq = []
    heapq.heappush(pq, (0, start))

    # Keep track of the path
    came_from = {start: None}

    # Cost from start to current node
    cost_so_far = {start: 0}

    while pq:
        penalty, current = heapq.heappop(pq)

        # Goal reached
        if current == goal:
            break

        # Loop through possible directions
        for dr, dc, cmd in directions:
            nr, nc = current[0] + dr, current[1] + dc
            nxt = (nr, nc)

            # Check bounds and walls
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == "W":
                continue

            # Calculate new cost
            new_cost = cost_so_far[current] + 1

            # If neighbor not visited yet or this path to neighbor is better then record it
            if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                cost_so_far[nxt] = new_cost

                # Heuristic for manhattan distance from goal
                h_goal = abs(nr - goal[0]) + abs(nc - goal[1])

                # Heuristic for goblin avoidance
                goblin_distance = abs(nr - goblin_pos[0]) + abs(nc - goblin_pos[1])

                # Increases heuristic penalty if within danger zone
                h_goblin = fear_weight * max(0, danger_zone - goblin_distance)

                # Total penalty
                penalty = new_cost + h_goal + h_goblin
                heapq.heappush(pq, (penalty, nxt))
                came_from[nxt] = current

    # If goal unreachable
    if goal not in came_from:
        return None

    # Reconstruct path
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.reverse()

    next_row, next_col = path[0]
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
