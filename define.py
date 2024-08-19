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

def remove_w_not_in_h_sequence(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == 'W':
            # Check if the W is part of a _H sequence
            if i > 0 and i < len(s) - 1 and s[i-1] == '_' and s[i+1] == 'H':
                result.append('W')  # Keep this W
            else:
                # Check if W is followed by a _H sequence
                if (i < len(s) - 2 and s[i+1] == '_' and s[i+2] == 'H'):
                    result.append('W')  # Keep W if it's followed by _H
                # If W is not part of a _H sequence, do not add it to the result
        else:
            result.append(s[i])
        i += 1
    return ''.join(result)

def remove_g_not_in_l_sequence(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] == 'G':
            # Check if G is part of _L sequence
            if i > 0 and i < len(s) - 1 and s[i-1] == '_' and s[i+1] == 'L':
                result.append('G')  # Keep this G
            # Check if G is part of G_L sequence
            elif i < len(s) - 2 and s[i+1] == '_' and s[i+2] == 'L':
                result.append('G')  # Keep this G
            else:
                # Skip this G because it's not part of _L or G_L
                pass
        else:
            result.append(s[i])
        i += 1
    return ''.join(result)