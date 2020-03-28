import pygame, sys
from pygame.locals import *
from generate_sudoku import *

pygame.init()


# BUILD UP DIMENSIONS FROM SMALLEST UNIT TO PREVENT ROUNDING ERROR
# small grid dimensions
SMALL_CELL_SIZE = 20
SMALL_SQUARE_SIZE = SMALL_CELL_SIZE * 3
SMALL_DIMENSION = SMALL_SQUARE_SIZE * 3

# large grid dimensions
LARGE_CELL_SIZE = SMALL_CELL_SIZE * 2
LARGE_SQUARE_SIZE = LARGE_CELL_SIZE * 3
LARGE_DIMENSION = LARGE_SQUARE_SIZE * 3

# window dimensions
PADDING = 50
WINDOW_DIMENSION = LARGE_DIMENSION * 2 + (PADDING * 4)

#game info
FPSCLOCK = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((WINDOW_DIMENSION, WINDOW_DIMENSION))
FPS = 10

#colours
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0, 70) #partially transparent
TURQOISE = (0, 255, 255, 70)
GREEN = (0, 255, 0, 70)
PURPLE1 = (140,0,255,70)
PURPLE2 = (255,0,140,70)

#font info
SMALL_FONT_SIZE = 15
LARGE_FONT_SIZE = 30
SMALL_FONT = pygame.font.Font('freesansbold.ttf', SMALL_FONT_SIZE)
LARGE_FONT = pygame.font.Font('freesansbold.ttf', LARGE_FONT_SIZE)

# possible coordinates for small grids (top-left corners)
POSSIBLE_COORDINATES_1D = [PADDING, int((WINDOW_DIMENSION - SMALL_DIMENSION) / 2), WINDOW_DIMENSION - SMALL_DIMENSION - PADDING]
POSSIBLE_SMALL_COORDS = []
LARGE_COORD = (2 * PADDING) + SMALL_DIMENSION


def get_all_grid_coordinates():
    for index, x in enumerate(POSSIBLE_COORDINATES_1D):
        for index2, y in enumerate(POSSIBLE_COORDINATES_1D):
            if index == 1 and index2 == 1:
                pass
            else:
                POSSIBLE_SMALL_COORDS.append((x,y))
    
    
def draw_small_grid(x, y):
    """ draw a small grid starting at (x, y) coordinates """
    # draw little lines
    for i in range(y, SMALL_DIMENSION + y, SMALL_CELL_SIZE): # vertical
        pygame.draw.line(DISPLAY, GRAY, (i,x), (i, SMALL_DIMENSION + x))
    for j in range (x, SMALL_DIMENSION + x, SMALL_CELL_SIZE): # horizontal
        pygame.draw.line(DISPLAY, GRAY, (y,j), (SMALL_DIMENSION + y, j))

    # draw thick lines
    for i in range(y, SMALL_DIMENSION + y + 1, SMALL_SQUARE_SIZE): # vertical
        pygame.draw.line(DISPLAY, BLACK, (i,x), (i, SMALL_DIMENSION + x))
    for j in range (x, SMALL_DIMENSION + x + 1, SMALL_SQUARE_SIZE): # horizontal
        pygame.draw.line(DISPLAY, BLACK, (y,j), (SMALL_DIMENSION + y, j))

    
def draw_large_grid(x, y):    
    """ draw the main grid starting at (x, y) coordinates """
    # draw little lines
    for i in range(y, LARGE_DIMENSION + y, LARGE_CELL_SIZE): # vertical
        pygame.draw.line(DISPLAY, GRAY, (i,x), (i, LARGE_DIMENSION + x))
    for j in range (x, LARGE_DIMENSION + x, LARGE_CELL_SIZE): # horizontal
        pygame.draw.line(DISPLAY, GRAY, (y,j), (LARGE_DIMENSION + y, j))

    # draw thick lines
    for i in range(y, LARGE_DIMENSION + y + 1, LARGE_SQUARE_SIZE): # vertical
        pygame.draw.line(DISPLAY, BLACK, (i,x), (i, LARGE_DIMENSION + x))
    for j in range (x, LARGE_DIMENSION + x + 1, LARGE_SQUARE_SIZE): # horizontal
        pygame.draw.line(DISPLAY, BLACK, (y,j), (LARGE_DIMENSION + y, j))
        
     
def draw_all_grids():
    """ draw all small and large grid lines """
    
    # draw the small grids
    for (x,y) in POSSIBLE_SMALL_COORDS:
        draw_small_grid(x, y)

    draw_large_grid(LARGE_COORD, LARGE_COORD)
    
    
def populate_cells_small(board, x, y, board_number):
    """ populate Sudoku board from starting x, y coordinates """
    for i in range(9):
        for j in range(9):
            cell_surf = SMALL_FONT.render('%s' %(board[i][j]), True, BLACK)
            cell_rect = cell_surf.get_rect()
            cell_rect.topleft = (x + i * SMALL_CELL_SIZE + SMALL_CELL_SIZE - SMALL_FONT_SIZE + 1, y + j * SMALL_CELL_SIZE + SMALL_CELL_SIZE - SMALL_FONT_SIZE)
            DISPLAY.blit(cell_surf, cell_rect)
            
    label_surf = LARGE_FONT.render('%s' %(board_number), True, BLACK)
    label_rect = label_surf.get_rect()
    label_rect.topleft = (x + 4 * SMALL_CELL_SIZE + 2, y + SMALL_DIMENSION + SMALL_CELL_SIZE - 10)
    DISPLAY.blit(label_surf, label_rect)            
    
    
def populate_cells_large(board, x, y, board_number):
    """ populate in-focus Sudoku board from starting x, y coordinates """
    for i in range(9):
        for j in range(9):
            cell_surf = LARGE_FONT.render('%s' %(board[i][j]), True, BLACK)
            cell_rect = cell_surf.get_rect()
            cell_rect.topleft = (x + i * LARGE_CELL_SIZE + LARGE_CELL_SIZE - LARGE_FONT_SIZE + 2, y + j * LARGE_CELL_SIZE + LARGE_CELL_SIZE - LARGE_FONT_SIZE - 2)
            DISPLAY.blit(cell_surf, cell_rect)
    label_surf = LARGE_FONT.render('%s' %(board_number), True, BLACK)
    label_rect = label_surf.get_rect()
    label_rect.topleft = (x + 4 * LARGE_CELL_SIZE + LARGE_CELL_SIZE - LARGE_FONT_SIZE + 2, y + LARGE_DIMENSION + LARGE_CELL_SIZE - LARGE_FONT_SIZE + 2)
    DISPLAY.blit(label_surf, label_rect)
            
            

def populate_all_cells(cube, current_large):
    
    """ populate cells of each sudoku board using slices of a cube """
    
    #populate small cells
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                pass
            else:
                populate_cells_small(cube[3*i+j], POSSIBLE_COORDINATES_1D[j], POSSIBLE_COORDINATES_1D[i], 3*i + j + 1)
        

    #populate large cells
    populate_cells_large(cube[4], LARGE_COORD, LARGE_COORD, current_large)
    
    
def draw_large_box(x, y):
    """ draw box around cell that is hovered over """
    cell_x = LARGE_COORD + ((x - LARGE_COORD) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    cell_y = LARGE_COORD + ((y - LARGE_COORD) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    pygame.draw.rect(DISPLAY, BLUE, (cell_x, cell_y, LARGE_CELL_SIZE, LARGE_CELL_SIZE), 2)
    
    
    
def highlight_large_cell(cell_x, cell_y, COLOUR):
    """highlight the cell the passed in colour"""
    
    #pygame.draw.rect(DISPLAY, YELLOW, (cell_x + 1, cell_y + 1, LARGE_CELL_SIZE - 2, LARGE_CELL_SIZE - 2), 0)
    
    surf = pygame.Surface((LARGE_CELL_SIZE - 2, LARGE_CELL_SIZE - 2), pygame.SRCALPHA)
    surf.fill(COLOUR)
    DISPLAY.blit(surf, (cell_x + 1, cell_y + 1))
    
    
def highlight_small_cell(cell_x, cell_y, COLOUR):
    """highlight the cell the passed in colour"""
    surf = pygame.Surface((SMALL_CELL_SIZE - 2, SMALL_CELL_SIZE - 2), pygame.SRCALPHA)
    surf.fill(COLOUR)
    DISPLAY.blit(surf, (cell_x + 1, cell_y + 1))    
    
    
def draw_small_box(x, y):
    """ draw blue box around small grid"""
    cell_x = LARGE_COORD + ((x - LARGE_COORD) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    cell_y = LARGE_COORD + ((y - LARGE_COORD) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE    
    pygame.draw.rect(DISPLAY, BLUE, (x, y, SMALL_DIMENSION, SMALL_DIMENSION), 2)
    
    
def highlight_relevant_cells(x, y, current_large, current_boards):
    """highlight the cells of elements 'related' to hovered over element"""
    
    cell_x = LARGE_COORD + ((x - LARGE_COORD) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    cell_y = LARGE_COORD + ((y - LARGE_COORD) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE   
    
    cell_x_subsquare = ((cell_x - LARGE_COORD) / LARGE_CELL_SIZE) // 3
    cell_y_subsquare = ((cell_y - LARGE_COORD) / LARGE_CELL_SIZE) // 3
    
    cell_x_index = (cell_x - LARGE_COORD) // LARGE_CELL_SIZE
    cell_y_index = (cell_y - LARGE_COORD) // LARGE_CELL_SIZE
    
    #highlighting the cells in the large Sudoku board
    for i in range(LARGE_COORD, LARGE_COORD + LARGE_DIMENSION , LARGE_CELL_SIZE):
        for j in range(LARGE_COORD, LARGE_COORD + LARGE_DIMENSION , LARGE_CELL_SIZE):
            
            if ((i - LARGE_COORD) / LARGE_CELL_SIZE) // 3 == cell_x_subsquare and ((j - LARGE_COORD) / LARGE_CELL_SIZE) // 3 == cell_y_subsquare:
                if i == cell_x and j == cell_y:
                    pass
                elif i == cell_x or j == cell_y:
                    highlight_large_cell(i, j, GREEN)
                else:
                    highlight_large_cell(i, j, TURQOISE)
                    
            elif i == cell_x or j == cell_y:
                highlight_large_cell(i, j, YELLOW)
                
                
    #highlighting the cells in the smaller boards
    for (x, y) in POSSIBLE_SMALL_COORDS:
        for i in range(9):
            for j in range(9):
                if (i, j) == (cell_x_index, cell_y_index):
                    #same column looking 'through' the cube
                    highlight_small_cell(x + i * SMALL_CELL_SIZE, y + j * SMALL_CELL_SIZE, YELLOW)
                elif (i // 3 == cell_x_subsquare and j == cell_y_index and (current_boards[(y,x)] - 1) // 3 == (current_large - 1) // 3):
                    #same subsquare looking down on the cube
                    highlight_small_cell(x + i * SMALL_CELL_SIZE, y + j * SMALL_CELL_SIZE, PURPLE1)
                elif (j // 3 == cell_y_subsquare and i == cell_x_index and (current_boards[(y,x)] - 1)// 3 == (current_large - 1) // 3):
                    #same subsquare looking at the cube from the side
                    highlight_small_cell(x + i * SMALL_CELL_SIZE, y + j * SMALL_CELL_SIZE, PURPLE2)
          
                

def in_large_box(x, y):    
    """ check if mouse hovering over large Sudoku """
    if x >= LARGE_COORD and x <= LARGE_COORD + LARGE_DIMENSION:
        if y >= LARGE_COORD and y <= LARGE_COORD + LARGE_DIMENSION:
            return True
        
    return False


def in_small_box(x, y):
    """ check if mouse is over small Sudoku """
    for (a, b) in POSSIBLE_SMALL_COORDS:
        if a <= x <= a + SMALL_DIMENSION and b <= y <= b + SMALL_DIMENSION:
            return True, (a,b)
        
    return False, None
    
    
def update_display(cube, current_large, current_boards, mouse_x=None, mouse_y=None):
    """ redraw display """
    DISPLAY.fill(WHITE)
    draw_all_grids()
    populate_all_cells(cube.x_elements, current_large)
    
    if mouse_x is not None and mouse_y is not None:
        if in_large_box(mouse_x, mouse_y):
            highlight_relevant_cells(mouse_x, mouse_y, current_large, current_boards)
            draw_large_box(mouse_x, mouse_y)
        in_small, coords = in_small_box(mouse_x, mouse_y)
        if in_small:
            draw_small_box(*coords)
    
    
def main():
    get_all_grid_coordinates()
    
    current_large = 5
    current_boards = {}
    for index, coords in enumerate(POSSIBLE_SMALL_COORDS):
        if index < 4:
            current_boards[coords] = index + 1
        else:
            current_boards[coords] = index + 2
            
    current_boards[5] = (LARGE_COORD, LARGE_COORD)
    
    pygame.display.set_caption('3D Sudoku') 
    
    mouse_x = 0
    mouse_y = 0
    
    cube = Sudoku3D(generate_3d_board())
    update_display(cube, current_large, current_boards)
    
    
    while True: #main game loop
        has_clicked = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
    
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                has_clicked = True
    
        
        # redraw everything
        update_display(cube, current_large, current_boards, mouse_x, mouse_y)    
    
        pygame.display.update()    
        FPSCLOCK.tick(FPS)        
    
        
        
if __name__ == '__main__':
    main()