import pycosat
from pprint import pprint

# number of cells in sudoku
NUM_CELLS = 81

# this can be used to interate all squares subset in 3x 3
#    V      V      V
#    1 2 3  4 5 6  7 8 9
#> 1 |0 0 0| 0 0 0| 0 0 0|
#  2 |0 0 0| 0 0 0| 0 0 0|
#  3 |0 0 0| 0 0 0| 0 0 0|
#    ---------------------
#> 4 |0 0 0| 0 0 0| 0 0 0|
#  5 |0 0 0| 0 0 0| 0 0 0|
#  6 |0 0 0| 0 0 0| 0 0 0|
#    --------------------
#> 7 |0 0 0| 0 0 0| 0 0 0|
#  8 |0 0 0| 0 0 0| 0 0 0|
#  9 |0 0 0| 0 0 0| 0 0 0|
SUBSQUARE_BOUDARIES = [1, 4, 7]

# most digit in sudoku
NUM_DIGITS = 9

def get_cell_value(row, column, digit):
   """
     make unique id to a cell

     first number is a row
     second is a column
     third is a digit value

     Ex: the cell (1,3) and (3,1) with digit 7 there are diferentes id
         cell (1,3) = 137
         cell (3,1) = 317
   """
   return row*100+column*10+ digit

def get_base_clauses():
    """
    make all NUM_VARIABLES used in sudoku board, named by id

    Ex:
        for cell (1,1) and digit 7 can be named: 117
        for cell (2,3) and digit 5 can be named: 235
    """
    base_clauses = []

    for row in range(1, NUM_DIGITS+1):
       for column in range(1, NUM_DIGITS+1):
          clauses = []
          for digit in range(1, NUM_DIGITS+1):
             clauses.append(get_cell_value(row,column,digit))
          base_clauses.append(clauses)

    return base_clauses

def get_unique_cells_clauses():
    """
    make clauses guarantee that a cell can just appear once for sudoku board.

    to make this each cell will have the next cell with the clause:
      ~current_digit or ~next_digit

    Example:
        to cell 111 there the clauses:
        (-111,-112),(-111,-113),(-111,-114),...,(-111,-999)
    """
    unique_digits_clauses = []

    for row in range(1, NUM_DIGITS+1):
        for column in range(1,NUM_DIGITS+1):
            for digit in range(1, NUM_DIGITS+1):
                for next_digit in range(digit+1, NUM_DIGITS+1):
                    cell_id = -get_cell_value(row,column,digit)
                    next_cell_id = -get_cell_value(row,column,next_digit)
                    unique_digits_clauses.append([cell_id,next_cell_id])

    return unique_digits_clauses

def get_unique_subset_clauses(board_subset):
    """
    this guarantee that a cell appear only once in the board subset
    """
    subset_clauses = []
    subset = enumerate(board_subset)

    for index, first_tuple in enumerate(board_subset):
        for n_index, n_tuple in enumerate(board_subset):
            if index < n_index:
                for digit in range(1, NUM_DIGITS + 1):
                    clause = [-get_cell_value(
                        first_tuple[0], first_tuple[1], digit),
                        -get_cell_value(
                        n_tuple[0], n_tuple[1], digit)]
                    subset_clauses.append(clause)
    return subset_clauses

def get_row_unique_clauses():
    """
    this guarantee that a cell in row appear only once in the row
    """
    unique_clauses = []

    for row in range(1,NUM_DIGITS +1):
        subset = []
        for column in range(1, NUM_DIGITS+1):
            subset.append((row,column))
        unique_clauses.extend(get_unique_subset_clauses(subset))
    return unique_clauses

def get_columns_unique_clauses():
    """
    this guarantee that a cell in column appear only once in the columns
    """
    unique_clauses = []
    for row in range(1,NUM_DIGITS +1):
        subset = []
        for column in range(1, NUM_DIGITS+1):
            subset.append((column,row))
        unique_clauses.extend(get_unique_subset_clauses(subset))
    return unique_clauses

def get_square_unique_clauses():
    """
    this guarantee that a cell in square appear only once in the squares
    """
    subset_clauses = []

    for row in SUBSQUARE_BOUDARIES:
        for column in SUBSQUARE_BOUDARIES:
            subset = [] # make subset 3x3
            for k in range(9):
                subset.append((row+k%3,column+k//3))
            subset_clauses.extend(get_unique_subset_clauses(subset))

    return subset_clauses

def get_sudoku_clauses():
    """
    mix all defined clauses to guarantee a valid sudoku
    """
    sudoku_clauses = []
    sudoku_clauses.extend(get_base_clauses())
    sudoku_clauses.extend(get_unique_cells_clauses())
    sudoku_clauses.extend(get_row_unique_clauses())
    sudoku_clauses.extend(get_columns_unique_clauses())
    sudoku_clauses.extend(get_square_unique_clauses())

    return sudoku_clauses

def get_single_clauses(sudoku_board):
    """
    This method make a clauses that can be answer true
    to solve the sudoku board
    """
    single_clauses = []
    for row in range(1, NUM_DIGITS+1):
        for column in range(1,NUM_DIGITS+1):
            cell_value = sudoku_board[row-1][column-1]
            if cell_value:
                single_clauses.append(
                    [get_cell_value(row,column,cell_value)])

    return single_clauses

def get_cell_solution(sudoku_solution, row, column):
    """
    verify a cell id in a sudoku solution list
    """
    for digit in range(1, NUM_DIGITS+1):
        if get_cell_value(row,column,digit) in sudoku_solution:
            return digit
    return -1

def solve_sudoku(sudoku_board):
    """
    Generate a sudoku clauses, apply in a pycosat and get sudoku solution
    """
    sudoku_clauses = get_sudoku_clauses()
    single_clauses = get_single_clauses(sudoku_board)
    sudoku_clauses.extend(single_clauses)

    sudoku_solution = set(pycosat.solve(sudoku_clauses))

    for row in range(1, NUM_DIGITS+1):
        for column in range(1, NUM_DIGITS+1):
            sudoku_board[row-1][column-1] = get_cell_solution(
                sudoku_solution, row, column)
    return sudoku_board

def main():
    print ("Sudoku problem:")
    sudoku_problem = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 6, 0, 0, 0, 0, 3],
                      [0, 7, 4, 0, 8, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 3, 0, 0, 2],
                      [0, 8, 0, 0, 4, 0, 0, 1, 0],
                      [6, 0, 0, 5, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 7, 8, 0],
                      [5, 0, 0, 0, 0, 9, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 4, 0]]
    pprint(sudoku_problem)

    print('\nGenerating solution:')
    sudoku_solution = solve_sudoku(sudoku_problem)
    pprint(sudoku_solution)


if __name__ == '__main__':
    main()
