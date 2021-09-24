# arrange n-queens on an nxn chess board, avoiding conflicts, using a random-restart hill climbing algorithm
# Author: Marcus Skinner

import sys
import random

# Return a string with the board rendered in a readable format
def printable_board(board):
    return "\n".join(["".join(row) for row in board])

# Add a queen to the board at the given position, and return a new board.
def add_queen(board, row, col):
    return board[0:row] + [board[row][0:col] + ['Q',] + board[row][col+1:]] + board[row+1:]

# Remove a queen from the board at a given position, and return the new board.
def remove_queen(board, row, col):
    return board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + board[row+1:]

# Returns a list of all the positions of all the queens
def findall_queens(board):
    return [(r,c) for r in range(len(board)) for c in range(len(board[0])) if board[r][c] == 'Q']

# Calculates how many queens threaten each space on the board
def calculate_threatened(board, queens_loc):
    threatened = [[0 for c in range(len(board[0]))] for r in range(len(board))]
    
    for q in queens_loc:
        sight = check_sight(board, q[0], q[1])
        for space in sight:
            threatened[space[0]][space[1]] += 1
            
    return threatened

# set random starting positions for all the queens
def setup_board(board, k):
    num_rows = len(board)
    num_cols = len(board[0])
    
    # Get a list of all free spaces
    free = [(r,c) for r in range(len(board)) for c in range(len(board[0])) if board[r][c] == "."]
    
    # place all queens in random free space
    for i in range(k):
        loc = random.choice(free)
        board = add_queen(board, loc[0], loc[1])
        free.remove(loc)
        
    return board

# Calculates the free spaces, with the number of queens that threaten them, and the locations of each queen,
# with the number of queens that threaten them
def calculate_state(board):
    free_spaces = {}
    queens = {}
    
    queens_loc = findall_queens(board)
    threatened = calculate_threatened(board, queens_loc)
    
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == '.':
                free_spaces[(r,c)] = threatened[r][c]
            if board[r][c] == 'Q':
                queens[(r,c)] = threatened[r][c]
    return free_spaces, queens

# check all spaces the agent has sight in direction
# direction can be (0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1)
def line_of_sight(board, row, col, direction):
    sight = []
    row += direction[0]
    col += direction[1]
    
    while row < len(board) and col < len(board[0]) and row > -1 and col > -1 and board[row][col] in ['.', 'Q']:
        sight += [(row, col)]
        row += direction[0]
        col += direction[1]
        
    return sight

# find all the space in a house map that a 'Q' threatens
def check_sight(board, row, col):
    sight = []
    directions = [(0,1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    for d in directions:
        sight += line_of_sight(board, row, col, d)
        
    return sight

# removes a queen from its previous position and adds it to a better position
# updates the free_spaces dictionary and queens dictionary accordingly
def successor(board, queens, free_spaces):
    # pick a queen and the space to move it to
    target_queen = max(queens, key=queens.get)
    target_space = min(free_spaces, key=free_spaces.get)
        
    # remove the queen from the house map
    sight = check_sight(board, target_queen[0], target_queen[1])
    for space in sight:
        if space in free_spaces: free_spaces[space] -= 1
        if space in queens: queens[space] -= 1
            
    board = remove_queen(board, target_queen[0], target_queen[1])
    free_spaces[target_queen] = queens[target_queen]
    del queens[target_queen]

    # add it in new space
    board = add_queen(board, target_space[0], target_space[1])
    queens[target_space] = free_spaces[target_space]
    del free_spaces[target_space]

    sight = check_sight(board, target_space[0], target_space[1])
    for space in sight:
        if space in free_spaces: free_spaces[space] += 1
        if space in queens: queens[space] += 1
    
    return board, queens, free_spaces

# Sets up a random board and attempts to find a solution in 1000 moves. If no solution is found in
# 1000 moves, reset the board and try again, up to 100 times
def solve(initial_board, k):
    
    for i in range(100):
        # variables for the state
        board = setup_board(initial_board, k)
        free_spaces, queens = calculate_state(board)

        for i in range(1000):
            board, queens, free_spaces = successor(board, queens, free_spaces)
            if sum(queens.values()) == 0: return (board, True)
    
    return ('', False)
        
# Main Function
if __name__ == "__main__":
    k = int(sys.argv[1])
    board= [ ['.' for c in range(k)] for r in range(k) ]

    solution = solve(board,k)
    print ("Here's what we found:")
    print (printable_board(solution[0]) if solution[1] else "False")