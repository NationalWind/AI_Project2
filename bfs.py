from collections import deque
from knowledgeBase import KnowledgeBase
from sympy import Not, symbols
from agent import Agent


class Node:
    def __init__(self, action, state, path_cost, parent):
        self.action = action
        self.state = state
        self.path_cost = path_cost
        self.parent = parent

    def __lt__(self, other):
        return self.state < other.state


def BFS(agent: Agent):
    node = start_node = Node(None, (agent.x, agent.y), 0, None)
    frontier = deque()
    frontier.append(node)
    reached = [[None] * 10 for _ in range(10)]
    result: None | Node = None
    while frontier:
        node = frontier.popleft()
        for child in expand(node, agent):
            sx, sy = child.state
            if not agent.kb.isKnown(child.state):
                if Not(agent.kb.propositions["W"]) in agent.kb.clauses and Not(agent.kb.propositions["P_S"]) in agent.kb.clauses:
                    return child
                elif agent.healing_potions > 0 and agent.kb.propositions["P_S"] in agent.kb.clauses:
                    if result is None or child.path_cost < result.path_cost:
                        result = child
            if reached[sx][sy] is None:
                reached[sx][sy] = child
                frontier.append(child)
    if result is None:
        for child in expand(start_node, agent, True):
            if not agent.kb.isKnown(child.state):
                return child

    return result


def expand(node, agent: Agent, for_start=False) -> list[Node]:
    children = []
    x, y = node.state
    movs = [(-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")]
    for mov in movs:
        nx, ny = x + mov[0], y + mov[1]
        if 0 <= nx < 10 and 0 <= ny < 10 and (for_start or (Not(agent.kb.propositions["W"]) in agent.kb.clauses or Not(agent.kb.propositions["P_S"]))):
            child = Node(mov[2], (nx, ny), node.path_cost + 1, node)
            children.append(child)
    return children


def trace(node):
    depth = 0
    path = []
    while node is not None:
        depth += 1
        path.append(node.state)
        node = node.parent
    return path[::-1]
