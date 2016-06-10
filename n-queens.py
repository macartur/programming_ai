import pycosat
from pprint import pprint

def get_cell_value(row, column):
    """
    This method return unique id for a cell.
    """
    return row*10+column

def get_base_clauses(NUM_ROWS, NUM_COLUMNS):
    """
    This method make all cell value to sat.
    """
    base_clauses = []

    for row in range(1,NUM_ROWS+1):
        for column in range(1, NUM_COLUMNS+1):
            base_clauses.append(get_cell_value(row,column))
    return base_clauses

def get_unique_row_clauses(NUM_ROWS, NUM_COLUMNS):
    """
    This method ensures that has a queen only once by row

    Clauses:
        For N = 4:
        x11 V x12 V x13 V x14 =  1
            ~X11 V ~X12
            ~X11 V ~X13
            ~X11 V ~X14
            ~X12 V ~X13
            ~X12 V ~X14
            ~X13 V ~X14
    """
    clauses = []

    for row in range(1, NUM_ROWS+1):
        first_clause = []
        for column in range(1, NUM_COLUMNS+1):
            first_clause.append(get_cell_value(row,column))
            unique_in_row = []
            for next_column in range(column+1,NUM_COLUMNS+1):
                clause = [-get_cell_value(row,column),
                          -get_cell_value(row,next_column)]
                unique_in_row.append(clause)
            clauses.extend(unique_in_row)
        clauses.append(first_clause)
    return clauses

def get_unique_column_clauses(NUM_ROWS, NUM_COLUMNS):
    """
    This method ensures that has a queen only once by column

    Clauses:
        For N = 4:
        x11 V x12 V x13 V x14 =  1
            ~X11 V ~X21
            ~X11 V ~X31
            ~X11 V ~X41
            ~X21 V ~X31
            ~X21 V ~X41
            ~X31 V ~X41
    """
    clauses = []

    for row in range(1, NUM_ROWS+1):
        first_clause = []
        for column in range(1, NUM_COLUMNS+1):
            first_clause.append(get_cell_value(column,row))
            unique_in_row = []
            for next_column in range(column+1,NUM_COLUMNS+1):
                clause = [-get_cell_value(column,row),
                          -get_cell_value(next_column,row)]
                unique_in_row.append(clause)
            clauses.extend(unique_in_row)
        clauses.append(first_clause)
    return clauses

def get_unique_right_diagonal(NUM_ROWS, NUM_COLUMNS):
    """
      This method guarantee that has a queen only once by right diagonal.

      Example:
        - right diagonal
        [ ['1', '0', '0', '0'],
          ['0', '1', '0', '0'],
          ['0', '0', '1', '0']
          ['0', '0', '0', '1']]

      Clauses:
         For N = 4 and (1,1):
            ~X11 V ~X22
            ~X11 V ~X33
            ~X11 V ~X44
    """

    clauses = []
    for row in range(1, NUM_ROWS+1):
        for column in range(1, NUM_COLUMNS+1):
            unique_in_diagonal = []
            row_diagonal = row+1
            column_diagonal = column+1
            while(row_diagonal < NUM_ROWS+1 and
                  column_diagonal < NUM_COLUMNS+1):
                clause = [-get_cell_value(row,column),
                          -get_cell_value(row_diagonal,column_diagonal)]
                unique_in_diagonal.append(clause)
                row_diagonal+=1
                column_diagonal+=1
            clauses.extend(unique_in_diagonal)
    return clauses

def get_unique_left_diagonal(NUM_ROWS, NUM_COLUMNS):
    """
    This method ensure that has a queen only once by left diagonal.

    Example:
        - left diagonal
        [ ['0', '0', '0', '1'],
          ['0', '0', '1', '0'],
          ['0', '1', '0', '0']
          ['1', '0', '0', '0']]
      Clauses:
         For N = 4 and (1,4):
            ~X14 V ~X23
            ~X14 V ~X32
            ~X14 V ~X41
    """
    clauses = []
    for row in range(1, NUM_ROWS+1):
        for column in range(1, NUM_COLUMNS+1):
            unique_in_diagonal = []
            row_diagonal = row+1
            column_diagonal = column-1
            while(row_diagonal < NUM_ROWS+1 and
                  column_diagonal > 0):
                clause = [-get_cell_value(row,column),
                          -get_cell_value(row_diagonal,column_diagonal)]
                unique_in_diagonal.append(clause)
                row_diagonal+=1
                column_diagonal-=1
            clauses.extend(unique_in_diagonal)
    return clauses

def get_nqueen_clauses(NUM_ROWS, NUM_COLUMNS):
    """
    This method return all clauses used to define a queen position valid.
    """
    nqueen_clauses = []
    nqueen_clauses.extend(get_unique_row_clauses(NUM_ROWS, NUM_COLUMNS))
    nqueen_clauses.extend(get_unique_column_clauses(NUM_ROWS, NUM_COLUMNS))
    nqueen_clauses.extend(get_unique_right_diagonal(NUM_ROWS, NUM_COLUMNS))
    nqueen_clauses.extend(get_unique_left_diagonal(NUM_ROWS, NUM_COLUMNS))

    return nqueen_clauses

def get_cell_solution(nqueen_solution, row, column):
    """
    This method returns 1 if found in the solution
    otherwise '0'.
    """
    if get_cell_value(row,column) in nqueen_solution:
        return '1'
    return '0'

def solve_nqueen(board, NUM_ROWS, NUM_COLUMNS):

    nqueen_clauses = get_nqueen_clauses(NUM_ROWS, NUM_COLUMNS)
    solution = set(pycosat.solve(nqueen_clauses))

    for row in range(1,NUM_ROWS+1):
        for column in range(1,NUM_COLUMNS+1):
            board[row-1][column-1] = get_cell_solution(solution,
                                                       row, column)
    return board

def create_board(NUM_ROWS, NUM_COLUMNS):
    board = []
    for row in range(1,NUM_ROWS+1):
        board.append([ '0' for column in range(1,NUM_COLUMNS+1) ])
    return board

def write_board(board_solution,NUM_ROWS, NUM_COLUMNS):
    file_solution = open('nquee_solution.txt','w+')
    for row in range(1,NUM_ROWS+1):
        for column in range(1,NUM_COLUMNS+1):
            file_solution.write("{} ".format(board_solution[row-1][column-1]))
        file_solution.write('\n')

def main():
    N = int(raw_input("Enter a number of row by columns (N):"))

    NUM_ROWS = N
    NUM_COLUMNS = N

    board = create_board(NUM_ROWS, NUM_COLUMNS)
    solve_nqueen(board, NUM_ROWS, NUM_COLUMNS)
    write_board(board, NUM_ROWS, NUM_COLUMNS)


if __name__ == '__main__':
    main()
