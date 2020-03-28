class Sudoku:
    
    def __init__(self, ls):
        self.board = ls
        
        if not self.is_correct():
            #throw error
            print(self.board)
            raise Exception("This is an invalid Sudoku board")
        
        else:
            print("VALID")

    
    def is_correct(self):
        """return True if current board violates Latin Square properties of Sudoku"""
        
        if self._x_correct() and self._y_correct() and self._sub_squares_correct():
            return True
        else:
            return False
        
    
    def _y_correct(self):
        """check columns all valid latin square columns"""
        
        for i in range(len(self.board)):
            items = set()
            for element in self.board[i] :
                if element in items and element != "":
                    return False
                else:
                    items.add(element)
                    
        return True
                
                
    def _x_correct(self):
        """check rows all latin square rows"""
        for i in range(len(self.board)):
            items = set()
            for column in self.board:
                if column[i] in items and column[i] != "":
                    return False
                else:
                    items.add(column[i])
                    
        return True
                    
    
    def _sub_squares_correct(self):
        """check if each subsquare is a valid sudoku subsquare"""
        for i in range(int(len(self.board) / 3)):
            items = set()
            for j in range(int(len(self.board) / 3)):
                if self.board[3*i][j] in items and self.board[3*i][j] != "":
                    return False
                else:
                    items.add(self.board[3*i][j])
                    
        return True
    
    
    def __len__(self):
        return len(self.board)
        
    def __getitem__(self, index):
        return self.board[index]
    
    def __repr__(self):
        output = ""
        for item in self.board:
            output += " ".join([str(x) for x in item])
            output += "\n"
        return output
                
        

class Sudoku3D(Sudoku):
    
    def __init__(self, ls):
        self.x_elements = [Sudoku(x) for x in ls] # list representation in column form as viewed from x axis
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
            y_view.append([x.board[i] for x in self.x_elements])
            
        y_view = [Sudoku(x) for x in y_view]
        return y_view
    
    
    def get_z_view(self):
        """
        'rotate' Sudoku cube to get view from z perspective
        """
        
        # we want nth element of all columns for all layers in x_view
        
        z_view = []
        
        for i in range(len(self.x_elements)): # works for arbitrary sized sudoku
            z_view.append([[x[i] for x in y.board] for y in self.x_elements])
            
        z_view = [Sudoku(x) for x in z_view]
        return z_view
            
            