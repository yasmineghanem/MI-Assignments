from typing import Tuple, Callable
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

# TODO (Optional): Import any builtin library or define any helper function you want to use
from itertools import combinations, product

# This is a class to define for cryptarithmetic puzzles as CSPs


class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None:
                continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match:
            raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []

        # the variables should be all the unique letters in the equation
        LRHS = LHS0 + LHS1 + RHS
        problem.variables = list(set([var for var in LRHS]))
        print(problem.variables)

        # the domains should be all the numbers from 0-9
        domain = list(i for i in range(10))
        problem.domains = {variable: domain for variable in problem.variables}

        # left most variables should not be equal to zero
        problem.domains[LHS0[0]] = list(i for i in range(1, 10))
        problem.domains[LHS1[0]] = list(i for i in range(1, 10))
        problem.domains[RHS[0]] = list(i for i in range(1, 10))

        # binary constraints
        problem.constraints = [BinaryConstraint((var1, var2), lambda v1, v2: v1 != v2) for var1, var2 in combinations(problem.variables, 2)]

        aligned_terms = [term.rjust(len(RHS)) for term in [LHS0, LHS1, RHS]]
        grouped_characters = list(reversed(list(zip(*aligned_terms))))
        i = 1
        cin = None

        aux_constraint = lambda i : lambda var, aux: var == aux[i]

        for l0, l1, r in grouped_characters:

            carry_variable = "C" + str(i)
            i += 1
            problem.variables.append(carry_variable)
            problem.domains[carry_variable] = [0, 1]

            aux_var = l0 + l1

            aux_var_list = []
            if l0 != " ":
                aux_var_list.append(l0)
            if l1 != " ":
                aux_var_list.append(l1)
            if cin is not None:
                aux_var += cin
                aux_var_list.append(cin)

            aux_var.replace(' ', '')

            # case 1: there is only one variable on the left handside then the r = l
            if len(aux_var) == 1:
                problem.constraints.append(BinaryConstraint((r, aux_var_list[0]), lambda r, l: r == l))
                problem.constraints.append(UnaryConstraint(carry_variable, lambda c: c == 0))

            # case 2: 2 or more varibales in the lhs so add the sum constraint by creating the auxiliary variable
            else:
                problem.variables.append(aux_var)
                problem.domains[aux_var] = list(product(*[problem.domains[var] for var in aux_var_list]))
                problem.constraints.extend(BinaryConstraint((var, aux_var), aux_constraint(i)) for i, var in enumerate(aux_var_list))
                problem.constraints.append(BinaryConstraint((aux_var, r), lambda l, s: sum(l) % 10 == s))
                problem.constraints.append(BinaryConstraint((aux_var, carry_variable), lambda l, c: sum(l) // 10 == c))

            cin = carry_variable

        problem.constraints.append(UnaryConstraint(cin, lambda x: x == 0))

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
