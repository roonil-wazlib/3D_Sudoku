class Sudoku3D:
    
    def __init__(self, ls):
        self.x_elements = ls # list representation in column form as viewed from x axis
        self.y_elements = self.get_y_view()
        self.z_elements = self.get_z_view()
    
        
    def get_x_view(self):
        return self.elements
    
    
    def get_y_view(self):
        """
        'rotate' Sudoku cube to get view from y perspective
        """
        
        # nth list of all 2nd tier lists in x_view forms columns of nth 'layer' in y_view
        
        y_view = []
        for i in range(len(self.x_elements)): # works for arbitrary sized sudoku
            y_view.append([x[i] for x in self.x_elements])
            
        return y_view
    
    
    def get_z_view(self):
        """
        'rotate' Sudoku cube to get view from z perspective
        """
        
        # we want nth element of all columns for all layers in x_view
        
        z_view = []
        
        for i in range(len(self.x_elements)): # works for arbitrary sized sudoku
            z_view.append([[x[i] for x in y] for y in self.x_elements])
            
        return z_view
            
            