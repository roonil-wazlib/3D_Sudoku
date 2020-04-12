from sudoku_classes import *
from generate_sudoku import *
from create_board import *
from solver import *
import copy
import time

class Solver:
    
    def __init__(self, cube, vertices=None):
        self.vertices = vertices
        self.solver = self.setup_sets(copy.deepcopy(cube))
        self.cube = cube
        self.is_incomplete = True
        self.something_changed = True
        
        while self.is_incomplete and self.something_changed:
            self.something_changed = False
            self.loop_cube()  
                
                
    def setup_sets(self, cube):
        """
        replace all empty squares with set containing all possible values
        """
        
        representatives = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        
        for x in range(len(cube)):
            for y in range(len(cube)):
                for z in range(len(cube)):
                    if cube.x_elements[x][y][z] == "":
                        cube.insert_value(copy.deepcopy(representatives), y, z, x)
                        
        return cube
    
    
    def set_system_of_representatives(self, x, y, z):
        """
        set the value of an unknown cell at coordinates (x,y,z) to be a set consisting of
        all elements not contained in the cell's corresponding rows, columns and subsquares
        in any direction
        """
        
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
            self.something_changed = True
            self.cube.insert_value(list(current_set)[0], y, z, x)
            self.solver.insert_value(list(current_set)[0], y, z, x)
            
            
            
    def loop_cube(self):
        """
        loop through entire cube defining system of representatives of values that can go in each cell
        """
        
        self.is_incomplete = False
        for x in range(len(self.cube)):
            for y in range(len(self.cube)):
                for z in range(len(self.cube)):
                    if self.cube.x_elements[x][y][z] == "":
                        if self.vertices is not None:
                            #update display to be like a mouse hovering over current cell
                            #but only if this has been called with vertices initalised, because running
                            #the visuals is time consuming
                            get_all_grid_coordinates(x+1)
                            mouse_x, mouse_y, _ = get_grid_coords(z,y,x,x+1)
                            update_display(self.cube, x+1, "x", [], self.vertices, mouse_x=mouse_x, mouse_y=mouse_y)
                            pygame.display.update()
                            FPSCLOCK.tick(FPS)             
                            
                        self.set_system_of_representatives(x, y, z)
                        self.is_incomplete = True
                        
                        
                        
                        
class BadSolver:
    """
    Concept: Recurse after any change and remove that value from any 'adjacent' cells, recursing again
    on each of those if that value changes.
    Reality: Slow as
    """
    def __init__(self, cube, vertices=None):
        self.vertices = vertices
        self.solver = self.setup_sets(copy.deepcopy(cube))
        self.cube = cube
        self.is_incomplete = True
        self.something_changed = True
        
        while self.is_incomplete and self.something_changed:
            self.something_changed = False
            self.loop_cube()
            
            
    def setup_sets(self, cube):
        """
        replace all empty squares with set containing all possible values
        """
        
        representatives = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        
        for x in range(len(cube)):
            for y in range(len(cube)):
                for z in range(len(cube)):
                    if cube.x_elements[x][y][z] == "":
                        cube.insert_value(copy.deepcopy(representatives), y, z, x)
                        
        return cube
    
    
    def loop_cube(self):
        """
        loop through entire cube defining system of representatives of values that can go in each cell
        """
        
        self.is_incomplete = False
        for x in range(len(self.cube)):
            for y in range(len(self.cube)):
                for z in range(len(self.cube)):
                    if self.cube.x_elements[x][y][z] == "":    
                        self.set_system_of_representatives(x, y, z)
                        self.is_incomplete = True
                        
                        
                        
                        
    def set_system_of_representatives(self, x, y, z):
        current_set = self.solver.x_elements[x][y][z]
    
        #eliminate elements from same row
        for i in range(y):
            if self.cube.x_elements[x][i][z] in current_set:
                current_set.remove(self.cube.x_elements[x][i][z])
    
        #eliminate elements from same column
        for i in range(x):
            if self.cube.x_elements[i][y][z] in current_set:
                current_set.remove(self.cube.x_elements[i][y][z])
    
        #eliminate elements from same...uhh...z axis row
        for i in range(z):
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
            self.something_changed = True
            value = list(current_set)[0]
            self.cube.insert_value(value, y, z, x)
            self.solver.insert_value(value, y, z, x)
            self.backtrack(x, y, z, value)
            
            
        
    def backtrack(self, x, y, z, val):
        
        #check row:
        #remove val from items in same row
        for i in range(9):
            
            current_set = self.solver.x_elements[x][i][z]
            self.update_display(x, i, z)
            if self.cube.x_elements[x][i][z] == "" and val in current_set:
                new_val = self.remove_val(x, i, z, val, current_set)
                if new_val != -1:
                    self.backtrack(x, i, z, new_val)
                    
    
        #backtrack column
        for i in range(9):
            current_set = self.solver.x_elements[i][y][z]
            self.update_display(i, y, z)
            if self.cube.x_elements[i][y][z] == "" and val in current_set:
                new_val = self.remove_val(i, y, z, val, current_set)
                if new_val != -1:
                    self.backtrack(i, y, z, new_val)
    
    
        #backtrack same...uhh...z axis row
        for i in range(9):
            current_set = self.solver.x_elements[x][y][i]
            self.update_display(x, y, i)
            if self.cube.x_elements[x][y][i] == "" and val in current_set:
                new_val = self.remove_val(x, y, i, val, current_set)
                if new_val != -1:
                    self.backtrack(x, y, i, new_val)

    
        #eliminate elements from same subsquare
        #subsquare coords : y // 3, z // 3
        #fix x
        for i in range(3):
            for j in range(3):
                current_set = self.solver.x_elements[x][3*(y//3)+j][3*(z//3)+i]
                self.update_display(x, 3*(y//3)+j, 3*(z//3)+i)
                if self.cube.x_elements[x][3*(y//3)+j][3*(z//3)+i] == "" and val in current_set:
                    new_val = self.remove_val(x, 3*(y//3)+j, 3*(z//3)+i, val, current_set)
                    if new_val != -1:
                        self.backtrack(x, 3*(y//3)+j, 3*(z//3)+i, new_val)
                        
                current_set = self.solver.x_elements[3*(x//3)+j][y][3*(z//3)+i]
                self.update_display(3*(x//3)+j, y, 3*(z//3)+i)
                if self.cube.x_elements[3*(x//3)+j][y][3*(z//3)+i] == "" and val in current_set:
                    new_val = self.remove_val(3*(x//3)+j, y, 3*(z//3)+i, val, current_set)
                    if new_val != -1:
                        self.backtrack(3*(x//3)+j, y, 3*(z//3)+i, new_val)
                        
                current_set = self.solver.x_elements[3*(x//3)+j][3*(y//3)+i][z]
                self.update_display(3*(x//3)+j, 3*(y//3)+i, z)
                if self.cube.x_elements[3*(x//3)+j][3*(y//3)+i][z] == "" and val in current_set:
                    new_val = self.remove_val(3*(x//3)+j, 3*(y//3)+i, z, val, current_set)
                    if new_val != -1:
                        self.backtrack(3*(x//3)+j, 3*(y//3)+i, z, new_val)
                    
                    
                    
                    
    def remove_val(self, x, y, z, val, current_set):
        """  \_(' . ')_/  """
        current_set.remove(val)
        if len(current_set) == 1:
            self.something_changed = True
            value = list(current_set)[0]
            self.cube.insert_value(value, y, z, x)
            self.solver.insert_value(value, y, z, x)
            
            return value
        
        return -1
        
        
        
    def update_display(self, x, y, z):
        if self.vertices is not None:
            #update display to be like a mouse hovering over current cell
            #but only if this has been called with vertices initalised, because running
            #the visuals is time consuming
            get_all_grid_coordinates(x+1)
            mouse_x, mouse_y, _ = get_grid_coords(z,y,x,x+1)
            update_display(self.cube, x+1, "x", [], self.vertices, mouse_x=mouse_x, mouse_y=mouse_y)
            pygame.display.update()
            FPSCLOCK.tick(FPS)               