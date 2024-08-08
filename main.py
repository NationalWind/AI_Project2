from program import Program
from agent import Agent

def main():
    program = Program('map1.txt')
    agent = Agent(program)
    
    program.display_grid()
    
    # Example agent actions
    agent.move_forward()
    agent.turn_left()
    agent.move_forward()
    agent.grab()
    agent.shoot()
    agent.climb()

if __name__ == "__main__":
    main()
