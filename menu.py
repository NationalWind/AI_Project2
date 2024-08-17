import tkinter as tk
from tkinter import messagebox
from program import Program 
from agent import Agent      
from WumpusWorldGUI import WumpusWorldGUI  


maps = ["map1.txt", "map2.txt", "map3.txt", "map4.txt", "map5.txt"]

def start_game(map_file):
    try:
        # Initialize the Program object with the selected map file
        print(f"Initializing Program with map: {map_file}")
        program = Program(map_file)
        
        # Check if the map is loaded correctly
        if program.map is None or len(program.map) == 0:
            raise ValueError("Unable to read the map from the file.")
        print("Map successfully loaded.")
        print(program.map)
        
        # Initialize the Agent object with the Program
        print("Initializing Agent.")
        agent = Agent(program)
        
        # Display the agent's initial knowledge
        agent.kb.display_knowledge()

        # Create a new GUI window and start the game
        print("Initializing GUI.")
        root = tk.Toplevel()
        app = WumpusWorldGUI(root, program, agent)
        root.mainloop()

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred while starting the game: {e}")

def main_menu():
    root = tk.Tk()
    root.title("Wumpus World Game Menu")
    root.geometry("300x300")  # Adjusted size for a more compact window

    # Create a title label
    title_label = tk.Label(root, text="Select Map", font=("Arial", 16))  # Smaller font for title
    title_label.pack(pady=10)

    # Create buttons to select map files
    for i, map_file in enumerate(maps):
        map_label = f"Map {i + 1}"  # Create label like "Map 1", "Map 2", etc.
        map_button = tk.Button(root, text=map_label, font=("Arial", 12), width=20, height=1)
        map_button.config(command=lambda m=map_file: start_game(m))
        map_button.pack(pady=5)  # Reduced padding

    # Create an exit button
    exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit, width=20, height=1)  # Reduced height and font size
    exit_button.pack(pady=10)

    # Run the main loop of the interface
    root.mainloop()

# Run the main menu
main_menu()
