import tkinter as tk
from tkinter import messagebox
from define import *
from agent import *
from bfs import *
from collections import deque
from PIL import Image, ImageTk


class WumpusWorldGUI:
    def __init__(self, master: tk.Tk, program, agent: Agent):
        self.master = master
        self.master.title("Wumpus World")
        self.canvas = tk.Canvas(master, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE + 50)
        self.canvas.pack(side="left")
        self.program = program
        self.agent = agent
        self.percept_text_ids = {}
        self.percept_images = {}

        # Load percept images
        self.images = {"S": ImageTk.PhotoImage(Image.open("stench.jpg").resize((20, 20))), "B": ImageTk.PhotoImage(Image.open("breezee.jpg").resize((20, 20))), "W_H": ImageTk.PhotoImage(Image.open("gas.png").resize((22, 22))), "G_L": ImageTk.PhotoImage(Image.open("g_l.png").resize((20, 20)))}

        # Status Labels
        self.message_label = tk.Label(master, text="", fg="red")
        self.message_label.pack(side="top", anchor="w", padx=1, pady=10)
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

        self.draw_grid()
        self.update_agent_position()
        self.master.bind("<Left>", self.on_turn_left)
        self.master.bind("<Right>", self.on_turn_right)
        self.master.bind("<Return>", self.on_move_forward)

        self.path = []

        self.agent.update_knowledge_base(9, 0)

        self.nextStepQueue = deque([])

        self.master.after(2, self.nextStep)

        self.lacdas = [lambda: self.on_grab(), lambda: self.on_heal(), lambda: self.master.destroy(), lambda: self.on_turn_right(), lambda: self.on_turn_left(), lambda: self.on_shoot(), lambda: self.on_move_forward()]

    def draw_grid(self):
        self.grid_rects = []  # Store references to the grid rectangles
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                x0 = j * CELL_SIZE
                y0 = i * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill="gray", outline="black")
                row.append(rect)
            self.grid_rects.append(row)

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

        # Update the cell color based on the agent's visited cells
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.agent.visited[i][j]:  # Check if the cell has been visited
                    self.canvas.itemconfig(self.grid_rects[i][j], fill="white")

        # Define the padding (offset) to move the images slightly inside the cell
        padding = 5  # Adjust this value as needed

        # Define the offset for each corner with padding
        corner_offsets = {"top-left": (padding, padding), "top-right": (CELL_SIZE - self.images["S"].width() - padding, padding), "bottom-left": (padding, CELL_SIZE - self.images["S"].height() - padding), "bottom-right": (CELL_SIZE - self.images["S"].width() - padding, CELL_SIZE - self.images["S"].height() - padding)}

        # Calculate image placement for each corner
        if "S" in cell_info:
            self.percept_images["S"] = self.canvas.create_image(y * CELL_SIZE + corner_offsets["top-left"][0], x * CELL_SIZE + corner_offsets["top-left"][1], image=self.images["S"], anchor="nw")  # X position  # Y position  # Anchor to the top-left corner of the image
        if "B" in cell_info:
            self.percept_images["B"] = self.canvas.create_image(y * CELL_SIZE + corner_offsets["top-right"][0], x * CELL_SIZE + corner_offsets["top-right"][1], image=self.images["B"], anchor="nw")  # X position  # Y position  # Anchor to the top-left corner of the image
        if "W_H" in cell_info:
            self.percept_images["W_H"] = self.canvas.create_image(y * CELL_SIZE + corner_offsets["bottom-left"][0], x * CELL_SIZE + corner_offsets["bottom-left"][1], image=self.images["W_H"], anchor="nw")  # X position  # Y position  # Anchor to the top-left corner of the image
        if "G_L" in cell_info:
            self.percept_images["G_L"] = self.canvas.create_image(y * CELL_SIZE + corner_offsets["bottom-right"][0], x * CELL_SIZE + corner_offsets["bottom-right"][1], image=self.images["G_L"], anchor="nw")  # X position  # Y position  # Anchor to the top-left corner of the image

        self.health_label.config(text=f"Health: {self.agent.health}")
        self.arrow_label.config(text=f"Arrows: {self.agent.arrows}")
        self.gold_label.config(text=f"Gold Collected: {self.agent.gold_collected}")
        self.points_label.config(text=f"Score: {self.agent.game_points}")
        self.potions_label.config(text=f"Healing Potions: {self.agent.healing_potions}")

    def display_message(self, message):
        self.message_label.config(text=message, font=("Arial", 14, "bold"), fg="red")
        self.message_label.place(x=300, y=GRID_SIZE * CELL_SIZE + 10)
        self.master.after(500, self.clear_message)

    def clear_message(self):
        self.message_label.config(text="")

    def on_turn_left(self, event=None):
        self.agent.turn_left()
        self.update_grid()
        self.update_agent_position()

    def on_turn_right(self, event=None):
        self.agent.turn_right()
        self.update_grid()
        self.update_agent_position()

    def on_move_forward(self, event=None):
        result = self.agent.move_forward()
        if result == "gold":
            self.nextStepQueue.append(self.lacdas[0])

        elif result == "healing potion":
            self.nextStepQueue.append(self.lacdas[0])

        self.check_agent_status()

        self.update_grid()
        self.update_agent_position()

        # if (self.agent.x, self.agent.y) == (9, 0) and self.agent.isReturning == True:
        #     self.master.after(5, self.lacdas[7])

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
        if not self.agent.visited[nx][ny] and self.agent.kb.check_consistency(self.agent.kb.propositions[(self.agent.x, self.agent.y, "S")]) is True and self.agent.kb.check_consistency(Not(self.agent.kb.propositions[(nx, ny, "W")])) == "Unknown":
            self.nextStepQueue.append(self.lacdas[5])
        self.nextStepQueue.append(self.lacdas[6])

    def on_grab(self):
        result = self.agent.grab()
        if result == "gold":
            self.agent.game_points += SCORE_PICKUP_GOLD
            self.display_message("Gold collected!")
        elif result == "healing potion":
            self.display_message("Healing potion grabbed!")
        self.update_grid()
        return result

    def on_shoot(self):
        result = self.agent.shoot()
        print("shoot")
        if result == "wumpus killed":
            self.display_message("Scream!!")
        elif result == "missed":
            pass
        self.update_grid()
        return result

    def on_climb(self):
        result = self.agent.climb()
        if result == "climb":
            self.agent.game_points += SCORE_CLIMB_OUT
            self.display_message("Exited the cave!")
            self.agent.save_result(self.program.map_file)
            messagebox.showinfo("Win", "You've exited the cave successfully!")
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
            self.agent.save_result(self.program.map_file)
            self.master.quit()
            self.master.destroy()
        elif cell_status == "pit":
            self.display_message("Fell into a pit! You are dead.")
            messagebox.showinfo("Game Over", "You have fallen into a pit!")
            self.agent.game_points += SCORE_AGENT_DIED
            self.agent.save_result(self.program.map_file)
            self.master.quit()
            self.master.destroy()
        elif cell_status == "poisonous gas":
            self.display_message("Entered poisonous gas! Health reduced.")
            if self.agent.healing_potions > 0:
                self.nextStepQueue.append(self.lacdas[1])
            if self.agent.health <= 0:
                messagebox.showinfo("Game Over", "You have been killed by the poisonous gas!")
                self.agent.save_result(self.program.map_file)
                self.master.quit()

    def nextStep(self):
        # Check if the agent should start climbing out
        if (self.agent.x, self.agent.y) == (9, 0) and self.agent.isReturning:
            # Call the climbing method
            self.on_climb()
            return
        if not self.agent.isReturning or (self.agent.x, self.agent.y) != (9, 0):
            if self.nextStepQueue:
                lacda = self.nextStepQueue.popleft()
                if lacda == self.lacdas[5]:
                    res = lacda()
                    if res != "missed":
                        self.nextStepQueue.appendleft(self.lacdas[5])
                elif lacda == self.lacdas[0]:
                    res = lacda()
                    if res != "":
                        self.nextStepQueue.appendleft(self.lacdas[0])
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
                        if (self.agent.x, self.agent.y) == (9, 0):
                            self.on_climb()
                            return
                        result = BFS(self.agent)
                        self.path = trace(result)
                        if not self.path:
                            messagebox.showinfo("Game Over", "Cannot Return. You will be killed by poisonous gas")
                            self.agent.save_result(self.program.map_file)
                            self.master.quit()
                            self.master.destroy()
                            return
                        self.path.pop()

                self.agent.last_positions.append(self.path[-1].state)

                self.move(self.path[-1].action)
                self.path.pop()

            # self.agent.kb.display_knowledge()

        self.master.after(2, self.nextStep)
