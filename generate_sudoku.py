import random


def generate_ordered_2d_board():
    """ Generate an unshuffled 2d sudoku board """
    
    board = []
    
    for i in range(3):
        for j in range(3):
            board.append([((x+i) + 3*j) % 9 + 1 for x in range(9)])
            
            
    for x in board:
        print(x)
    
    
generate_ordered_2d_board()