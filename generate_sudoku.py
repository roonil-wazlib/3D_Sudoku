import random
from sudoku_classes import *


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
    
    
board = Sudoku(generate_ordered_2d_board())
cube = Sudoku3D(generate_3d_board())
print(cube.y_elements)
print(cube.z_elements)
board2 = generate_ordered_2d_board()
board2[0][0] = 2
board2 = Sudoku(board2)
print(board2.is_correct())