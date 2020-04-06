from sudoku_classes import *
from generate_sudoku import *
from solver import *
import random
import copy


def order_generator(available_indices):
    """randomly determine order of subsquares from which we will remove elements"""
    order = list(range(27))
    random.shuffle(order)
    
    for subcube in order:
        yield available_indices[subcube]
        

def index_generator(x_options, y_options, z_options):
    """randomly determine order of (x, y, z) tuples"""
    random.shuffle(x_options)
    random.shuffle(y_options)
    random.shuffle(z_options)
    
    tuples = [(x, y, z) for x in x_options for y in y_options for z in z_options]
    for item in tuples:
        yield item


def get_subcube_indices():
    """
    Generate dictionary of possible coordinate values for each subcube.
    Used as a reference point for determining the subset of coordinates we can
    choose from at each stage.
    """
    remaining_indices = {}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                z_coords = {3*i, 3*i+1, 3*i+2}
                y_coords = {3*j, 3*j+1, 3*j+2}
                x_coords = {3*k, 3*k+1, 3*k+2}
                remaining_indices[9*i + 3*j + k] = [x_coords, y_coords, z_coords]
                
    return remaining_indices



def get_available_coordinates():
    """
    Generate available coordinate values for overall cube, in form
       coordinates = {(x,y,z), (x2,y2,z2)...}
       
    Part used for latin hypercube sampling aspect of algorithm.
    """
    
    coordinates = set()
    for i in range(9):
        for j in range(9):
            for k in range(9):
                coordinates.add((i, j, k))
        
    return coordinates


def get_blank_game():
    """build a blank game to be populated overtime"""
    game = []
    for _ in range(9):
        plane = []
        for _ in range(9):
            plane.append([""] * 9)
        game.append(plane)
        
    return game


def build_game(num_blank):
    """generate a game of Sudoku with num_blank blank squares, evenly distributed about the board."""
    
    #since all boards isomorphic to a uniquely solvable game should also be uniquely solvable (??),
    #we need only check the ordered case
    sudoku_ls = generate_unshuffled_3d_board()
    
    #generate initial coordinate values, and subcube reference
    subcube_indices = get_subcube_indices()
    available_coordinates = get_available_coordinates()
    
    #generate blank game that we will slowly populate
    #since we know the optimal solution has well over half the squares blank, it is faster to populate than to unpopulate
    #evenly distributing populated squares is the same as evenly distributing unpopulated squares
    game = get_blank_game()
    
    num_selected = 0
    #keeps track of the number of times we've looped
    count = 0
    
    
    while num_selected < 729 - num_blank:
        
        coordinates_this_loop = copy.deepcopy(available_coordinates)
        #loop through subcubes
        for item in order_generator(subcube_indices):
            
            x_options = list(item[0])
            y_options = list(item[1])
            z_options = list(item[2])
            
            for (x, y, z) in index_generator(x_options, y_options, z_options):
                if (x, y, z) in coordinates_this_loop and (x, y, z) in available_coordinates:
                    my_x = x
                    my_y = y
                    my_z = z
                    break
                    
            
            for i in range(9):
                #discard anything that threatens this guy
                coordinates_this_loop.discard((i, y, z))
                coordinates_this_loop.discard((x, i, z))
                coordinates_this_loop.discard((x, y, i))
            
            #remove specific point from overall coordinates. will throw error if I've messed up
            available_coordinates.remove((x, y, z))
            
            game[x][y][z] = sudoku_ls[x][y][z]
            
            num_selected += 1
            if num_selected >= 729 - num_blank:
                break
            
            count += 1
            
    
    return game


def main():
    #testing if various games are solvable:
    
    for i in range(625, 729):
        while True:
            game = build_game(i)
            cube = Sudoku3D(game, False)
            solver = Solver(cube)
            if not solver.is_incomplete:
                print(i)
                break
            
            
main()