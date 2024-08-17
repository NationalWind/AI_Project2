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
        return self.path_cost < other.path_cost


def BFS(agent: Agent):
    node = start_node = Node(None, (agent.x, agent.y), 0, None)
    frontier = deque()
    frontier.append(node)
    reached = [[None] * 10 for _ in range(10)]
    results = []
    while frontier:
        node = frontier.popleft()
        if not agent.isReturning and not agent.kb.cnt_known == 100 and not ((agent.healing_potions > 0 or agent.health >= 50) and agent.visited[node.state[0]][node.state[1]]):
            continue
        for child in expand(node, agent):

            sx, sy = child.state
            if agent.isReturning or agent.kb.cnt_known == 100:
                if (sx, sy) == (9, 0):
                    return child
            else:
                if not agent.visited[sx][sy] and not agent.kb.isKnown(child.state):

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
            if reached[sx][sy] is None:
                reached[sx][sy] = child
                frontier.append(child)

    if results:
        results.sort()
        print("THIS")
        return results[0][1]
    else:
        # key point? explore more?

        next_node = None
        next_prop = []
        known = None
        for child in expand(start_node, agent, True):
            sx, sy = child.state

            maybe_poison_positive = None
            maybe_poison_negative = None
            maybe_wumpus = None
            maybe_pit = None
            if not isinstance(agent.kb.clauses, bool) and (agent.kb.clauses.has(agent.kb.propositions[(sx, sy, "P")])):
                if agent.visited[sx][sy]:
                    if known is None:
                        if agent.health <= 50:
                            if not agent.kb.clauses.has(agent.kb.propositions[(sx, sy, "P_G")]):
                                known = child
                        else:
                            if all(child.state != state for state in agent.last_positions):
                                known = child
                    else:
                        if not isinstance(agent.kb.clauses, bool) and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P_G")])) == True:
                            known = child
                        if all(child.state != state for state in agent.last_positions):
                            known = child
                continue  # ?
                maybe_pit = child  # last priority
            if not isinstance(agent.kb.clauses, bool) and agent.kb.clauses.has(agent.kb.propositions[(sx, sy, "P_G")]):  # and agent.kb.check_consistency(agent.kb.propositions[(sx, sy, "P_G")] == "Unknown")
                if agent.healing_potions > 0 or agent.health > 50:
                    maybe_poison_positive = child
                else:
                    maybe_poison_negative = child
            if not agent.visited[sx][sy] and not isinstance(agent.kb.clauses, bool) and agent.kb.clauses.has(agent.kb.propositions[(sx, sy, "W")]):
                maybe_wumpus = child  # second to last priority

            if not agent.visited[sx][sy] and maybe_poison_positive and not maybe_wumpus:
                return child
            # if known is None and agent.kb.isKnown(child.state) and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "W")])) is True and agent.kb.check_consistency(Not(agent.kb.propositions[(sx, sy, "P_G")])):
            #     known = child

            if not agent.visited[sx][sy] and not maybe_pit and not maybe_poison_positive and not maybe_poison_negative and not maybe_wumpus and not agent.kb.isKnown(child.state):  # still unsure thou,,..
                return child

            if not agent.visited[sx][sy] and maybe_wumpus:
                next_node = child
            if not agent.visited[sx][sy] and maybe_poison_positive:
                next_node = child
            if not agent.visited[sx][sy] and not maybe_poison_negative and not maybe_pit:  # still unsure thou,,..
                return child

        if next_node is None:
            return known
        else:
            return next_node


def expand(node, agent: Agent, for_start=False) -> list[Node]:
    children = []
    x, y = node.state
    movs = [(-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")]
    for mov in movs:
        nx, ny = x + mov[0], y + mov[1]
        if 0 <= nx < 10 and 0 <= ny < 10:
            child = Node(mov[2], (nx, ny), node.path_cost + 1, node)
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
