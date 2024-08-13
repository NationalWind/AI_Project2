import tkinter as tk
from tkinter import messagebox
from program import Program
from agent import Agent
from WumpusWorldGUI import WumpusWorldGUI


if __name__ == "__main__":
    root = tk.Tk()
    program = Program()
    agent = Agent(program)
    app = WumpusWorldGUI(root, program, agent)
    root.mainloop()
