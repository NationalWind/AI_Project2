import tkinter as tk
from tkinter import messagebox

# Constants
GRID_SIZE = 10
CELL_SIZE = 65
MAX_HEALTH = 100
HEALTH_REDUCTION = 25
HEALTH_RESTORE = 25
ARROW_COUNT = float('inf')

# Scoring Constants
SCORE_PICKUP_GOLD = 5000
SCORE_SHOOT_ARROW = -100
SCORE_AGENT_DIED = -10000
SCORE_CLIMB_OUT = 10
SCORE_ACTION = -10

def split_objects(cell_content):
    objects = []
    i = 0
    while i < len(cell_content):
        if cell_content[i:i+3] == "H_P":  
            objects.append("H_P")
            i += 3
        elif cell_content[i:i+3] == "P_G": 
            objects.append("P_G")
            i += 3
        elif cell_content[i:i+3] == "G_L": 
            objects.append("G_L")
            i += 3
        elif cell_content[i:i+3] == "W_H": 
            objects.append("W_H")
            i += 3
        else:
            objects.append(cell_content[i])
            i += 1
    return objects
    
class Program:
    def __init__(self):
        self.map = self.generate_map()
        self.wumpus_count_map = self.count_wumpuses()


    def generate_map(self):
        base_map = [
            ['-', '-', 'WH_PWW', '-', 'P', '-', '-', 'P_G', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', 'H_P', '-', '-', '-', '-', '-'],
            ['-', 'GH_P', 'WH_P', '-', '-', '-', 'P', '-', '-', '-'],
            ['-', '-', '-', '-', 'P_G', '-', '-', '-', '-', '-'],
            ['H_P', '-', '-', '-', '-', 'W', '-', '-', 'H_P', '-'],
            ['P', '-', 'P', '-', 'P', 'WP_GPH_P', '-', '-', '-', '-'],
            ['-', 'GH_P', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', 'W', '-', '-', '-', '-', 'W', '-', '-'],
            ['A', '-', '-', 'P_G', '-', 'P', '-', '-', '-', '-']
        ]

        percept_map = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        def add_percept(x, y, percept):
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                if percept not in percept_map[x][y]:
                    percept_map[x][y] += percept
    

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell_objects = split_objects(base_map[i][j])
                for obj in cell_objects:
                    if obj == 'W':
                        add_percept(i, j, 'S')     # Add Stench to the Wumpus cell itself
                        add_percept(i-1, j, 'S')  # Stench around Wumpus
                        add_percept(i+1, j, 'S')
                        add_percept(i, j-1, 'S')
                        add_percept(i, j+1, 'S')
                    elif obj == 'P':
                        add_percept(i, j, 'B')     # Add Breeze to the Pit cell itself
                        add_percept(i-1, j, 'B')  # Breeze around Pit
                        add_percept(i+1, j, 'B')
                        add_percept(i, j-1, 'B')
                        add_percept(i, j+1, 'B')
                    elif obj == 'P_G':
                        add_percept(i, j, 'W_H')     # Add Whiff to the Poisonous Gas cell itself
                        add_percept(i-1, j, 'W_H')  # Whiff around Poisonous Gas
                        add_percept(i+1, j, 'W_H')
                        add_percept(i, j-1, 'W_H')
                        add_percept(i, j+1, 'W_H')
                    elif obj == 'H_P':
                        add_percept(i, j, 'G_L')   # Add Glow to the Healing Potions cell itself
                        add_percept(i-1, j, 'G_L') # Glow around Healing Potions
                        add_percept(i+1, j, 'G_L')
                        add_percept(i, j-1, 'G_L')
                        add_percept(i, j+1, 'G_L')

        final_map = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if base_map[i][j] == '-':
                    final_map[i][j] = percept_map[i][j] if percept_map[i][j] else '-'
                else:
                    final_map[i][j] = base_map[i][j] + percept_map[i][j]

        return final_map

    def count_wumpuses(self):
            wumpus_count_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    cell_objects = split_objects(self.map[i][j])
                    wumpus_count_map[i][j] = cell_objects.count('W')
            return wumpus_count_map
    
    def get_cell_info(self, x, y):
        return self.map[x][y]

    def set_cell_info(self, x, y, info):
        self.map[x][y] = info
        
    def update_map_after_wumpus_death(self, x, y):
        # Reduce the count of Wumpuses in the cell
        if self.wumpus_count_map[x][y] > 0:
            self.wumpus_count_map[x][y] -= 1
        print(self.wumpus_count_map[x][y])
        
        # If no more Wumpuses in the cell, remove stench from the Wumpus cell and surrounding cells
        if self.wumpus_count_map[x][y] == 0:
            self.set_cell_info(x, y, self.get_cell_info(x, y).replace('W', ''))
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        cell_info = self.get_cell_info(nx, ny)
                        self.set_cell_info(nx, ny, cell_info.replace('S', ''))

    def update_map_after_grab(self, x, y):
        # Remove glow from the Healing Potions cell
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    cell_info = self.get_cell_info(nx, ny)
                    self.set_cell_info(nx, ny, cell_info.replace('G_L', ''))