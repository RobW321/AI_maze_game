# Maze AI Project

This repository contains a grid-based maze navigation system built with Pygame, where an agent navigates through a maze toward a goal using the A* search algorithm. The project also includes keyboard control functionality and an `execute` function to step the agent forward.

## Game Objective

Navigate the agent(in yellow) from the left side of the maze to the red exit on the right side while avoiding the green agent.

## Features

* **Pygame-based visualization** of a maze grid.
* **Agent navigation** through free cells while avoiding obstacles.
* **A* search implementation** using Manhattan distance as the heuristic.
* **Supports both autonomous navigation and manual control**.
* **Step-by-step execution** of agent moves via the provided `execute` function.

## File Overview

* `main.py` – Initializes the game window, draws the grid, updates frames, and handles input.
* `agent.py` – Defines the A* implementation for the agent's movement.
* `goblin.py` – Defines the A* implementation for the goblin's movement.
* `Q_learning.py (maybe)` – Defines the Q_learning algorithm for the agent's moevemnt

## How It Works

### A* Search

The agent uses A* to plan a path from its current position to the goal located at the **bottom-right corner of the grid**. The algorithm:

* Uses **Manhattan distance** as the heuristic.
* Avoids obstacles when expanding neighbors.
* Returns a sequence of grid positions representing the shortest path.
* The agent selects the **next step** from this path and returns it via `plan_next_move()`.


## Running the Project

### Requirements

```
Python 3.x
pygame
```

Install dependencies:

```
pip install pygame
```

Run the game:

```
python main.py
```

A window will appear showing the maze, agent, and goal.

## Project Structure

```
├── game.py
├── agent.py
├── goblin.py
├── q_learning.py
└── README.md
```

## Customization

You can modify:

* Maze layout in `maze.py`
* Agent behavior in `agent.py`
* Rendering colors, grid size, and speed in `main.py`


