from collections import deque
from knowledgeBase import KnowledgeBase
from sympy import Not, symbols
from agent import Agent


class Node:
    def __init__(self, action, state: tuple[int, int, int, int], path_cost, parent):
        self.action = action
        self.state = state
        self.path_cost = path_cost
        self.parent = parent

    def __lt__(self, other):
        return self.path_cost < other.path_cost


def BFS(agent: Agent):
    print(agent.cnt_visited)
    node = start_node = Node(None, (agent.x, agent.y, agent.healing_potions, agent.health), 0, None)
    frontier = deque()
    frontier.append(node)
    reached = [[None] * 10 for _ in range(10)]
    results = []
    while frontier:
        node = frontier.popleft()
        if not agent.isReturning and not ((node.state[2] > 0 or node.state[3] >= 50) and agent.visited[node.state[0]][node.state[1]]):  # 100
            continue
        for child in expand(node, agent):

            sx, sy, _, shealth = child.state
            if agent.isReturning:  # 100
                if (sx, sy) == (9, 0):
                    return child
            else:
                if not agent.visited[sx][sy]:  # and not agent.kb.isKnown((sx, sy))

                    # if Not(agent.kb.propositions["W"]) in agent.kb.clauses and Not(agent.kb.propositions["P_G"]) in agent.kb.clauses:
                    if agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "W")])) is True and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P_G")])) is True and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P")])) is True:
                        return child
                    elif (agent.healing_potions > 0 or agent.health >= 50) and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P")])) is True:
                        results.append(("a", child))
                    elif agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P_G")])) is True and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P")])) is True:
                        results.append(("b", child))
                    elif (agent.healing_potions > 0 or agent.health >= 50) and not isinstance(agent.kb.clauses, bool) and not agent.kb.clauses.has(agent.kb.propositions[(sx, sy, "P")]):  # has considered wumpus
                        results.append(("c", child))
                    elif agent.healing_potions > 0 or agent.health >= 50:  # has considered wumpus
                        results.append(("d", child))
            if reached[sx][sy] is None and shealth >= 50 and (agent.isReturning or child.path_cost <= 5):
                reached[sx][sy] = child
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
    x, y, _, _ = node.state
    movs = [(-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")]
    for mov in movs:
        nx, ny = x + mov[0], y + mov[1]
        if 0 <= nx < 10 and 0 <= ny < 10:
            child = Node(mov[2], (nx, ny, agent.healing_potions, agent.health - (25 if agent.kb.check_consistency(agent.kb.propositions[(nx, ny, "P_G")]) is True else 0)), node.path_cost + 1, node)
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
