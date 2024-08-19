# Constants
GRID_SIZE = 10
CELL_SIZE = 70
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