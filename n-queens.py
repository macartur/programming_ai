import pycosat
from pprint import pprint

def cell_id(row, column):
    return row*10+column

def get_unique_row_column_clauses(row, column, N):
    clauses = []

    for next_element in range(column+1,N+1):
        clauses.append([-cell_id(row,column), -cell_id(row,next_element)])
        clauses.append([-cell_id(column,row), -cell_id(next_element,row)])

    return clauses

def get_unique_right_diagonal(row,column, N):
    unique_in_diagonal = []
    right_diagonal = [row+1,column+1]

    while(right_diagonal[0] < N+1 and right_diagonal[1] < N+1):
        unique_in_diagonal.append([-cell_id(row,column), -cell_id(right_diagonal[0],right_diagonal[1])])
        right_diagonal = [right_diagonal[0]+1,right_diagonal[1]+1]

    return unique_in_diagonal

def get_unique_left_diagonal(row,column, N):
    unique_in_diagonal = []
    left_diagonal = [row+1, column-1]

    while(left_diagonal[0] < N+1 and left_diagonal[1] > 0):
        unique_in_diagonal.append([-cell_id(row,column), -cell_id(left_diagonal[0],left_diagonal[1])])
        left_diagonal = [left_diagonal[0]+1, left_diagonal[1]-1]

    return unique_in_diagonal

def get_clauses(N):
    clauses = []
    unique_row_column_clauses=[]

    for row in range(1,N+1):

        line_clauses = []
        column_clauses = []

        for column in range(1, N+1):
            line_clauses.append(cell_id(row,column))
            column_clauses.append(cell_id(column,row))

            unique_row_column_clauses.extend(get_unique_row_column_clauses(row, column, N))
            clauses.extend(get_unique_right_diagonal(row, column, N))
            clauses.extend(get_unique_left_diagonal(row, column, N))

        unique_row_column_clauses.append(line_clauses)
        unique_row_column_clauses.append(column_clauses)

    clauses.extend(unique_row_column_clauses)

    return clauses


def get_nqueen_clauses(NUM_ROWS, NUM_COLUMNS):
    """
    This method return all clauses used to define a queen position valid.
    """
    nqueen_clauses = []
    nqueen_clauses.extend(get_clauses(NUM_ROWS))

    return nqueen_clauses

def get_cell_solution(nqueen_solution, row, column):
    """
    This method returns 1 if found in the solution
    otherwise '0'.
    """
    if cell_id(row,column) in nqueen_solution:
        return '1'
    return '0'

def solve_nqueen(board, NUM_ROWS, NUM_COLUMNS):

    nqueen_clauses = get_nqueen_clauses(NUM_ROWS, NUM_COLUMNS)
    solution = set(pycosat.solve(nqueen_clauses))

    for row in range(1,NUM_ROWS+1):
        for column in range(1,NUM_COLUMNS+1):
            board[row-1][column-1] = get_cell_solution(solution,row, column)

def create_board(NUM_ROWS, NUM_COLUMNS):
    board = []
    for row in range(1,NUM_ROWS+1):
        board.append([ '0' for column in range(1,NUM_COLUMNS+1) ])
    return board

def write_board(board_solution,NUM_ROWS, NUM_COLUMNS):
    file_solution = open('nqueen_solution.txt','w')
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
