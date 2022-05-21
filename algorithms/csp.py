from collections import deque
from functools import cmp_to_key

class DecisionVariable:
    """
    Decision variable (DV) in the CSP. Every cell in the sudoku grid has a
    decision variable associated with it.
    """

    def __init__(self, row, col, domain):
        """
        Initializes the DV.

        Args:
            row (int): Row in the sudoku grid
            col (int): Column in the sudoku grid
            domain (set): Set of feasible values
        """

        self.row = row
        self.col = col
        self.domain = domain

        # Set of DVs that share a constraint with the given DV. This includes
        # DVs in the same row, column, or 3x3 box as the given DV.
        self.neighbors = set()

    def cmp(dv1, dv2):
        """
        Compares DVs to determine which has higher priority when making a 
        guess in the backtracking algorithm. The comparison is made using the
        minimum-remaining-values (MRV) heuristic and the degree heuristic.

        Args:
            dv1 (DecisionVariable): First DV
            dv2 (DecisionVariable): Second DV

        Returns:
            int: -1 if dv1 is higher priority, 1 if dv2 is higher priority, and 
            0 if dv1 and dv2 are of equal priority
        """

        if len(dv1.domain) < len(dv2.domain): # MRV heuristic
            return -1 # dv1 is higher priority
        elif len(dv1.domain) > len(dv2.domain): # MRV heuristic
            return 1  # dv2 is higher priority
        else: # Degree heuristic
            dv1_unassigned_neighbors_count = \
                sum(1 for dv in dv1.neighbors if len(dv.domain) > 1)
            dv2_unassigned_neighbors_count = \
                sum(1 for dv in dv2.neighbors if len(dv.domain) > 1)

            if dv1_unassigned_neighbors_count > dv2_unassigned_neighbors_count:
                return -1 # dv1 is higher priority
            elif dv1_unassigned_neighbors_count < dv2_unassigned_neighbors_count:
                return 1 # dv2 is higher priority
            else:
                return 0 # dv1 and dv2 are of equal priority

class SudokuCSP:
    """
    Implementation of a backtracking algorithm to solve a 9x9 sudoku when
    modelled as a constraint satisfaction problem (CSP).

    See for reference Chapter 6 of Russell, S. J., Norvig, P., & Davis, E. \
    (2010). Artificial intelligence: a modern approach. 3rd ed. Upper Saddle \
    River, NJ: Prentice Hall.  
    """

    def __init__(self, grid):
        """
        Initializes the CSP.

        Args:
            grid (list): 9x9 sudoku grid with 0s in unfilled cells
        """

        self.guesses = 0 # No. of guesses made by the algorithm
        self.grid = [[None for j in range(9)] for i in range(9)] # 9x9 grid of DVs
        self.unassigned_variables = [] # List of unassigned DVs

        # Add DVs to the grid
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0: # DV is assigned
                    self.grid[i][j] = DecisionVariable(
                        i, j,
                        set([grid[i][j]])
                    )
                else: # DV is unassigned
                    self.grid[i][j] = DecisionVariable(
                        i, j,
                        set([i + 1 for i in range(9)])
                    )

                    self.unassigned_variables.append(self.grid[i][j])
        
        # Assign neighbors to the DVs
        for i in range(9):
            for j in range(9):
                for k in range(9):
                    if k != j: # DVs in the same row as the given DV
                        self.grid[i][j].neighbors.add(self.grid[i][k])
                    if k != i: # DVs in the same column as the given DV
                        self.grid[i][j].neighbors.add(self.grid[k][j])

                # DVs in the same 3x3 block as the given DV
                r = (i // 3) * 3
                c = (j // 3) * 3
                for k in range(3):
                    for l in range(3):
                        if r + k != i or c + l != j:
                            self.grid[i][j].neighbors.add(self.grid[r + k][c + l])

        # Propagate constraints using the AC-3 algorithm
        queue = deque()
        for i in range(9):
            for j in range(9):
                for neighbor in self.grid[i][j].neighbors:
                    queue.append([self.grid[i][j], neighbor])
        self.__ac3(queue)

    def __sort_unassigned_variables(self):
        """
        Sorts unassigned DVs in ascending order of guessing priority.
        """

        self.unassigned_variables.sort(key=cmp_to_key(DecisionVariable.cmp), reverse=True)

    def __ac3(self, queue):
        """
        Implements the arc-consistency algorithm AC-3.

        Args:
            queue (collections.deque): Queue of arcs. Each arc is of the form 
            [xi, xj], where xi and xj are DVs

        Returns:
            list/int: Returns a list of inferences if no inconsistency is found 
            i.e. the CSP can be solved. Each inference is of the form 
            [dv, val], where dv is a decision variable and val is the value 
            removed from dv's domain. Otherwise, returns -1 if an 
            inconsistency is found.
        """

        inferences = []

        while len(queue) > 0:
            xi, xj = queue.popleft() # Dequeue first arc
            xj_value = next(iter(xj.domain))

            # Revise xi's domain if xj is already assigned and xi's domain
            # contains xj's value
            if len(xj.domain) == 1 and xj_value in xi.domain:
                xi.domain.remove(xj_value)
                inferences.append([xi, xj_value])

                if len(xi.domain) == 0: # xi has an empty domain
                    for inference in inferences: # Remove inferences
                        inference[0].domain.add(inference[1])

                    return -1 # Inconsistency is found

                for xk in xi.neighbors:
                    if xk != xj:
                        queue.append([xk, xi])
        
        self.__sort_unassigned_variables()

        return inferences
                

    def __mac(self, dv):
        """
        Implements the maintaining arc consistency (MAC) algorithm.

        Args:
            dv (DecisionVariable): DV whose value has been set

        Returns:
            list/int: Output of the __ac3 method
        """

        queue = deque()

        for neighbor in dv.neighbors:
            if len(neighbor.domain) > 1: # DV is unassigned
                queue.append([neighbor, dv])

        return self.__ac3(queue)

    def __backtrack(self):
        """
        Implements the backtracking algorithm.

        Returns:
            bool: True if the sudoku is solved and False otherwise
        """

        if len(self.unassigned_variables) == 0: # Sudoku is solved
            return True

        # Select DV to be assigned
        dv = self.unassigned_variables.pop()
        old_domain = dv.domain

        for value in old_domain:
            self.guesses += 1

            # Guess DV's value
            dv.domain = set([value])

            inferences = self.__mac(dv)

            if inferences != -1: # No inconsistency found
                result = self.__backtrack()

                if result: # Sudoku is solved
                    return result

                # Remove inferences
                for inference in inferences:
                    inference[0].domain.add(inference[1])
        
        # Reset DV
        dv.domain = old_domain
        self.unassigned_variables.append(dv)

        return False # Sudoku cannot be solved

    def solve(self):
        """
        Solves the sudoku.

        Returns:
            (bool, int, list): A tuple with the first value indicating if the
            sudoku is successfully solved, the second value containing the 
            no. of guesses, and the third value containing the solved grid
        """

        is_solved = self.__backtrack()

        solved_grid = [[0 for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                solved_grid[i][j] = next(iter(self.grid[i][j].domain))

        return (is_solved, self.guesses, solved_grid)