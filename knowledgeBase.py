from define import *
from sympy import symbols, Or, And, Not, Implies, Symbol, satisfiable, Equivalent
from sympy.logic.boolalg import to_cnf, simplify_logic
from sympy.assumptions.cnf import EncodedCNF


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
        self.clauses = []
        self.known = [[False] * 10 for _ in range(10)]
        self.cnt_known = 0

    def add_clause(self, *literals):
        # Adds a CNF clause to the knowledge base
        oredLiterals = Or(*literals)
        if Not(oredLiterals) in self.clauses:
            self.clauses.remove(Not(oredLiterals))
        if oredLiterals not in self.clauses:
            self.clauses.append(oredLiterals)

    def remove_clause(self, *literals):
        # Adds a CNF clause to the knowledge base
        oredLiterals = Or(*literals)
        if oredLiterals in self.clauses:
            self.clauses.remove(oredLiterals)

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
        # proposition = to_cnf(proposition, True)
        test = satisfiable(And(*self.clauses, Not(proposition)), algorithm="dpll")
        if test is False:
            self.add_clause(proposition)
            return True  # Contradiction
        else:
            return "Unknown"  # Ambiguous

    def infer(self):
        # Placeholder for inference logic
        # Here, you might want to implement a more sophisticated inference mechanism
        pass

    # def isKnown(self, pos: tuple[int, int]):
    #     if self.known[pos[0]][pos[1]]:
    #         return True

    #     entities = ["W", "P", "G", "P_G", "H_P", "B", "S", "W_H", "G_L"]
    #     for entity in entities:
    #         check_pos = self.check_consistency(self.propositions[(*pos, entity)])
    #         check_neg = self.check_consistency(Not(self.propositions[(*pos, entity)]))
    #         if check_pos == "Unknown" and check_neg == "Unknown":
    #             return False

    #     self.known[pos[0]][pos[1]] = True
    #     self.cnt_known += 1
    #     return True

    def display_knowledge(self):
        # Display the CNF of the knowledge base
        print(self.clauses)


kb = KnowledgeBase(GRID_SIZE)

# Define propositions
W_3_2 = kb.propositions[(3, 2, "W")]
W_4_1 = kb.propositions[(4, 1, "W")]
W_4_3 = kb.propositions[(4, 3, "W")]
W_5_2 = kb.propositions[(5, 2, "W")]

a, b, c, d, e = symbols("a b c d e")
print(Equivalent(a, b | c | d | e) & a & Not(b | c | d | e))

# print(
#     satisfiable(
#         "B_6_1 & B_7_0 & G_7_1 & G_L_4_2 & G_L_6_1 & G_L_7_0 & G_L_8_1 & H_P_7_1 & P_G_3_2 & P_G_4_1 & P_G_4_2 & P_G_4_3 & P_G_5_1 & P_G_5_2 & P_G_5_3 & P_G_6_1 & P_G_6_2 & P_G_6_3 & P_G_7_1 & P_G_7_2 & P_G_7_3 & P_G_8_2 & S_4_2 & S_7_2 & S_8_1 & W_3_2 & ~B_4_2 & ~B_5_2 & ~B_6_2 & ~B_7_1 & ~B_7_2 & ~B_8_0 & ~B_8_1 & ~B_9_0 & ~G_4_2 & ~G_5_2 & ~G_6_1 & ~G_6_2 & ~G_7_0 & ~G_7_1 & ~G_7_2 & ~G_8_0 & ~G_8_1 & ~G_9_0 & ~G_L_5_2 & ~G_L_6_2 & ~G_L_7_1 & ~G_L_7_2 & ~G_L_8_0 & ~G_L_9_0 & ~H_P_4_2 & ~H_P_5_1 & ~H_P_5_2 & ~H_P_5_3 & ~H_P_6_1 & ~H_P_6_2 & ~H_P_6_3 & ~H_P_7_0 & ~H_P_7_1 & ~H_P_7_2 & ~H_P_7_3 & ~H_P_8_0 & ~H_P_8_1 & ~H_P_8_2 & ~H_P_9_0 & ~H_P_9_1 & ~P_3_2 & ~P_4_1 & ~P_4_2 & ~P_4_3 & ~P_5_1 & ~P_5_2 & ~P_5_3 & ~P_6_1 & ~P_6_2 & ~P_6_3 & ~P_7_0 & ~P_7_1 & ~P_7_2 & ~P_7_3 & ~P_8_0 & ~P_8_1 & ~P_8_2 & ~P_9_0 & ~P_9_1 & ~P_G_3_2 & ~P_G_4_1 & ~P_G_4_2 & ~P_G_4_3 & ~P_G_5_1 & ~P_G_5_2 & ~P_G_5_3 & ~P_G_6_0 & ~P_G_6_1 & ~P_G_6_2 & ~P_G_6_3 & ~P_G_7_0 & ~P_G_7_1 & ~P_G_7_2 & ~P_G_7_3 & ~P_G_8_0 & ~P_G_8_1 & ~P_G_8_2 & ~P_G_9_0 & ~P_G_9_1 & ~S_5_2 & ~S_6_1 & ~S_6_2 & ~S_7_0 & ~S_7_1 & ~S_8_0 & ~S_9_0 & ~W_4_2 & ~W_5_1 & ~W_5_2 & ~W_5_3 & ~W_6_0 & ~W_6_1 & ~W_6_2 & ~W_6_3 & ~W_7_0 & ~W_7_1 & ~W_7_2 & ~W_8_0 & ~W_8_1 & ~W_9_0 & ~W_9_1 & ~W_H_4_2 & ~W_H_5_2 & ~W_H_6_1 & ~W_H_6_2 & ~W_H_7_0 & ~W_H_7_1 & ~W_H_7_2 & ~W_H_8_0 & ~W_H_8_1 & ~W_H_9_0 & (H_P_6_0 | H_P_7_1 | H_P_8_0) & (P_6_0 | P_7_1 | P_8_0) & (H_P_3_2 | H_P_4_1 | H_P_4_3 | H_P_5_2) & (H_P_5_1 | H_P_6_0 | H_P_6_2 | H_P_7_1) & (H_P_7_1 | H_P_8_0 | H_P_8_2 | H_P_9_1) & (P_5_1 | P_6_0 | P_6_2 | P_7_1) & (W_3_2 | W_4_1 | W_4_3 | W_5_2) & (W_6_2 | W_7_1 | W_7_3 | W_8_2) & (W_7_1 | W_8_0 | W_8_2 | W_9_1)"
#     )
# )
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
# kb.display_knowledge()
