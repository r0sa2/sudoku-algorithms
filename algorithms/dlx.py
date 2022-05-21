class Node:
    """
    Node in the DLX network. Nodes can be of three types :-
    1) Root node - has properties L, R
    2) Header node - has properties L, R, U, D, S
    3) Non-header node - has properties L, R, U, D, C, N
    """
    def __init__(self):
        """
        Initializes the node.
        """

        self.L = None # Reference to left neighbor
        self.R = None # Reference to right neighbor
        self.U = None # Reference to up neighbor
        self.D = None # Reference to down neighbor
        self.C = None # Reference to associated header node
        self.S = 0 # No. of non-header nodes in the column

        # Non-header nodes in the same row are associated with one possibility
        # [row, col, val] i.e. adding val to (row, col) in the sudoku grid
        self.N = None # [row, col, val]

class SudokuDLX:
    """
    Implementation of Donald Knuth's Algorithm X to solve a 9x9 sudoku when
    modelled as an exact cover problem. Algorithm X is implemented using the
    dancing links technique (DLX).

    See for reference https://arxiv.org/pdf/cs/0011047.pdf
    """

    def __init__(self, grid):
        """
        Initializes the DLX network.

        Args:
            grid (list): 9x9 sudoku grid with 0s in unfilled cells
        """

        self.guesses = 0 # No. of guesses made by the algorithm
        self.prefilled_count = 0 # No. of prefilled cells
        self.O = [None for i in range(81)] # Solution

        self.root = Node()

        self.network_height = 730
        self.network_width = 324

        # Nodes in the network other than the root node. First row contains
        # the header nodes and all remaining rows contain non-header nodes
        self.network = [[None for j in range(self.network_width)] for i in range(self.network_height)]

        # Add header nodes
        for i in range(self.network_width):
            self.network[0][i] = Node()

        # Assign L and R properties of the root and header nodes
        self.root.L = self.network[0][self.network_width - 1]
        self.root.R = self.network[0][0]
        self.network[0][0].L = self.root
        self.network[0][0].R = self.network[0][1]
        self.network[0][self.network_width - 1].L = self.network[0][self.network_width - 2]
        self.network[0][self.network_width - 1].R = self.root
        for i in range(1, self.network_width - 1):
            self.network[0][i].L = self.network[0][i - 1]
            self.network[0][i].R = self.network[0][i + 1]

        offset = 81
        for row in range(9):
            for col in range(9):
                # 3x3 block associated with the given (row, col)
                box_index = (row // 3) * 3 + (col // 3)

                for val in range(9):
                    row_index = row * 81 + col * 9 + val + 1
                    col_index0 = row * 9 + col
                    col_index1 = offset + row * 9 + val
                    col_index2 = offset * 2 + col * 9 + val
                    col_index3 = offset * 3 + box_index * 9 + val              
                    
                    # Add non-header nodes
                    self.network[row_index][col_index0] = Node() # Row-Column constraint
                    self.network[row_index][col_index1] = Node() # Row-Number constraint
                    self.network[row_index][col_index2] = Node() # Column-Number constraint
                    self.network[row_index][col_index3] = Node() # Box-Number constraint

                    # Assign L, R, and C properties of the non-header nodes 
                    self.network[row_index][col_index0].L = self.network[row_index][col_index3]
                    self.network[row_index][col_index0].R = self.network[row_index][col_index1]
                    self.network[row_index][col_index1].L = self.network[row_index][col_index0]
                    self.network[row_index][col_index1].R = self.network[row_index][col_index2]
                    self.network[row_index][col_index2].L = self.network[row_index][col_index1]
                    self.network[row_index][col_index2].R = self.network[row_index][col_index3]
                    self.network[row_index][col_index3].L = self.network[row_index][col_index2]
                    self.network[row_index][col_index3].R = self.network[row_index][col_index0]
                    self.network[row_index][col_index0].C = self.network[0][col_index0]
                    self.network[row_index][col_index1].C = self.network[0][col_index1]
                    self.network[row_index][col_index2].C = self.network[0][col_index2]
                    self.network[row_index][col_index3].C = self.network[0][col_index3]

                    # Increment S property of the associated header nodes
                    self.network[row_index][col_index0].C.S += 1
                    self.network[row_index][col_index1].C.S += 1
                    self.network[row_index][col_index2].C.S += 1
                    self.network[row_index][col_index3].C.S += 1                

                    self.network[row_index][col_index0].N = [row, col, val + 1]
                    self.network[row_index][col_index1].N = [row, col, val + 1]
                    self.network[row_index][col_index2].N = [row, col, val + 1]
                    self.network[row_index][col_index3].N = [row, col, val + 1]

                    if grid[row][col] == val + 1: # Cell is prefilled
                        self.O[self.prefilled_count] = self.network[row_index][col_index0]
                        self.prefilled_count += 1

        # Assign U and D properties of the header and non-header nodes
        for col in range(self.network_width):
            header = self.network[0][col]
            node = header

            for row in range(1, self.network_height):
                if self.network[row][col] != None:
                    node.D = self.network[row][col]
                    self.network[row][col].U = node
                    node = self.network[row][col]

            header.U = node
            node.D = header

        # Remove rows associated with prefilled cells
        for i in range(self.prefilled_count):
            self.__remove_row(self.O[i])

    def __remove_row(self, node):
        """
        Removes rows associated with prefilled cells.

        Args:
            node (Node): Non-header node in the row
        """
    
        # Determine header nodes associated with the row
        col_heads = []
        col_heads.append(node.C)
        
        row_node = node.R
        while row_node != node:
            col_heads.append(row_node.C)
            row_node = row_node.R
        
        # Cover the column of each header node
        for i in range(len(col_heads)):
            self.__cover_col(col_heads[i])

    def __select_col_head(self):
        """
        Returns the header node of the next column to be covered or None if
        there are no remaining header nodes

        Returns:
            Node: Header node of column to be covered
        """

        if self.root.R == self.root: # No remaining header nodes
            return None

        # Select the header node with minimum S value
        col_head = self.root
        min_col_head = col_head
        min_rows = self.network_height
        while col_head.R != self.root:
            col_head = col_head.R

            if col_head.S < min_rows:
                min_col_head = col_head
                min_rows = col_head.S

        return min_col_head

    def __cover_col(self, col_head):
        """
        Covers the column.

        Args:
            col_head (Node): Header node of column to be covered
        """

        col_head.R.L = col_head.L
        col_head.L.R = col_head.R

        col_node = col_head.D
        while col_node != col_head:
            row_node = col_node.R
            while row_node != col_node:
                row_node.D.U = row_node.U
                row_node.U.D = row_node.D
                row_node.C.S -= 1

                row_node = row_node.R

            col_node = col_node.D

    def __uncover_col(self, col_head):
        """
        Uncovers the column.

        Args:
            col_head (Node): Header node of column to be uncovered
        """

        col_node = col_head.U
        while col_node != col_head:
            row_node = col_node.L
            while row_node != col_node:
                row_node.C.S += 1
                row_node.D.U = row_node
                row_node.U.D = row_node

                row_node = row_node.L

            col_node = col_node.U

        col_head.R.L = col_head
        col_head.L.R = col_head

    def __search(self, k):
        """
        Implements the DLX algorithm.

        Args:
            k (int): index of solution array O to be filled next

        Returns:
            bool: True if the sudoku is solved and False otherwise
        """

        # Select the header node of the column to be covered
        col_head = self.__select_col_head()

        if col_head == None: # Sudoku is solved
            return True

        # Cover the column
        self.__cover_col(col_head)

        # Select the first row in the column
        col_node = col_head.D

        while col_node != col_head:
            # Add the row to the solution
            self.O[k] = col_node
            self.guesses += 1

            # Cover columns associated with the row
            row_node = col_node.R
            while row_node != col_node:
                self.__cover_col(row_node.C)

                row_node = row_node.R

            if self.__search(k + 1): # Sudoku is solved
                return True

            # Uncover columns associated with the row
            row_node = col_node.L
            while row_node != col_node:
                self.__uncover_col(row_node.C)

                row_node = row_node.L

            # Move to the next row
            col_node = col_node.D

        # Uncover the column
        self.__uncover_col(col_head)
        
        return False # Sudoku cannot be solved

    def solve(self):
        """
        Solves the sudoku.

        Returns:
            (bool, int, list): A tuple with the first value indicating if the
            sudoku is successfully solved, the second value containing the 
            no. of guesses, and the third value containing the solved grid
        """

        is_solved = self.__search(k=self.prefilled_count)

        solved_grid = [[0 for j in range(9)] for i in range(9)]
        for i in range(81):
            solved_grid[self.O[i].N[0]][self.O[i].N[1]] = self.O[i].N[2]

        return (is_solved, self.guesses, solved_grid)