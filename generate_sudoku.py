import random
from sudoku_classes import *


def generate_ordered_2d_board():
    """ Generate an unshuffled 2d sudoku board """
    board = []
    
    for i in range(3):
        for j in range(3):
            board.append([((x+i) + 3*j) % 9 + 1 for x in range(9)])
            
    return board


def generate_shuffled_2d_board():
    """ Generate a 'random' 2D Sudoku board """
    
    ordered = generate_ordered_2d_board()
    columns_shuffled = shuffle_columns(ordered)
    # rows_shuffled = shuffle_rows(columns_shuffled)
    relabeled = relabel_values(columns_shuffled)

    return relabeled
    
    
    
def shuffle_columns(board):
    """ Shuffle the columns of a 2D board"""
    shuffled = []
    column_group_order = [0,1,2]
    random.shuffle(column_group_order)
    for i in column_group_order:
        #shuffle columns within each of the 3 column groups
        column_order = [0,1,2]
        random.shuffle([0,1,2])
        for j in column_order:
            shuffled.append(board[3*i + j])
            
    return shuffled
    
    
def shuffle_rows(board):
    """ Shuffle the rows of a 2D board"""
    #returns a 90* rotation but who cares, we're shuffling anyway
    
    #convert rows to columns:
    board = rows_to_columns(board)

    #now shuffle as columns
    return shuffle_columns(board)
    
    
def relabel_values(board):
    """makes the board look more random but actually just produces the same board (isomorphic by relabelling)"""
    values = [1,2,3,4,5,6,7,8,9]
    random.shuffle(values)
    
    output = []
    
    for x in board:
        col = []
        for y in x:
            col.append(values[y-1])
        output.append(col)
        
    return output
    
    
def rows_to_columns(board):
    """Return a 90* rotation of the board in the same list representation"""
    
    output = []
    for i in range(9):
        col = []
        for j in range(9):
            col.append(board[j][i])
        output.append(col)
        
    return output
    
    
def shuffle_cube(cube):
    shuffled = []
    column_group_order = [0,1,2]
    random.shuffle(column_group_order)
    for i in column_group_order:
        #shuffle columns within each of the 3 column groups
        column_order = [0,1,2]
        random.shuffle([0,1,2])
        for j in column_order:
            shuffled.append(cube[3*i + j])

    return shuffled    
    
    
def generate_3d_board():
    """generate 3D cube from 2D board"""
    layer = generate_shuffled_2d_board()
    cube = []
    for i in range(len(layer)):
        new_layer = []
        for column in layer:
            new_column = []
            #this nested mess is to ensure that none of the sub 3x3 squares violates sudoku rules from any x y or z perspective
            #(also the Latin Square rules but the subsquares are trickier and the cause of more mess)
            for j in range(3):
                for k in range(3):
                    #lot of 3 = (i+j) % 3
                    #index within lot = (i + k + (i//3)) % 3 
                    new_column.append(column[3*((i + j) % 3) + (i + k + (i // 3)) % 3])
            new_layer.append(new_column)
        cube.append(new_layer)
        
    return shuffle_cube(cube)


def convert_to_game(cube):
    """ convert a valid Sudoku cube to a solvable game """
    game_cube = cube[:]
    count = 0
    #remove 500 elements from the cube at random
    while count < 500:
        x = random.randrange(0,9,1)
        y = random.randrange(0,9,1)
        z = random.randrange(0,9,1)
        if game_cube[x][y][z] != "":
            count += 1
            game_cube[x][y][z] = ""
        
    return game_cube
    
    
#board = Sudoku(generate_ordered_2d_board())
#cube = Sudoku3D(generate_3d_board())
#print(cube.y_elements)
#print(cube.z_elements)
#board2 = generate_ordered_2d_board()
#board2[0][0] = 2
#board2 = Sudoku(board2)
#print(board2.is_correct())



