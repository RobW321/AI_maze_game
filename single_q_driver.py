from q_learning_gridgame import QGridGame
import pygame
import random
import numpy as np
import pickle
import sys
from goblin import move_goblin_towards_agent
from agent import plan_next_move
import matplotlib.pyplot as plt
import csv
import json
from copy import deepcopy


gui_flag = 'gui' in sys.argv              # True = GUI Displayed; False = No GUI
train_flag = "train" in sys.argv          # True = Running Simulation to Train; False = Not Running Simulation to Train
single_maze_flag = "single" in sys.argv   # True = Simulation Will Use A single Maze; False = Maze Will be Regenerated at the Start of Each Episode
not_train_flag = "not_train" in sys.argv  # True = Running to Evaluate a Trained Agent; False = Not Running to Evaluate a Trained Agent

"""ADJUST THESE VALUES TO CHANGE MAZE SIZE"""
rows = 15
cols = 15

game = QGridGame(rows, cols, 14, 0.1, gui_flag)
num_episodes = 10000
epsilon = 1
decay_rate = 0.9999
gamma = 0.9
ACTION_SPACE = ["UP", "DOWN", "LEFT", "RIGHT"]
ACTION_SPACE_INDICES = [0, 1, 2, 3]
BOLD = '\033[1m'
RESET = '\033[0m'


def hash(obs):
    """Hash function that returns a unique state id for the agent
       based on a 5x5 observation window centered on said agent."""
    window = obs.get('window', {})

    cell_values = []
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            cell = window.get((dx, dy))
            if cell is None or not cell.get('in_bounds', False):
                cell_values.append(4)
                continue

            # Determine what's in the cell
            if cell.get('is_wall'):
                cell_value = 1
            elif cell.get('is_exit'):
                cell_value = 2
            elif cell.get('is_goblin'):
                cell_value = 3
            else:
                cell_value = 0

            cell_values.append(cell_value)

    window_hash = 0
    base = 1
    for v in cell_values:
        window_hash += v * base
        base *= 5

    # window_hash uses 5^5 space
    return 5 ** 5 + window_hash

if __name__ == '__main__':
    if train_flag:
        running = True
        max_actions = 1000
        rewards = []
        running_average_reward = []

        for episode in range(num_episodes):
            print(f"Starting Episode {episode + 1}")
            episode_complete = False
            actions_taken = 0
            if single_maze_flag:
                obs, reward = game.single_maze_reset()
            else:
                obs, reward = game.reset()
            total_reward = 0

            while not episode_complete:
                old_state_id = hash(obs)

                # Make an entry for the state in the Q and Eta tables if one doesn't exist
                if old_state_id not in game.q_table.keys():
                    game.q_table[old_state_id] = np.zeros(4)
                    game.eta_table[old_state_id] = np.zeros(4)

                # Take an action
                action = None
                if episode < 100:
                    # Offer the chance for the agent to learn a goal exists
                    action, _ = plan_next_move(game.player_pos, game.exit_pos, game.goblin_pos, grid=game.grid)
                    if action == "UP":
                        action = 0
                    elif action == "DOWN":
                        action = 1
                    elif action == "LEFT":
                        action = 2
                    else:
                        action = 3
                else:
                    if random.random() < epsilon:
                        action = random.choice(ACTION_SPACE_INDICES)
                    else:
                        action = np.argmax(game.q_table[old_state_id])

                # Take the action and get the new state ID
                obs, reward = game.execute(ACTION_SPACE[action])
                total_reward += reward
                new_state_id = hash(obs)
                actions_taken += 1

                # Make an entry in the q and eta tables for this new state if one doesn't exist
                if new_state_id not in game.q_table.keys():
                    game.q_table[new_state_id] = np.zeros(4)
                    game.eta_table[new_state_id] = np.zeros(4)

                # Compute eta for this new state
                eta = 1 / (1 + game.eta_table[new_state_id][action])

                # Compute new Q and Eta values for the old state
                game.q_table[old_state_id][action] = (1 - eta) * game.q_table[old_state_id][action] + eta * (reward + gamma * max(game.q_table[new_state_id]))
                game.eta_table[old_state_id][action] += 1

                # Let the goblin move
                goblin_move = move_goblin_towards_agent(game, 20)
                game.display_move(goblin_move, entity="GOBLIN")

                # Let window be closed if requested
                if gui_flag:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            episode_complete = True
                            running = False

                if game.player_pos == game.exit_pos:
                    print("Goal reached!")
                    episode_complete = True
                if game.player_pos == game.goblin_pos:
                    print("Caught by goblin!")
                    episode_complete = True
                if actions_taken >= max_actions:
                    episode_complete = True
            
            epsilon = epsilon * decay_rate
            rewards.append(total_reward)
            running_average_reward.append(sum(rewards) / (len(rewards)))
            if not running:
                print("Terminating Simulation Early")
                break

        episodes = range(1, len(rewards) + 1)  # gives [1, 2, 3, 4, 5, ...]
        plt.scatter(episodes, running_average_reward, marker='o')
        plt.xlabel("Number of Completed Episodes")
        plt.ylabel("Running Average Reward")
        plt.title(f"Running Average Reward Over {num_episodes:,} Episodes & DR of {decay_rate}")
        plt.grid(True)
        plt.tight_layout()
        # plt.show()


        print("Saving Q-Table!")
        # Save the Q-table dict to a fil
        with open(f'tables/Q_table_Rows={rows}_Cols={cols}_'+str(num_episodes)+'_'+str(decay_rate)+'_Single='+str(single_maze_flag)+'.pickle', 'wb') as fh: 
            pickle.dump(game.q_table, fh, protocol=pickle.HIGHEST_PROTOCOL)
        
        if single_maze_flag:
            # Save the grid used in training
            print("Saving Grid!")
            with open(f'grids/Q_table_Rows={rows}_Cols={cols}_'+str(num_episodes)+'_'+str(decay_rate)+'_Single='+str(single_maze_flag)+'.csv', 'w', newline='') as fh:
                writer = csv.writer(fh)
                writer.writerows(game.grid)

            # Save the original spawn locations used in training
            print ("Saving Spawn Locations!")
            spawn_locations = {
                "exit": game.exit_pos,
                "player_spawn": game.original_player_spawn,
                "goblin_spawn": game.original_goblin_spawn
            }
            with open(f'spawns/Q_table_Rows={rows}_Cols={cols}_'+str(num_episodes)+'_'+str(decay_rate)+'_Single='+str(single_maze_flag)+'.json', "w") as fh:
                json.dump(spawn_locations, fh, indent=4)




    def softmax(x, temp=1.0):
        e_x = np.exp((x - np.max(x)) / temp)
        return e_x / e_x.sum(axis=0)


    if not_train_flag:
        running = True

        # Load the Q-Table
        filename = f'tables/Q_table_Rows={rows}_Cols={cols}_'+str(num_episodes)+'_'+str(decay_rate)+'_Single='+str(single_maze_flag)+'.pickle'
        Q_table = np.load(filename, allow_pickle=True)

        # If trained on a single maze, load the respective maze and spawn locations
        if single_maze_flag:
            # Load Grid
            grid_trained_on = []
            filename = f'grids/Q_table_Rows={rows}_Cols={cols}_'+str(num_episodes)+'_'+str(decay_rate)+'_Single='+str(single_maze_flag)+'.csv'
            with open(filename, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    grid_trained_on.append(row)
            game.grid = grid_trained_on

            # Load Spawns
            filename = f'spawns/Q_table_Rows={rows}_Cols={cols}_'+str(num_episodes)+'_'+str(decay_rate)+'_Single='+str(single_maze_flag)+'.json'
            with open(filename, "r") as fh:
                spawn_locations = json.load(fh)
            
            # Set the game objects fields to the loaded ones
            game.exit_pos = list(spawn_locations["exit"])
            game.player_pos = list(spawn_locations["player_spawn"])
            game.original_player_spawn = deepcopy(game.player_pos)
            game.goblin_pos = list(spawn_locations["goblin_spawn"])
            game.original_goblin_spawn = deepcopy(game.goblin_pos)
            game.dist_to_exit = game.compute_distance_grid(game.grid, tuple(game.exit_pos))
            _, game.optimal_path = plan_next_move(game.player_pos, game.exit_pos, game.goblin_pos, game.grid)

        # Exercise the Q-Table
        for episode in range(10000):
            print(f"Starting Episode {episode + 1}")
            episode_complete = False
            if single_maze_flag:
                obs, reward = game.single_maze_reset()
            else:
                obs, reward = game.reset()


            while not episode_complete:
                state_id = hash(obs)

                # Pick an action
                try:
                    action = np.random.choice(4, p=softmax(Q_table[state_id]))
                except KeyError:
                    action = random.choice(ACTION_SPACE_INDICES)

                # Take the chosen action
                obs, reward = game.execute(ACTION_SPACE[action])

                # Let the goblin move
                goblin_move = move_goblin_towards_agent(game, 20)
                game.display_move(goblin_move, entity="GOBLIN")

                # Let window be closed if requested
                if gui_flag:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            episode_complete = True
                            running = False

                if game.player_pos == game.exit_pos:
                    print("Goal reached!")
                    episode_complete = True
                if game.player_pos == game.goblin_pos:
                    print("Caught by goblin!")
                    episode_complete = True

            if not running:
                print("Terminating Early")
                break



