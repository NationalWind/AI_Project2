class Program:
    def __init__(self, filename):
        self.grid = []
        self.size = 0
        self.read_map(filename)
        self.update_percepts()
    
    def read_map(self, filename):
        with open(filename, 'r') as file:
            self.size = int(file.readline().strip())
            for line in file:
                self.grid.append(line.strip().split('.'))
    
    def update_percepts(self):
        for row in range(self.size):
            for col in range(self.size):
                if 'W' in self.grid[row][col]:
                    self.add_percept(row, col, 'S')
                if 'P' in self.grid[row][col]:
                    self.add_percept(row, col, 'B')
                if 'P_G' in self.grid[row][col]:
                    self.add_percept(row, col, 'W_H')
                if 'H_P' in self.grid[row][col]:
                    self.add_percept(row, col, 'G_L')
    
    def add_percept(self, row, col, percept):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                if '-' in self.grid[nr][nc]:
                    self.grid[nr][nc] = percept
                else:
                    self.grid[nr][nc] += f"+{percept}"
    
    def display_grid(self):
        for row in self.grid:
            print('.'.join(row))
