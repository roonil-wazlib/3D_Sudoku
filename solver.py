from sudoku_classes import *
from generate_sudoku import *
from create_board import *
import copy
import time

class Solver:
    
    def __init__(self, cube, vertices=None):
        self.vertices = vertices
        self.solver = self.setup_sets(copy.deepcopy(cube))
        self.cube = cube
        self.is_incomplete = True
        
        while(self.is_incomplete):
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

        #eliminate elements from same row
        for i in range(9):
            if self.cube.x_elements[x][i][z] in current_set:
                current_set.remove(self.cube.x_elements[x][i][z])
                
        #eliminate elements from same column
        for i in range(9):
            if self.cube.x_elements[i][y][z] in current_set:
                current_set.remove(self.cube.x_elements[i][y][z])
                
        #eliminate elements from same...uhh...z axis row
        for i in range(9):
            if self.cube.x_elements[x][y][i] in current_set:
                current_set.remove(self.cube.x_elements[x][y][i])
                
                
        #eliminate elements from same subsquare
        #subsquare coords : y // 3, z // 3
        #fix x
        for i in range(3):
            for j in range(3):
                if self.cube.x_elements[x][3*(y//3)+j][3*(z//3)+i] in current_set:
                    current_set.remove(self.cube.x_elements[x][3*(y//3)+j][3*(z//3)+i])
                if self.cube.x_elements[3*(x//3)+j][y][3*(z//3)+i] in current_set:
                    current_set.remove(self.cube.x_elements[3*(x//3)+j][y][3*(z//3)+i])
                if self.cube.x_elements[3*(x//3)+j][3*(y//3)+i][z] in current_set:
                    current_set.remove(self.cube.x_elements[3*(x//3)+j][3*(y//3)+i][z])
        
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
                        if self.vertices is not None:
                            #update display to be like a mouse hovering over current cell
                            get_all_grid_coordinates(x+1)
                            mouse_x, mouse_y, _ = get_grid_coords(z,y,x,x+1)
                            update_display(self.cube, x+1, "x", [], self.vertices, mouse_x=mouse_x, mouse_y=mouse_y)
                            pygame.display.update()
                            FPSCLOCK.tick(FPS)                   
                        self.set_system_of_representatives(x, y, z)
                        self.is_incomplete = True
                        