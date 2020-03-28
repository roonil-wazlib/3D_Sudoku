import pygame, sys
from pygame.locals import *
from generate_sudoku import *

pygame.init()


# BUILD UP DIMENSIONS FROM SMALLEST UNIT TO PREVENT ROUNDING ERROR
# small grid dimensions
SMALL_CELL_SIZE = 18
SMALL_SQUARE_SIZE = SMALL_CELL_SIZE * 3
SMALL_DIMENSION = SMALL_SQUARE_SIZE * 3

# large grid dimensions
LARGE_CELL_SIZE = SMALL_CELL_SIZE * 2
LARGE_SQUARE_SIZE = LARGE_CELL_SIZE * 3
LARGE_DIMENSION = LARGE_SQUARE_SIZE * 3

# window dimensions
PADDING = 50
BORDER = 30
GAME_SECTION = LARGE_DIMENSION * 3 + 2*BORDER
MENU_SECTION = 800
WINDOW_X = GAME_SECTION + MENU_SECTION
WINDOW_Y = GAME_SECTION

# game info
FPSCLOCK = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

FPS = 10

# colours for text, background and grids
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# partially transparent for highlighting
YELLOW = (255, 255, 0, 70) 
TURQOISE = (0, 255, 255, 70)
GREEN = (0, 255, 0, 70)
PURPLE1 = (140,0,255,70)
PURPLE2 = (255,0,140,70)

# font info
SMALL_FONT_SIZE = 15
LARGE_FONT_SIZE = 30
SMALL_FONT = pygame.font.Font('freesansbold.ttf', SMALL_FONT_SIZE)
LARGE_FONT = pygame.font.Font('freesansbold.ttf', LARGE_FONT_SIZE)

# possible coordinates for small grids (top-left corners)
POSSIBLE_COORDINATES_1D = [BORDER + PADDING, int((GAME_SECTION - SMALL_DIMENSION) / 2), GAME_SECTION - BORDER - SMALL_DIMENSION - PADDING]

# sudoku lookup dictionaries
coord_lookup = {}
board_number_lookup = {}


def get_all_grid_coordinates(current_large):
    """ populate dictionaries with coordinates of each grid and corresponding grid number """
    
    for index, x in enumerate(POSSIBLE_COORDINATES_1D):
        for index2, y in enumerate(POSSIBLE_COORDINATES_1D):
            if index + 3*index2 == current_large - 1:
                pass
            else:
                board_number_lookup[(x,y)] = index + 3*index2 + 1
                coord_lookup[index + 3*index2 + 1] = (x,y)
                

    large_x = ((current_large - 1) % 3) * LARGE_DIMENSION + BORDER
    large_y = ((current_large - 1) // 3) * LARGE_DIMENSION + BORDER
    board_number_lookup[(large_x, large_y)] = current_large
    coord_lookup[current_large] = (large_x, large_y)
    
    
def draw_small_grid(x, y):
    """ draw a small grid starting at (x, y) coordinates """
    
    # draw little lines
    for i in range(x, SMALL_DIMENSION + x, SMALL_CELL_SIZE): # vertical
        pygame.draw.line(DISPLAY, GRAY, (i,y), (i, SMALL_DIMENSION + y))
    for j in range (y, SMALL_DIMENSION + y, SMALL_CELL_SIZE): # horizontal
        pygame.draw.line(DISPLAY, GRAY, (x,j), (SMALL_DIMENSION + x, j))

    # draw thick lines
    for i in range(x, SMALL_DIMENSION + x + 1, SMALL_SQUARE_SIZE): # vertical
        pygame.draw.line(DISPLAY, BLACK, (i,y), (i, SMALL_DIMENSION + y))
    for j in range (y, SMALL_DIMENSION + y + 1, SMALL_SQUARE_SIZE): # horizontal
        pygame.draw.line(DISPLAY, BLACK, (x,j), (SMALL_DIMENSION + x, j))

    
def draw_large_grid(x, y):    
    """ draw the main grid starting at (x, y) coordinates """
    
    # draw little lines
    for i in range(x, LARGE_DIMENSION + x, LARGE_CELL_SIZE): # vertical
        pygame.draw.line(DISPLAY, GRAY, (i,y), (i, LARGE_DIMENSION + y))
    for j in range (y, LARGE_DIMENSION + y, LARGE_CELL_SIZE): # horizontal
        pygame.draw.line(DISPLAY, GRAY, (x,j), (LARGE_DIMENSION + x, j))

    # draw thick lines
    for i in range(x, LARGE_DIMENSION + x + 1, LARGE_SQUARE_SIZE): # vertical
        pygame.draw.line(DISPLAY, BLACK, (i,y), (i, LARGE_DIMENSION + y))
    for j in range (y, LARGE_DIMENSION + y + 1, LARGE_SQUARE_SIZE): # horizontal
        pygame.draw.line(DISPLAY, BLACK, (x,j), (LARGE_DIMENSION + x, j))
        
     
def draw_all_grids(current_large):
    """ draw all small and large grid lines """
    
    (a,b) = coord_lookup[current_large]
    
    # draw the small grids
    for number, (x,y) in coord_lookup.items():
        if number != current_large:
            draw_small_grid(x, y)

    draw_large_grid(a, b)
    
    
def populate_cells_small(board, x, y, board_number):
    """ populate Sudoku board from starting x, y coordinates """
    
    for i in range(9):
        for j in range(9):
            cell_surf = SMALL_FONT.render('%s' %(board[i][j]), True, BLACK)
            cell_rect = cell_surf.get_rect()
            cell_rect.topleft = (x + i * SMALL_CELL_SIZE + SMALL_CELL_SIZE - SMALL_FONT_SIZE + 2, y + j * SMALL_CELL_SIZE + SMALL_CELL_SIZE - SMALL_FONT_SIZE)
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
            cell_rect.topleft = (x + i * LARGE_CELL_SIZE + LARGE_CELL_SIZE - LARGE_FONT_SIZE + 4, y + j * LARGE_CELL_SIZE + LARGE_CELL_SIZE - LARGE_FONT_SIZE)
            DISPLAY.blit(cell_surf, cell_rect)
    label_surf = LARGE_FONT.render('%s' %(board_number), True, BLACK)
    label_rect = label_surf.get_rect()
    label_rect.topleft = (x + 4 * LARGE_CELL_SIZE + LARGE_CELL_SIZE - LARGE_FONT_SIZE + 2, y + LARGE_DIMENSION + LARGE_CELL_SIZE - LARGE_FONT_SIZE + 2)
    DISPLAY.blit(label_surf, label_rect)
            
            

def populate_all_cells(cube, current_large):
    """ populate cells of each sudoku board using slices of a cube """
    
    (a,b) = coord_lookup[current_large]
    
    #populate small cells
    for i in range(3):
        for j in range(3):
            if 3*i + j == current_large - 1:
                pass
            else:
                populate_cells_small(cube[3*i+j], POSSIBLE_COORDINATES_1D[j], POSSIBLE_COORDINATES_1D[i], 3*i + j + 1)
        

    #populate large cells
    populate_cells_large(cube[current_large - 1], a, b, current_large)
    
    
def draw_large_box(x, y, current_large):
    """ draw box around cell that is hovered over """
    
    (a,b) = coord_lookup[current_large]
    
    cell_x = a + ((x - a) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    cell_y = b + ((y - b) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    pygame.draw.rect(DISPLAY, BLUE, (cell_x, cell_y, LARGE_CELL_SIZE, LARGE_CELL_SIZE), 2)
    
    
    
def highlight_large_cell(cell_x, cell_y, COLOUR):
    """highlight the cell the passed in colour"""
    
    surf = pygame.Surface((LARGE_CELL_SIZE - 2, LARGE_CELL_SIZE - 2), pygame.SRCALPHA)
    surf.fill(COLOUR)
    DISPLAY.blit(surf, (cell_x + 1, cell_y + 1))
    
    
def highlight_small_cell(cell_x, cell_y, COLOUR):
    """highlight the cell the passed in colour"""
    surf = pygame.Surface((SMALL_CELL_SIZE - 2, SMALL_CELL_SIZE - 2), pygame.SRCALPHA)
    surf.fill(COLOUR)
    DISPLAY.blit(surf, (cell_x + 1, cell_y + 1))    
    
    
def draw_small_box(x, y, current_large):
    """ draw blue box around small grid"""
    (a,b) = coord_lookup[current_large]
    
    cell_x = a + ((x - a) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    cell_y = b + ((y - b) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE    
    pygame.draw.rect(DISPLAY, BLUE, (x, y, SMALL_DIMENSION, SMALL_DIMENSION), 2)
    
    
def highlight_relevant_cells(x, y, current_large):
    """highlight the cells of elements 'related' to hovered over element"""
    
    (a,b) = coord_lookup[current_large]
    
    cell_x = a + ((x - a) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    cell_y = b + ((y - b) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE   
    
    cell_x_subsquare = ((cell_x - a) / LARGE_CELL_SIZE) // 3
    cell_y_subsquare = ((cell_y - b) / LARGE_CELL_SIZE) // 3
    
    cell_x_index = (cell_x - a) // LARGE_CELL_SIZE
    cell_y_index = (cell_y - b) // LARGE_CELL_SIZE
    
    #highlighting the cells in the large Sudoku board
    for i in range(a, a + LARGE_DIMENSION , LARGE_CELL_SIZE):
        for j in range(b, b + LARGE_DIMENSION , LARGE_CELL_SIZE):
            
            if ((i - a) / LARGE_CELL_SIZE) // 3 == cell_x_subsquare and ((j - b) / LARGE_CELL_SIZE) // 3 == cell_y_subsquare:
                if i == cell_x and j == cell_y:
                    pass
                elif i == cell_x or j == cell_y:
                    highlight_large_cell(i, j, GREEN)
                else:
                    highlight_large_cell(i, j, TURQOISE)
                    
            elif i == cell_x or j == cell_y:
                highlight_large_cell(i, j, YELLOW)
                
                
    #highlighting the cells in the smaller boards
    for number, (x, y) in coord_lookup.items():
        for i in range(9):
            for j in range(9):
                if number == current_large:
                    pass
                elif (i, j) == (cell_x_index, cell_y_index):
                    #same column looking 'through' the cube
                    highlight_small_cell(x + i * SMALL_CELL_SIZE, y + j * SMALL_CELL_SIZE, YELLOW)
                elif (i // 3 == cell_x_subsquare and j == cell_y_index and (number - 1) // 3 == (current_large - 1) // 3):
                    #same subsquare looking down on the cube
                    highlight_small_cell(x + i * SMALL_CELL_SIZE, y + j * SMALL_CELL_SIZE, PURPLE1)
                elif (j // 3 == cell_y_subsquare and i == cell_x_index and (number - 1)// 3 == (current_large - 1) // 3):
                    #same subsquare looking at the cube from the side
                    highlight_small_cell(x + i * SMALL_CELL_SIZE, y + j * SMALL_CELL_SIZE, PURPLE2)
          
                

def in_large_box(x, y, current_large):
    """ check if mouse hovering over large Sudoku """
    (a,b) = coord_lookup[current_large]
    if x >= a and x <= a + LARGE_DIMENSION:
        if y >= b and y <= b + LARGE_DIMENSION:
            return True
        
    return False


def in_small_box(x, y, current_large):
    """ check if mouse is over small Sudoku """
    for number, (a, b) in coord_lookup.items():
        if a <= x <= a + SMALL_DIMENSION and b <= y <= b + SMALL_DIMENSION and number != current_large:
            return True, (a,b)
        
    return False, None
    
    
def update_display(cube, current_large, mouse_x=None, mouse_y=None):
    """ redraw display """
    DISPLAY.fill(WHITE)
    draw_all_grids(current_large)
    populate_all_cells(cube.x_elements, current_large)
    
    if mouse_x is not None and mouse_y is not None:
        if in_large_box(mouse_x, mouse_y, current_large):
            highlight_relevant_cells(mouse_x, mouse_y, current_large)
            draw_large_box(mouse_x, mouse_y, current_large)
        in_small, coords = in_small_box(mouse_x, mouse_y, current_large)
        if in_small:
            draw_small_box(*coords, current_large)
    
    
def main():
    #start with center board in focus
    current_large = 5
    
    pygame.display.set_caption('3D Sudoku')
    get_all_grid_coordinates(current_large)
    cube = Sudoku3D(generate_3d_board())
    update_display(cube, current_large)
    
    
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
    
        if has_clicked:
            in_small, coords = in_small_box(mouse_x, mouse_y, current_large)
            if in_small:
                #change current_large
                current_large = board_number_lookup[coords]
                print(current_large)
                
            else:
                #if square is editable, open edit
                pass
            
            
        # redraw everything
        get_all_grid_coordinates(current_large)
        update_display(cube, current_large, mouse_x, mouse_y)    
    
        pygame.display.update()    
        FPSCLOCK.tick(FPS)        
    
        
        
if __name__ == '__main__':
    main()