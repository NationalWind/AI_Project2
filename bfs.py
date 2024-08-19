from collections import deque
from knowledgeBase import KnowledgeBase
from sympy import Not, symbols
from agent import Agent


class Node:
    def __init__(self, action, state: tuple[int, int, int], path_cost, parent):
        self.action = action
        self.state = state
        self.path_cost = path_cost
        self.parent = parent

    def __lt__(self, other):
        return self.path_cost < other.path_cost


def BFS(agent: Agent):
    print(agent.cnt_visited)
    node = start_node = Node(None, (agent.x, agent.y, agent.health), 0, None)
    frontier = deque()
    frontier.append(node)
    reached = [[None] * 10 for _ in range(10)]
    results = []
    while frontier:
        node = frontier.popleft()
        if agent.isReturning:
            print(node.state)
        if not agent.visited[node.state[0]][node.state[1]]:  # 100
            continue
        for child in expand(node, agent):
            sx, sy, shealth = child.state
            if agent.isReturning:  # 100
                if (sx, sy) == (9, 0):
                    return child
            else:
                if not agent.visited[sx][sy] and agent.kb.check_consistency(agent.kb.propositions[(sx, sy, "P")]) == "Unknown":  # and not agent.kb.isKnown((sx, sy))

                    # if Not(agent.kb.propositions["W"]) in agent.kb.clauses and Not(agent.kb.propositions["P_G"]) in agent.kb.clauses:
                    if agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "W")])) is True and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P_G")])) is True and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P")])) is True:
                        return child
                    elif ((agent.healing_potions > 0 and shealth >= 50) or shealth >= 75) and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P")])) is True:
                        results.append(("a", child))
                    elif agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P_G")])) is True and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P")])) is True:
                        results.append(("b", child))
                    elif ((agent.healing_potions > 0 and shealth >= 50) or shealth >= 75) and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P")])) is True:  # has considered wumpus
                        results.append(("c", child))
                    elif (agent.healing_potions > 0 and shealth >= 50) or shealth >= 75:  # has considered wumpus
                        results.append(("d", child))
            if reached[sx][sy] is None:
                reached[sx][sy] = child
                if agent.isReturning or (((agent.healing_potions > 0 and shealth >= 50) or shealth >= 75) and child.path_cost <= 3):
                    frontier.append(child)

    if results:
        results.sort()
        print("THIS")
        if results[0][0] == "d":
            if agent.cnt_visited >= 50:
                return None
        return results[0][1]
    else:
        print("RETURNINGGGG")
        return None


def expand(node, agent: Agent, for_start=False) -> list[Node]:
    children = []
    x, y, health = node.state
    movs = [(-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")]
    for mov in movs:
        nx, ny = x + mov[0], y + mov[1]
        if 0 <= nx < 10 and 0 <= ny < 10:
            child = Node(mov[2], (nx, ny, health - (25 if agent.kb.check_consistency(agent.kb.propositions[(nx, ny, "P_G")]) is True else 0)), node.path_cost + 1, node)
            sx, sy, shealth = child.state
            if agent.isReturning:
                # print(child.state)
                if agent.visited[sx][sy] and shealth >= 25:
                    # print(sx, sy, agent.kb.check_consistency(agent.kb.propositions[(sx, sy, "P_G")]), health, shealth)
                    children.append(child)
            else:
                children.append(child)
    return children


def trace(node: Node | None) -> list[Node]:
    depth = 0
    path = []
    while node is not None:
        depth += 1
        path.append(node)
        node = node.parent
    return path
