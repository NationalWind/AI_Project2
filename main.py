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

def transfer_base_map(base_map):
    conversion_dict = {
        'W': 'WU',
        'P': 'PI',
        'G': 'GO'
    }
    converted_map = [[conversion_dict.get(cell, cell) for cell in row] for row in base_map]
    return converted_map

class Program:
    def __init__(self):
        self.map = self.generate_map()

    def generate_map(self):
        ori_map = [
            ['-', '-', 'W', '-', 'P', '-', '-', 'P_G', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', 'H_P', '-', '-', '-', '-', '-'],
            ['-', 'G', 'WH_P', '-', '-', '-', 'P', '-', '-', '-'],
            ['-', '-', '-', '-', 'P_G', '-', '-', '-', '-', '-'],
            ['H_P', '-', '-', '-', '-', 'W', '-', '-', 'H_P', '-'],
            ['P', '-', 'P', '-', 'P', '-', '-', '-', '-', '-'],
            ['-', 'G', '-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', 'W', '-', '-', '-', '-', 'W', '-', '-'],
            ['A', '-', '-', 'P_G', '-', 'P', '-', '-', '-', '-']
        ]
        base_map = transfer_base_map(ori_map)

        percept_map = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        def add_percept(x, y, percept):
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                if percept not in percept_map[x][y]:
                    percept_map[x][y] += percept

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if base_map[i][j] == 'WU':
                    add_percept(i, j, 'S')     # Add Stench to the Wumpus cell itself
                    add_percept(i-1, j, 'S')  # Stench around Wumpus
                    add_percept(i+1, j, 'S')
                    add_percept(i, j-1, 'S')
                    add_percept(i, j+1, 'S')
                elif base_map[i][j] == 'PI':
                    add_percept(i, j, 'B')     # Add Breeze to the Pit cell itself
                    add_percept(i-1, j, 'B')  # Breeze around Pit
                    add_percept(i+1, j, 'B')
                    add_percept(i, j-1, 'B')
                    add_percept(i, j+1, 'B')
                elif base_map[i][j] == 'P_G':
                    add_percept(i, j, 'W_H')     # Add Whiff to the Poisonous Gas cell itself
                    add_percept(i-1, j, 'W_H')  # Whiff around Poisonous Gas
                    add_percept(i+1, j, 'W_H')
                    add_percept(i, j-1, 'W_H')
                    add_percept(i, j+1, 'W_H')
                elif base_map[i][j] == 'H_P':
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

    def get_cell_info(self, x, y):
        return self.map[x][y]

    def set_cell_info(self, x, y, info):
        self.map[x][y] = info
        
    def update_map_after_wumpus_death(self, x, y):
        # Remove stench from the Wumpus cell and surrounding cells
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
        if 'GO' in cell_info:
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
        if 'GO' in cell_info:
            self.gold_collected = True
            self.program.set_cell_info(self.x, self.y, cell_info.replace('GO', ''))
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
        if self.arrows > 0:
            self.arrows -= 1
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
                if 'WU' in self.program.get_cell_info(nx, ny):
                    self.program.set_cell_info(nx, ny, self.program.get_cell_info(nx, ny).replace('W', ''))
                    self.program.update_map_after_wumpus_death(nx, ny)
                    action_str = f"({ny + 1},{GRID_SIZE - nx}): shoot"
                    self.actions.append(action_str)
                    return "wumpus killed"
            action_str = f"({ny + 1},{GRID_SIZE - nx}): shoot"
            self.actions.append(action_str)
            self.game_points += SCORE_SHOOT_ARROW
            return "missed"
        return "no arrows"

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
        if 'WU' in cell_info:
            return "wumpus"
        elif 'PI' in cell_info:
            return "pit"
        elif 'P_G' in cell_info:
            self.health -= HEALTH_REDUCTION
            return "poisonous gas"
        return ""

    def save_result(self):
        with open("result1.txt", "w") as f:
            for action in self.actions:
                f.write(f"{action}\n")
            f.write(f"Game points: {self.game_points}\n")


class WumpusWorldGUI:
    def __init__(self, master, program, agent):
        self.master = master
        self.master.title("Wumpus World")
        self.canvas = tk.Canvas(master, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
        self.canvas.pack(side="left")
        self.program = program
        self.agent = agent
        self.percept_text_ids = {}

        # Status Labels
        self.message_label = tk.Label(master, text="", fg="blue")
        self.message_label.pack(side="top", anchor="w", padx=10, pady=10)
        self.health_label = tk.Label(master, text=f"Health: {self.agent.health}", fg="green")
        self.health_label.pack(side="top", anchor="w", padx=10, pady=10)
        self.arrow_label = tk.Label(master, text=f"Arrows: {self.agent.arrows}", fg="purple")
        self.arrow_label.pack(side="top", anchor="w", padx=10, pady=10)
        self.gold_label = tk.Label(master, text="Gold: Not Collected", fg="gold")
        self.gold_label.pack(side="top", anchor="w", padx=10, pady=10)
        self.points_label = tk.Label(master, text=f"Score: {self.agent.game_points}", fg="black")
        self.points_label.pack(side="top", anchor="w", padx=10, pady=10)
        self.potions_label = tk.Label(master, text=f"Healing Potions: {self.agent.healing_potions}", fg="orange")
        self.potions_label.pack(side="top", anchor="w", padx=10, pady=10)

        # Control Buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.grab_button = tk.Button(self.button_frame, text="Grab (G)", command=self.on_grab)
        self.grab_button.pack(pady=5)
        self.shoot_button = tk.Button(self.button_frame, text="Shoot (S)", command=self.on_shoot)
        self.shoot_button.pack(pady=5)
        self.climb_button = tk.Button(self.button_frame, text="Climb (C)", command=self.on_climb)
        self.climb_button.pack(pady=5)
        self.heal_button = tk.Button(self.button_frame, text="Heal (H)", command=self.on_heal)
        self.heal_button.pack(pady=5)

        self.draw_grid()
        self.update_agent_position()
        self.master.bind("<Left>", self.on_turn_left)
        self.master.bind("<Right>", self.on_turn_right)
        self.master.bind("<Return>", self.on_move_forward)
        
        self.display_usage_instructions()
        
    def display_usage_instructions(self):
        instructions = (
            "Arrow Keys: Turn Left/Right\n"
            "Enter: Move Forward\n"
        )
        self.message_label.config(text=instructions)

    def draw_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x0 = j * CELL_SIZE
                y0 = i * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                # Optional: Add additional grid lines or other decorations if needed.

    def update_agent_position(self):
        self.canvas.delete("agent")
        cx, cy = (self.agent.y + 0.5) * CELL_SIZE, (self.agent.x + 0.5) * CELL_SIZE
        size = 10

        if self.agent.direction == "up":
            points = [cx, cy - size, cx - size, cy + size, cx + size, cy + size]
        elif self.agent.direction == "down":
            points = [cx, cy + size, cx - size, cy - size, cx + size, cy - size]
        elif self.agent.direction == "left":
            points = [cx - size, cy, cx + size, cy - size, cx + size, cy + size]
        elif self.agent.direction == "right":
            points = [cx + size, cy, cx - size, cy - size, cx - size, cy + size]

        self.canvas.create_polygon(points, fill="blue", tag="agent")

    def clear_percepts(self):
        for text_id in self.percept_text_ids.values():
            self.canvas.delete(text_id)
        self.percept_text_ids.clear()

    def update_grid(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.update_agent_position()
        self.clear_percepts()
        cell_info = self.agent.get_current_info()
        x, y = self.agent.x, self.agent.y
        if 'S' in cell_info:
            self.percept_text_ids['S'] = self.canvas.create_text(y * CELL_SIZE + CELL_SIZE / 4, x * CELL_SIZE + CELL_SIZE / 4,
                                                                 text='S', fill="red", font=("Arial", 8))
        if 'B' in cell_info:
            self.percept_text_ids['B'] = self.canvas.create_text(y * CELL_SIZE + 3 * CELL_SIZE / 4, x * CELL_SIZE + CELL_SIZE / 4,
                                                                 text='B', fill="blue", font=("Arial", 8))
        if 'W_H' in cell_info:
            self.percept_text_ids['W_H'] = self.canvas.create_text(y * CELL_SIZE + CELL_SIZE / 4, x * CELL_SIZE + 3 * CELL_SIZE / 4,
                                                                 text='W_H', fill="gray", font=("Arial", 8))
        if 'G_L' in cell_info:
            self.percept_text_ids['G_L'] = self.canvas.create_text(y * CELL_SIZE + 3 * CELL_SIZE / 4, x * CELL_SIZE + 3 * CELL_SIZE / 4,
                                                                   text='G_L', fill="red", font=("Arial", 8))

        self.health_label.config(text=f"Health: {self.agent.health}")
        self.arrow_label.config(text=f"Arrows: {self.agent.arrows}")
        self.gold_label.config(text=f"Gold: {'Collected' if self.agent.gold_collected else 'Not Collected'}")
        self.points_label.config(text=f"Score: {self.agent.game_points}")
        self.potions_label.config(text=f"Healing Potions: {self.agent.healing_potions}")

    def display_message(self, message):
        self.message_label.config(text=message)

    def on_turn_left(self, event):
        self.agent.turn_left()
        self.update_agent_position()

    def on_turn_right(self, event):
        self.agent.turn_right()
        self.update_agent_position()

    def on_move_forward(self, event):
        result = self.agent.move_forward()
        if result == "gold":
            self.display_message("You have entered a cell with Gold!")
        elif result == "healing potion":
            self.display_message("You have entered a cell with Healing Potion!")
        self.check_agent_status()
        self.update_grid()
        self.update_agent_position()


    def on_grab(self):
        result = self.agent.grab()
        if result == "gold":
            self.agent.game_points += SCORE_PICKUP_GOLD
            self.display_message("Gold collected!")
        elif result == "healing potion":
            self.display_message("Healing potion grabbed!")
        else:
            self.display_message("Nothing to grab here.")
        self.update_grid()

    def on_shoot(self):
        result = self.agent.shoot()
        if result == "wumpus killed":
            self.display_message("Scream!!")
        elif result == "missed":
            self.display_message("Missed the shot.")
        self.update_grid()

    def on_climb(self):
        result = self.agent.climb()
        if result == "climb":
            self.agent.game_points += SCORE_CLIMB_OUT
            self.display_message("Exited the cave!")
            self.agent.save_result()
            messagebox.showinfo("Game Over", "You've exited the cave successfully!")
            self.master.quit()
        else:
            self.display_message("Not at the starting position.")

    def on_heal(self):
        result = self.agent.heal()
        if result == "healed":
            self.display_message("Health restored!")
        else:
            self.display_message("No healing potion to use.")
        self.update_grid()

    def check_agent_status(self):
        cell_status = self.agent.check_cell()
        if cell_status == "wumpus":
            self.display_message("Encountered a Wumpus! You are dead.")
            messagebox.showinfo("Game Over", "You have been killed by the Wumpus!")
            self.agent.game_points += SCORE_AGENT_DIED
            self.agent.save_result()
            self.master.quit()
        elif cell_status == "pit":
            self.display_message("Fell into a pit! You are dead.")
            messagebox.showinfo("Game Over", "You have fallen into a pit!")
            self.agent.game_points += SCORE_AGENT_DIED
            self.agent.save_result()
            self.master.quit()
        elif cell_status == "poisonous gas":
            self.display_message("Entered poisonous gas! Health reduced.")
            if self.agent.health <= 0:
                messagebox.showinfo("Game Over", "You have been killed by the poisonous gas!")
                self.agent.save_result()
                self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    program = Program()
    agent = Agent(program)
    app = WumpusWorldGUI(root, program, agent)
    root.mainloop()
