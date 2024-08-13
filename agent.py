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
    
class Agent:
    def __init__(self, program):
        self.program = program
        self.x, self.y = GRID_SIZE - 1, 0  # Start position (1,1) in 1-indexed, (9,0) in 0-indexed
        self.actions = []
        self.game_points = 0
        self.health = MAX_HEALTH
        self.gold_collected = False
        self.arrows = ARROW_COUNT
        self.direction = "up"  # Initial direction
        self.healing_potions = 0  # Track healing potions

    def get_current_info(self):
        return self.program.get_cell_info(self.x, self.y)

    def move_forward(self):
        if self.direction == "up" and self.x > 0:
            self.x -= 1
        elif self.direction == "down" and self.x < GRID_SIZE - 1:
            self.x += 1
        elif self.direction == "left" and self.y > 0:
            self.y -= 1
        elif self.direction == "right" and self.y < GRID_SIZE - 1:
            self.y += 1

        action_str = f"({self.y + 1},{GRID_SIZE - self.x}): move forward"
        self.actions.append(action_str)
        self.game_points += SCORE_ACTION

        # Check for Gold and Healing Potions
        cell_info = self.get_current_info()
        objects = split_objects(cell_info)
        if 'G' in objects:
            return "gold"
        elif 'H_P' in cell_info:
            return "healing potion"
        return ""
    
    def turn_left(self):
        directions = ["up", "left", "down", "right"]
        self.direction = directions[(directions.index(self.direction) + 1) % 4]
        action_str = f"({self.y + 1},{GRID_SIZE - self.x}): turn left"
        self.actions.append(action_str)
        self.game_points += SCORE_ACTION

    def turn_right(self):
        directions = ["up", "right", "down", "left"]
        self.direction = directions[(directions.index(self.direction) + 1) % 4]
        action_str = f"({self.y + 1},{GRID_SIZE - self.x}): turn right"
        self.actions.append(action_str)
        self.game_points += SCORE_ACTION

    def grab(self):
        cell_info = self.get_current_info()
        objects = split_objects(cell_info)
        if 'G' in objects:
            self.gold_collected = True
            self.program.set_cell_info(self.x, self.y, cell_info.replace('G', ''))
            action_str = f"({self.y + 1},{GRID_SIZE - self.x}): grab"
            self.actions.append(action_str)
            return "gold"
        elif 'H_P' in cell_info:
            self.healing_potions += 1
            self.program.set_cell_info(self.x, self.y, cell_info.replace('H_P', ''))
            action_str = f"({self.y + 1},{GRID_SIZE - self.x}): grab"
            self.program.update_map_after_grab(self.x, self.y)
            self.actions.append(action_str)
            self.game_points += SCORE_ACTION
            return "healing potion"
        return ""

    def shoot(self):
        self.game_points += SCORE_SHOOT_ARROW
        dx, dy = 0, 0
        if self.direction == "up":
            dx, dy = -1, 0
        elif self.direction == "down":
            dx, dy = 1, 0
        elif self.direction == "left":
            dx, dy = 0, -1
        elif self.direction == "right":
            dx, dy = 0, 1

        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            cell_info = self.program.get_cell_info(nx, ny)
            objects = split_objects(cell_info)
            if 'W' in objects:
                self.program.update_map_after_wumpus_death(nx, ny)
                action_str = f"({ny + 1},{GRID_SIZE - nx}): shoot"
                self.actions.append(action_str)
                return "wumpus killed"
        action_str = f"({ny + 1},{GRID_SIZE - nx}): shoot"
        self.actions.append(action_str)
        return "missed"

    def climb(self):
        if (self.x, self.y) == (GRID_SIZE - 1, 0):  # Starting position
            action_str = f"({self.y + 1},{GRID_SIZE - self.x}): climb"
            self.actions.append(action_str)
            return "climb"
        return "not at start"

    def heal(self):
        if self.healing_potions > 0:  # Check if there are healing potions available
            self.health = min(self.health + HEALTH_RESTORE, MAX_HEALTH)
            self.healing_potions -= 1  # Use one healing potion
            action_str = f"({self.y + 1},{GRID_SIZE - self.x}): heal"
            self.actions.append(action_str)
            return "healed"
        return "no healing potion"

    def check_cell(self):
        cell_info = self.get_current_info()
        objects = split_objects(cell_info)
        print (objects)
        if 'W' in objects:
            return "wumpus"
        elif 'P' in objects:
            return "pit"
        elif 'P_G' in objects:
            self.health -= HEALTH_REDUCTION
            return "poisonous gas"
        return ""

    def save_result(self):
        with open("result1.txt", "w") as f:
            for action in self.actions:
                f.write(f"{action}\n")
            f.write(f"Game points: {self.game_points}\n")

