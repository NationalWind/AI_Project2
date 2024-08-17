import tkinter as tk
from tkinter import messagebox
from define import *
from agent import *
from bfs import *
from collections import deque


class WumpusWorldGUI:
    def __init__(self, master: tk.Tk, program, agent: Agent):
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

        self.path = []

        self.agent.update_knowledge_base(9, 0)

        self.nextStepQueue = deque([])

        self.display_usage_instructions()
        self.master.after(1000, self.nextStep)

        self.lacdas = [lambda: self.on_grab(), lambda: self.on_heal(), lambda: self.master.destroy(), lambda: self.on_turn_right(), lambda: self.on_turn_left(), lambda: self.on_shoot(), lambda: self.on_move_forward()]

    def display_usage_instructions(self):
        instructions = "Arrow Keys: Turn Left/Right\n" "Enter: Move Forward\n"
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
        if "S" in cell_info:
            self.percept_text_ids["S"] = self.canvas.create_text(y * CELL_SIZE + CELL_SIZE / 4, x * CELL_SIZE + CELL_SIZE / 4, text="S", fill="red", font=("Arial", 8))
        if "B" in cell_info:
            self.percept_text_ids["B"] = self.canvas.create_text(y * CELL_SIZE + 3 * CELL_SIZE / 4, x * CELL_SIZE + CELL_SIZE / 4, text="B", fill="blue", font=("Arial", 8))
        if "W_H" in cell_info:
            self.percept_text_ids["W_H"] = self.canvas.create_text(y * CELL_SIZE + CELL_SIZE / 4, x * CELL_SIZE + 3 * CELL_SIZE / 4, text="W_H", fill="gray", font=("Arial", 8))
        if "G_L" in cell_info:
            self.percept_text_ids["G_L"] = self.canvas.create_text(y * CELL_SIZE + 3 * CELL_SIZE / 4, x * CELL_SIZE + 3 * CELL_SIZE / 4, text="G_L", fill="red", font=("Arial", 8))

        self.health_label.config(text=f"Health: {self.agent.health}")
        self.arrow_label.config(text=f"Arrows: {self.agent.arrows}")
        self.gold_label.config(text=f"Gold: {'Collected' if self.agent.gold_collected else 'Not Collected'}")
        self.points_label.config(text=f"Score: {self.agent.game_points}")
        self.potions_label.config(text=f"Healing Potions: {self.agent.healing_potions}")

    def display_message(self, message):
        self.message_label.config(text=message)

    def on_turn_left(self, event=None):
        self.agent.turn_left()
        self.update_agent_position()

    def on_turn_right(self, event=None):
        self.agent.turn_right()
        self.update_agent_position()

    def on_move_forward(self, event=None):
        result = self.agent.move_forward()
        if result == "gold":
            self.display_message("You have entered a cell with Gold!")
            self.nextStepQueue.append(self.lacdas[0])

        elif result == "healing potion":
            self.display_message("You have entered a cell with Healing Potion!")
            self.nextStepQueue.append(self.lacdas[0])

        self.check_agent_status()

        self.update_grid()
        self.update_agent_position()

        if (self.agent.x, self.agent.y) == (9, 0) and self.agent.isReturning == True:
            self.master.after(2000, self.lacdas[2])

    def move(self, direction):
        idx = {"up": 0, "right": 1, "down": 2, "left": 3}

        # delay?
        diff = idx[self.agent.direction] - idx[direction]
        if diff < 0:
            if -diff < 2:
                for _ in range(-diff):
                    self.nextStepQueue.append(self.lacdas[3])

            else:
                for _ in range(4 + diff):
                    self.nextStepQueue.append(self.lacdas[4])
        else:
            if diff < 2:
                for _ in range(diff):
                    self.nextStepQueue.append(self.lacdas[4])
            else:
                for _ in range(4 - diff):
                    self.nextStepQueue.append(self.lacdas[3])

        nx, ny = self.agent.x, self.agent.y
        if direction == "up":
            nx -= 1
        elif direction == "down":
            nx += 1
        elif direction == "left":
            ny -= 1
        elif direction == "right":
            ny += 1
        if not self.agent.visited[nx][ny] and not isinstance(self.agent.kb.clauses, bool) and self.agent.kb.clauses.has(self.agent.kb.propositions[(nx, ny, "W")]) and self.agent.kb.check_consistency(Not(self.agent.kb.propositions[(nx, ny, "W")])) == "Unknown":
            self.nextStepQueue.append(self.lacdas[5])
        self.nextStepQueue.append(self.lacdas[6])

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
        print("shoot")
        if result == "wumpus killed":
            self.display_message("Scream!!")
        elif result == "missed":
            self.display_message("Missed the shot.")
        self.update_grid()
        return result

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
            if self.agent.healing_potions > 0:
                self.nextStepQueue.append(self.lacdas[1])
            if self.agent.health <= 0:
                messagebox.showinfo("Game Over", "You have been killed by the poisonous gas!")
                self.agent.save_result()
                self.master.quit()

    def nextStep(self):
        if not self.agent.isReturning or (self.agent.x, self.agent.y) != (9, 0):
            if self.nextStepQueue:
                lacda = self.nextStepQueue.popleft()
                if lacda == self.lacdas[5]:
                    res = lacda()
                    if res != "missed":
                        self.nextStepQueue.appendleft(self.lacdas[5])
                else:
                    lacda()

            else:
                # if not self.agent.isReturning:  # self.agent.kb.cnt_known == 100
                #     result = BFS(self.agent)
                #     self.path = trace(result)
                #     self.path.pop()
                #     self.agent.isReturning = True

                if not self.path:
                    result = BFS(self.agent)
                    self.path = trace(result)

                    if self.path:
                        self.path.pop()
                    else:
                        self.agent.isReturning = True
                        result = BFS(self.agent)
                        self.path = trace(result)
                        self.path.pop()

                self.agent.last_positions.append(self.path[-1].state)

                self.move(self.path[-1].action)
                self.path.pop()

            # self.agent.kb.display_knowledge()

        self.master.after(200, self.nextStep)
