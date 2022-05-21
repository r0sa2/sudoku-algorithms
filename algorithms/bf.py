class SudokuBF:
    """
    Implementation of a simple backtracking algorithm to solve a 9x9 sudoku.
    """

    def __init__(self, grid):
        """
        Initializes the sudoku grid.

        Args:
            grid (list): 9x9 sudoku grid with 0s in unfilled cells
        """

        self.guesses = 0 # No. of guesses made by the algorithm
        self.grid = [[0 for j in range(9)] for i in range(9)]
        for i in range(9):
            for j in range(9):
                self.grid[i][j] = grid[i][j]

    def __in_row(self, row, val):
        """
        Checks if val is already present in row.

        Args:
            row (int): Row
            val (int): Value

        Returns:
            bool: True if val is already present in row and False otherwise
        """

        for i in range(9):
            if self.grid[row][i] == val:
                return True

        return False

    def __in_col(self, col, val):
        """
        Checks if val is already present in col.

        Args:
            col (int): Column
            val (int): Value

        Returns:
            bool: True if val is already present in col and False otherwise
        """

        for i in range(9):
            if self.grid[i][col] == val:
                return True
        
        return False

    def __in_box(self, row, col, val):
        """
        Checks if val is already present in the 3x3 box of (row, col).

        Args:
            row (int): Row
            col (int): Column
            val (int): Value

        Returns:
            bool: True if val is already present in the 3x3 box and False otherwise
        """

        r = row - (row % 3)
        c = col - (col % 3)
        for i in range(r, r + 3):
            for j in range(c, c + 3):
                if self.grid[i][j] == val:
                    return True

        return False

    def __is_valid(self, row, col, val):
        """
        Checks if placing val in (row, col) is valid.

        Args:
            row (int): Row
            col (int): Column
            val (int): Value

        Returns:
            bool: True if valid and False otherwise
        """

        return not (self.__in_row(row, val) or self.__in_col(col, val) or self.__in_box(row, col, val))

    def __backtrack(self):
        """
        Implements the backtracking algorithm.

        Returns:
            bool: True if the sudoku is solved and False otherwise
        """

        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    for val in range(1, 10):
                        if self.__is_valid(row, col, val):
                            self.guesses += 1
                            self.grid[row][col] = val

                            if self.__backtrack():
                                return True # Sudoku is solved
                            else:
                                self.grid[row][col] = 0

                    return False # Sudoku cannot be solved
    
        return True # Sudoku is solved

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
                solved_grid[i][j] = self.grid[i][j]

        return (is_solved, self.guesses, solved_grid)