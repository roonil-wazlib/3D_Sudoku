from sudoku_classes import *
from generate_sudoku import *
import copy

class Solver:
    
    def __init__(self, cube, display=None):
        self.display = display
        self.solver = self.setup_sets(copy.deepcopy(cube))
        self.cube = cube
        self.is_incomplete = True
        
        while(self.is_incomplete):
            #for i in range(len(self.cube.x_elements)):
                #print(self.cube.x_elements[i])
                #print("\n\n")
                #print(self.solver.x_elements[i])
                #print("\n\n")
                
            self.loop_cube()
            
            
                
                
    def setup_sets(self, cube):
        """replace empty squares with set containing all possible values"""
        
        representatives = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        
        for x in range(len(cube)):
            for y in range(len(cube)):
                for z in range(len(cube)):
                    if cube.x_elements[x][y][z] == "":
                        cube.insert_value(copy.deepcopy(representatives), y, z, x)
                        
        return cube
    
    
    def set_system_of_representatives(self, x, y, z):
        current_set = self.solver.x_elements[x][y][z]
        #print(x,y,z)
        #eliminate elements from same row
        for i in range(9):
            if self.cube.x_elements[x][i][z] in current_set:
                #print(current_set)
                #print(self.cube.x_elements[x][i][z])
                current_set.remove(self.cube.x_elements[x][i][z])
                
        #eliminate elements from same column
        for i in range(9):
            if self.cube.x_elements[i][y][z] in current_set:
                current_set.remove(self.cube.x_elements[i][y][z])
                
        #eliminate elements from same...uhh...z axis row
        for i in range(9):
            if self.cube.x_elements[x][y][i] in current_set:
                current_set.remove(self.cube.x_elements[x][y][i])
                
        
        self.solver.insert_value(current_set, y, z, x)
        
        if len(current_set) == 1:
            self.cube.insert_value(list(current_set)[0], y, z, x)
            self.solver.insert_value(list(current_set)[0], y, z, x)
            
            
            
    def loop_cube(self):
        """loop through entire cube defining system of representatives of values that can go in each cell"""
        
        self.is_incomplete = False
        for x in range(len(self.cube)):
            for y in range(len(self.cube)):
                for z in range(len(self.cube)):
                    if self.cube.x_elements[x][y][z] == "":
                        #print("CUBE", self.cube.x_elements[x])
                        self.set_system_of_representatives(x, y, z)
                        self.is_incomplete = True
                        