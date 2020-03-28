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
    """generate 3D cube from 2D board"""
    layer = generate_ordered_2d_board()
    cube = []
    for i in range(len(layer)):
        new_layer = []
        for column in layer:
            new_column = []
            #this nested mess is to ensure that none of the sub 3x3 squares violates sudoku rules from any x y or z perspective
            #(also the Latin Square rules but the subsquares is trickier and the cause of more mess)
            for j in range(3):
                for k in range(3):
                    #lot of 3 = (i+j) % 3 ##CORRECT
                    #index within lot = (i + k + (i//3)) % 3 
                    ##OK TBH THIS MADE SENSE WHEN I FIGURED IT OUT IN A CAFFIENE INDUCED FRENZY AT 2AM IN THE FUCKING MORNING
                    #BUT I NO LONGER HAVE ANY IDEA WTF IT IS MEANT TO DO SO JUST...BELIEVE IT??
                    new_column.append(column[3*((i + j) % 3) + (i + k + (i // 3)) % 3])
            new_layer.append(new_column)
        cube.append(new_layer)
        
    return cube
    
    
#board = Sudoku(generate_ordered_2d_board())
#cube = Sudoku3D(generate_3d_board())
#print(cube.y_elements)
#print(cube.z_elements)
#board2 = generate_ordered_2d_board()
#board2[0][0] = 2
#board2 = Sudoku(board2)
#print(board2.is_correct())


square = []
for i in range(9):
    col = []
    for j in range(9):
        col.append((i+j)%9 + 1)
    square.append(col)
    
board = Sudoku(square)
print(board)