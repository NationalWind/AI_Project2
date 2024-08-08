class Agent:
    def __init__(self, program):
        self.program = program
        self.health = 100
        self.position = self.find_agent()
        self.direction = (0, 1)  # Initially facing right
        self.has_gold = False
    
    def find_agent(self):
        for row in range(self.program.size):
            for col in range(self.program.size):
                if 'A' in self.program.grid[row][col]:
                    return (row, col)
    
    def move_forward(self):
        row, col = self.position
        dr, dc = self.direction
        nr, nc = row + dr, col + dc
        if 0 <= nr < self.program.size and 0 <= nc < self.program.size:
            self.position = (nr, nc)
            self.check_cell()
    
    def turn_left(self):
        self.direction = (-self.direction[1], self.direction[0])
    
    def turn_right(self):
        self.direction = (self.direction[1], -self.direction[0])
    
    def grab(self):
        row, col = self.position
        if 'G' in self.program.grid[row][col]:
            self.has_gold = True
            self.program.grid[row][col] = self.program.grid[row][col].replace('G', '-')
        if 'H_P' in self.program.grid[row][col]:
            self.health = min(100, self.health + 25)
            self.program.grid[row][col] = self.program.grid[row][col].replace('H_P', '-')
    
    def shoot(self):
        row, col = self.position
        dr, dc = self.direction
        nr, nc = row + dr, col + dc
        if 0 <= nr < self.program.size and 0 <= nc < self.program.size:
            if 'W' in self.program.grid[nr][nc]:
                self.program.grid[nr][nc] = self.program.grid[nr][nc].replace('W', '-')
                self.program.add_percept(nr, nc, 'S')
                print("Scream!")
    
    def climb(self):
        if self.position == self.find_agent():
            return self.has_gold
    
    def check_cell(self):
        row, col = self.position
        cell = self.program.grid[row][col]
        if 'P' in cell:
            print("Agent fell into a pit and died.")
            self.health = 0
        if 'W' in cell:
            print("Agent was killed by the Wumpus.")
            self.health = 0
        if 'P_G' in cell:
            print("Agent was poisoned.")
            self.health -= 25
            if self.health <= 0:
                print("Agent died from poisoning.")
    
    def heal(self):
        if self.health < 100:
            self.health = min(100, self.health + 25)
