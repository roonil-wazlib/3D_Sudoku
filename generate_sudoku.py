import random
from sudoku_classes import Sudoku3D


def generate_ordered_2d_board():
    """ Generate an unshuffled 2d sudoku board """
    
    board = []
    
    for i in range(3):
        for j in range(3):
            board.append([((x+i) + 3*j) % 9 + 1 for x in range(9)])
            
    return board
    
    
def generate_3d_board():
    """place holder 3d generater to test Sudoku3D class"""
    layer = generate_ordered_2d_board()
    cube = []
    for i in range(len(layer)):
        cube.append(layer)
    return cube
    
    
generate_ordered_2d_board()
board = Sudoku3D(generate_3d_board())
print(board.y_elements)
print(board.z_elements)
