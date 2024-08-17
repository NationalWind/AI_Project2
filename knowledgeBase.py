from define import *
from sympy import symbols, Or, And, Not, Implies, Symbol
from sympy.logic.boolalg import to_cnf, simplify_logic


# Define propositions
def define_propositions():
    propositions = {}
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            propositions[(x, y, "W")] = symbols(f"W_{x}_{y}")
            propositions[(x, y, "P")] = symbols(f"P_{x}_{y}")
            propositions[(x, y, "G")] = symbols(f"G_{x}_{y}")
            propositions[(x, y, "P_G")] = symbols(f"P_G_{x}_{y}")
            propositions[(x, y, "H_P")] = symbols(f"H_P_{x}_{y}")
            propositions[(x, y, "B")] = symbols(f"B_{x}_{y}")
            propositions[(x, y, "S")] = symbols(f"S_{x}_{y}")
            propositions[(x, y, "W_H")] = symbols(f"W_H_{x}_{y}")
            propositions[(x, y, "G_L")] = symbols(f"G_L_{x}_{y}")

    return propositions


class KnowledgeBase:
    def __init__(self, size):
        self.size = size
        self.propositions = define_propositions()
        self.clauses = True
        self.known = [[False] * 10 for _ in range(10)]
        self.cnt_known = 0

    def add_clause(self, *literals):
        # Adds a CNF clause to the knowledge base
        self.clauses = And(self.clauses, (Or(*literals)))

    def add_clause_list(self, literals):
        # Adds a CNF clause to the knowledge base
        self.clauses = And(self.clauses, (Or(*literals)))

    def add_proposition(self, x, y, prop, value):
        proposition = self.propositions[(x, y, prop)]
        if value:
            self.add_clause(proposition)
        else:
            self.add_clause(Not(proposition))

    def add_implication(self, antecedent, consequent):
        # Add an implication to the knowledge base
        implication = Implies(antecedent, consequent)
        self.add_clause(to_cnf(implication, True))

    def check_consistency(self, proposition):
        # Check if adding the proposition leads to inconsistency
        proposition = to_cnf(proposition, True)
        test = simplify_logic(And(self.clauses, Not(proposition)))
        if test == False:
            self.add_clause(proposition)
            return True  # Contradiction
        else:
            return "Unknown"  # Ambiguous

    def infer(self):
        # Placeholder for inference logic
        # Here, you might want to implement a more sophisticated inference mechanism
        pass

    def isKnown(self, pos: tuple[int, int]):
        if self.known[pos[0]][pos[1]]:
            return True

        entities = ["W", "P", "G", "P_G", "H_P", "B", "S", "W_H", "G_L"]
        for entity in entities:
            check_pos = self.check_consistency(self.propositions[(*pos, entity)])
            check_neg = self.check_consistency(Not(self.propositions[(*pos, entity)]))
            if check_pos == "Unknown" and check_neg == "Unknown":
                return False
        self.cnt_known += 1
        return True

    def display_knowledge(self):
        # Display the CNF of the knowledge base
        print(self.clauses)


kb = KnowledgeBase(GRID_SIZE)

# Define propositions
W_1_1 = kb.propositions[(1, 1, "W")]
P_1_1 = kb.propositions[(1, 1, "P")]
P_G_1_1 = kb.propositions[(1, 1, "P_G")]
P_G_2_2 = kb.propositions[(2, 2, "P_G")]


kb.add_clause(W_1_1, P_G_1_1)  # Adding that there's a Wumpus at (1, 1)
# kb.add_knowledge(1, 1, 'P', False)  # Adding that there's no Pit at (1, 1)
# combined_proposition = combine_propositions(P_G_2_2, P_1_1, P_G_1_1)
# kb.add_clause(combined_proposition)
# Add an implication: If there's a Wumpus, then there should not be a Pit
# kb.add_implication(W_1_1, Not(P_1_1))

# Check consistency of adding a new proposition
# new_proposition = Not(P_1_1)
# consistency_result = kb.check_consistency(new_proposition)
# if consistency_result == True:
#     print("Consistency check for proposition 'P_1_1': True")
# else:
#     kb.add_proposition(1, 1, 'P', True)  # Add to KB if consistent
#     print("Consistency check for proposition 'P_1_1': Unknown")

# Display knowledge base
kb.display_knowledge()
