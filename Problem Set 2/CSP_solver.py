from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented


# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {
            value for value in problem.domains[variable] if constraint.condition(value)
        }
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable


# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic,
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min(
        (len(domains[variable]), index, variable)
        for index, variable in enumerate(problem.variables)
        if variable in domains
    )
    return variable


# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
#            since they contain the current domains of unassigned variables only.
def forward_checking(
    problem: Problem,
    assigned_variable: str,
    assigned_value: Any,
    domains: Dict[str, set],
) -> bool:
    # TODO: Write this function
    for constraint in problem.constraints:

        # check if the constraint is a binary constraint
        if isinstance(constraint, BinaryConstraint):

            # if the assigned variable is associated with the current constraint
            if assigned_variable in constraint.variables:

                # get the other variable associated with the same constraint
                other_variable = constraint.get_other(assigned_variable)

                # check if the other variable has no domain -> skip this constraint.
                if other_variable in domains:

                    # take a copy of the set of domains
                    # to remove values while iterating
                    other_domain = domains[other_variable].copy()

                    # loop on the values in the domain and assign it to the other variable
                    for value in other_domain:
                        # create a new assignment with the assigned value and the current value in the domain
                        # assign all the values to the other variable
                        assignment = {
                            assigned_variable: assigned_value, other_variable: value}

                        # check if the new assignmetn satisfies the constraint
                        # if it does then proceed to the next value
                        if constraint.is_satisfied(assignment):
                            continue

                        # if the value assignment violates the constraint then remove it from the domain
                        domains[other_variable].remove(value)

                    # check for an empty domain after removing all the values that violate the constraint
                    # if an empty domain exists then a dead end is reached
                    if (len(domains[other_variable]) == 0):
                        return False
    return True


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic,
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(
    problem: Problem, variable_to_assign: str, domains: Dict[str, set]
) -> List[Any]:
    # TODO: Write this function
    order = []
    value_count = {}

    # take a copy of the domain as the function should not modify ay given arguments
    domains_copy = domains.copy()

    for value in domains_copy[variable_to_assign]:

        count = 0

        for constraint in problem.constraints:

            # check if the constraint is a binary constraint
            if isinstance(constraint, BinaryConstraint):

                if not (variable_to_assign in constraint.variables):
                    continue

                other_variable = constraint.get_other(variable_to_assign)

                if not (other_variable in domains_copy):
                    continue

                for other_value in domains[other_variable]:

                    assignment = {variable_to_assign: value,
                                  other_variable: other_value}

                    # check if the new assignmetn satisfies the constraint
                    # if it does then proceed to the next value
                    if constraint.is_satisfied(assignment):
                        continue

                    count += 1

        value_count[value] = count

    value_count = dict(sorted(value_count.items(), key=lambda x: (x[1], x[0])))

    order = [value for value in value_count.keys()]

    return order


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:

    # TODO: Write this function
    # apply the 1-consistency algorithm on the problem to apply all the unary constraints
    # this will remove values from the domain
    unary_check = one_consistency(problem)

    # if the 1-Consistency algorithm returns false then the problem is not solvable
    if not unary_check:
        return None

    # initialize assignment with an empty dictionary
    assignment = {}

    # call the backtrack function for the problem
    return backtrack(assignment, problem, problem.domains)


# recursive function to backtrack the assigments of varibales to check for dead ends
def backtrack(assignment: Assignment, problem: Problem, domains: Dict[str, set]) -> Any:

    # TODO: Write this function

    # if the current assignment is complete
    # all variables are assigned and constraints are satisfied
    if problem.is_complete(assignment):
        return assignment

    # choose the next variable based on the MRV heuristic
    next_var = minimum_remaining_values(
        problem, domains)  # ghalebn msh el domains dy

    # loop on all values in the order of the LRV heuristic
    for value in least_restraining_values(problem, next_var, domains):

        # take a copy of the new domain after removing the current variable to send to the forward_checking
        new_domain = domains.copy()
        new_domain = {var: val.copy()
                      for var, val in new_domain.items() if var != next_var}

        # if the current assignment can be done (returns True) then the assign the value to the variable
        if forward_checking(problem, next_var, value, new_domain):
            # assign the value to the varibale 
            assignment[next_var] = value 

            # call backtrack for the assignment with the new domain
            result = backtrack(assignment, problem, new_domain)

            # if result is not none then there is a solution -> return it
            if result:
                return result

    # if no solution was found return None
    return None
