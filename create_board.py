import pygame, sys
import copy
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
MENU_SECTION = 600
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
DARKGRAY = (110,110,110)
BLUE = (0, 0, 255)
ORANGE = (255, 180, 0)

# partially transparent for highlighting
YELLOW = (255, 255, 0, 70) 
TURQOISE = (0, 255, 255, 70)
GREEN = (0, 255, 0, 70)
PURPLE1 = (140,0,255,70)
PURPLE2 = (255,0,140,70)
RED = (255, 0, 0, 70)

# font info
SMALL_FONT_SIZE = 15
LARGE_FONT_SIZE = 30
SMALL_FONT = pygame.font.Font('freesansbold.ttf', SMALL_FONT_SIZE)
LARGE_FONT = pygame.font.Font('freesansbold.ttf', LARGE_FONT_SIZE)

# possible coordinates for small grids (top-left corners)
POSSIBLE_COORDINATES_1D = [BORDER + PADDING, int((GAME_SECTION - SMALL_DIMENSION) / 2), GAME_SECTION - BORDER - SMALL_DIMENSION - PADDING]


CUBE_SIDE_LENGTH = 250

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


def in_new_game(x, y):
    """check if mouse/click occured on generate new game button"""
    if x >= GAME_SECTION + 100 and x <= GAME_SECTION + MENU_SECTION - 100:
        if y >= 120 and y <= 160:
            return True
    return False


def in_solve(x, y):
    """check if mouse hover/click occured on solve button"""
    if x >= GAME_SECTION + 100 and x <= GAME_SECTION + MENU_SECTION - 100:
        if y >= 180 and y <= 220:
            return True
    return False


def in_check(x, y):
    """check if mouse hover/click occured on check button"""
    if x >= GAME_SECTION + 100 and x <= GAME_SECTION + MENU_SECTION - 100:
        if y >= 240 and y <= 280:
            return True
    return False    
    
    
def in_x_face(x, y, vertices):
    """check if mouse hover/click occured on x face of cube"""
    return in_polygon((x, y), [vertices[0], vertices[6], vertices[2], vertices[1]])


def in_y_face(x, y, vertices):
    """check if mouse hover/click occured on y face of cube"""
    return in_polygon((x, y), [vertices[0], vertices[5], vertices[4], vertices[6]])


def in_z_face(x, y, vertices):
    """check if mouse hover/click occured on z face of cube"""
    return in_polygon((x, y), [vertices[2], vertices[6], vertices[4], vertices[3]])
    
    
def in_polygon(point, vertices):
    """check if a given point is in a polygon determined by the vertices"""
    current = 0
    while current + 1 != len(vertices):
        
        edge_vector = tuple(map(lambda x : x[0] - x[1], zip(vertices[current + 1], vertices[current]))) 
        point_vector = tuple(map(lambda x : x[0] - x[1], zip(point, vertices[current])))
        
        #print(edge_vector[0] * point_vector[1] - point_vector[0]*edge_vector[1])
        if edge_vector[0] * point_vector[1] - edge_vector[1] * point_vector[0] < 0:
            #signed area is negative, point is on wrong side of edge
            return False
        
        current += 1
        
    return True
    
    
def select_box(x, y, current_large):
    """highlight the selected box"""
    (a,b) = coord_lookup[current_large]
    
    cell_x = a + ((x - a) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    cell_y = b + ((y - b) // LARGE_CELL_SIZE) * LARGE_CELL_SIZE
    pygame.draw.rect(DISPLAY, ORANGE, (cell_x, cell_y, LARGE_CELL_SIZE, LARGE_CELL_SIZE), 2)
    
    
def get_selected_coordinates(x, y, current_large):
    """get coordinates from x perspective of selected box"""
    (a,b) = coord_lookup[current_large]
    
    x = ((x - a) // LARGE_CELL_SIZE)
    y = ((y - b) // LARGE_CELL_SIZE)
    
    return x, y
    
    
def update_display(cube, current_large, current_dim, incorrect, vertices, selected=None, mouse_x=None, mouse_y=None):
    """ redraw display """
    DISPLAY.fill(WHITE)
    draw_all_grids(current_large)
    draw_menu(vertices)
    
    if current_dim == "x":
        cube_ls = cube.x_elements
        draw_x_view_parallelogram(vertices, fill_colour=YELLOW)
        
    elif current_dim == "y":
        cube_ls = cube.y_elements
        draw_y_view_parallelogram(vertices, fill_colour=YELLOW)
    else:
        cube_ls = cube.z_elements
        draw_z_view_parallelogram(vertices, fill_colour=YELLOW)
    populate_all_cells(cube_ls, current_large)
    
    
    if mouse_x is not None and mouse_y is not None:
        if in_large_box(mouse_x, mouse_y, current_large):
            highlight_relevant_cells(mouse_x, mouse_y, current_large)
            draw_large_box(mouse_x, mouse_y, current_large)
        in_small, coords = in_small_box(mouse_x, mouse_y, current_large)
        if in_small:
            draw_small_box(*coords, current_large)
        elif in_check(mouse_x, mouse_y):
            draw_check(BLUE)
        elif in_solve(mouse_x, mouse_y):
            draw_solve(BLUE)
        elif in_new_game(mouse_x, mouse_y):
            #give blue border to new game box
            draw_new_game(BLUE)
        elif in_x_face(mouse_x, mouse_y, vertices):
            #give x face blue border
            if current_dim == 'x':
                draw_x_view_parallelogram(vertices, BLUE, YELLOW)
            else:
                draw_x_view_parallelogram(vertices, BLUE)
        elif in_y_face(mouse_x, mouse_y, vertices):
            if current_dim == 'y':
                draw_y_view_parallelogram(vertices, BLUE, YELLOW)
            else:
                draw_y_view_parallelogram(vertices, BLUE)
        elif in_z_face(mouse_x, mouse_y, vertices):
            if current_dim == 'z':
                draw_z_view_parallelogram(vertices, BLUE, YELLOW)
            else:
                draw_z_view_parallelogram(vertices, BLUE)
            
    if selected is not None:
        #give border to current selected box
        select_box(*selected, current_large)
        
    #highlight any incorrect squares red
    mark_incorrect(current_dim, incorrect, current_large)
    label_cube(vertices)
        
        
def get_grid_coords(x, y, z, current_large):
    """get the grid coordinates of a value from it's in-cube coordinates"""
    board = z + 1
    board_coordinates = coord_lookup[board]
    
    if board == current_large:
        x_coord = y * LARGE_CELL_SIZE + board_coordinates[0]
        y_coord = x * LARGE_CELL_SIZE + board_coordinates[1]
    else:
        x_coord = y * SMALL_CELL_SIZE + board_coordinates[0]
        y_coord = x * SMALL_CELL_SIZE + board_coordinates[1]
        
    return x_coord, y_coord, board == current_large
        
            
def mark_incorrect(current_dim, incorrect, current_large):
    """mark the incorrect squares in red"""
    for item in incorrect:
        if current_dim == "x":
            x, y, is_big = get_grid_coords(*item, current_large)
        elif current_dim == "y":
            x, y, is_big = get_grid_coords(item[0], item[2], item[1], current_large)
        else:
            x, y, is_big = get_grid_coords(item[1], item[2], item[0], current_large)
        if is_big:
            highlight_large_cell(x, y, RED)
        else:
            highlight_small_cell(x, y, RED)
            
    
def draw_menu(vertices):
    """ draw menu """
    draw_new_game(BLACK)
    draw_solve(BLACK)
    draw_check(BLACK)
    
    draw_3D_cube(vertices)
    label_cube(vertices)
    
    
def draw_new_game(COLOUR):
    """draw new game button"""
    # draw new gamebutton
    pygame.draw.rect(DISPLAY, COLOUR, (GAME_SECTION + 100, 120, MENU_SECTION - 200, 40), 2)
    generate_surf = LARGE_FONT.render("NEW GAME", True, BLACK)
    generate_rect = generate_surf.get_rect()
    generate_rect.topleft = (GAME_SECTION + 220, 128)
    DISPLAY.blit(generate_surf, generate_rect)    
    
    
def draw_solve(COLOUR):
    """draw solve button"""
    pygame.draw.rect(DISPLAY, COLOUR, (GAME_SECTION + 100, 180, MENU_SECTION - 200, 40), 2)
    generate_surf = LARGE_FONT.render("SOLVE", True, BLACK)
    generate_rect = generate_surf.get_rect()
    generate_rect.topleft = (GAME_SECTION + 260, 188)
    DISPLAY.blit(generate_surf, generate_rect)
    
    
def draw_check(COLOUR):
    """draw check game button"""
    pygame.draw.rect(DISPLAY, COLOUR, (GAME_SECTION + 100, 240, MENU_SECTION - 200, 40), 2)
    check_surf = LARGE_FONT.render("CHECK", True, BLACK)
    check_rect = check_surf.get_rect()
    check_rect.topleft = (GAME_SECTION + 255, 248)
    DISPLAY.blit(check_surf, check_rect)
    

def get_cube_vertices():
    """generate list of cube vertices"""
    midpoint = MENU_SECTION / 2 + GAME_SECTION
    start = 340

    vertex1 = (midpoint, start + 2 * CUBE_SIDE_LENGTH)
    vertex2 = (midpoint + int(3**0.5 * CUBE_SIDE_LENGTH / 2), start + 1.5 * CUBE_SIDE_LENGTH)
    vertex3 = (midpoint + int(3**0.5 * CUBE_SIDE_LENGTH / 2), start + 0.5 * CUBE_SIDE_LENGTH)
    vertex4 = (midpoint, start)
    vertex5 = (midpoint - int(3**0.5 * CUBE_SIDE_LENGTH / 2), start + 0.5 * CUBE_SIDE_LENGTH)
    vertex6 = (midpoint - int(3**0.5 * CUBE_SIDE_LENGTH / 2), start + 1.5 * CUBE_SIDE_LENGTH)
    vertex7 = (midpoint, start + CUBE_SIDE_LENGTH)
    vertices = [vertex1, vertex2, vertex3, vertex4, vertex5, vertex6, vertex7]
    
    return vertices
    
    
def draw_3D_cube(vertices):
    """draw a 3D cube image"""
    draw_x_view_parallelogram(vertices)
    draw_y_view_parallelogram(vertices)
    draw_z_view_parallelogram(vertices)
    
    
def label_cube(vertices):
    """label the faces of the cube"""
    x_surf = LARGE_FONT.render("X", True, BLACK)
    x_rect = x_surf.get_rect()
    x_rect.topleft = ((vertices[0][0] + vertices[2][0]) / 2 , (vertices[2][1] + vertices[0][1]) / 2 - 12)
    DISPLAY.blit(x_surf, x_rect)
    
    y_surf = LARGE_FONT.render("Y", True, BLACK)
    y_rect = y_surf.get_rect()
    y_rect.topleft = ((vertices[5][0] + vertices[6][0]) / 2 - 12, (vertices[6][1] + vertices[5][1]) / 2 - 12)
    DISPLAY.blit(y_surf, y_rect)
    
    z_surf = LARGE_FONT.render("Z", True, BLACK)
    z_rect = z_surf.get_rect()
    z_rect.topleft = ((vertices[4][0] + vertices[2][0]) / 2 - 10, (vertices[2][1] + vertices[4][1]) / 2 - 12)
    DISPLAY.blit(z_surf, z_rect)       
    
    
def draw_x_view_parallelogram(vertices, border_colour=BLACK, fill_colour=GRAY):
    """draw the x_view face of the cube"""
    pygame.draw.polygon(DISPLAY, fill_colour, (vertices[0], vertices[1], vertices[2], vertices[6]))
    pygame.draw.polygon(DISPLAY, border_colour, (vertices[0], vertices[1], vertices[2], vertices[6]), 5)
    
    
def draw_y_view_parallelogram(vertices, border_colour=BLACK, fill_colour=DARKGRAY):
    """draw the z_view face of the cube"""
    pygame.draw.polygon(DISPLAY, fill_colour, (vertices[0], vertices[6], vertices[4], vertices[5]))
    pygame.draw.polygon(DISPLAY, border_colour, (vertices[0], vertices[6], vertices[4], vertices[5]), 5)
    
    
def draw_z_view_parallelogram(vertices, border_colour=BLACK, fill_colour=WHITE):
    """draw the y_view face of the cube"""
    pygame.draw.polygon(DISPLAY, fill_colour, (vertices[6], vertices[2], vertices[3], vertices[4]))
    pygame.draw.polygon(DISPLAY, border_colour, (vertices[6], vertices[2], vertices[3], vertices[4]), 5)
    
    
    
def get_value(key, val=""):
    """ get value of number key typed """
    if key == pygame.K_1:
        val = 1
    elif key == pygame.K_2:
        val = 2
    elif key == pygame.K_3:
        val = 3
    elif key == pygame.K_4:
        val = 4
    elif key == pygame.K_5:
        val = 5
    elif key == pygame.K_6:
        val = 6
    elif key == pygame.K_7:
        val = 7
    elif key == pygame.K_8:
        val = 8
    elif key == pygame.K_9:
        val = 9
    elif key == pygame.K_0:
        val = 0
        
    return val
    
    
def main():
    #start with center board in focus
    current_large = 5
    current_dim = "x"
    incorrect = []
    
    pygame.display.set_caption('3D Sudoku')
    get_all_grid_coordinates(current_large)
    vertices = get_cube_vertices()

    solved_cube_ls = generate_3d_board()
    solution = copy.deepcopy(solved_cube_ls)
    game_cube = convert_to_game(solved_cube_ls)
    solved_cube = Sudoku3D(solution)
    cube = Sudoku3D(game_cube, False)
    
    update_display(cube, current_large, current_dim, incorrect, vertices)
    
    selected = None
    
    while True: #main game loop
        has_clicked = False
        val = ""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
    
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                has_clicked = True
                
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_x:
                    #flip to x view
                    current_dim = "x"
                    
                elif event.key == pygame.K_y:
                    #flip to y view
                    current_dim = "y"
                    
                elif event.key == pygame.K_z:
                    #flip to z view
                    current_dim = "z"
                    
                else:
                    val = get_value(event.key)
                    
                    if selected is not None and val != "":
                        #get coordinates of selected square
                        x, y = get_selected_coordinates(*selected, current_large)
                        z = current_large - 1
                        
                        #update value of that square
                        if current_dim == "x":
                            cube.insert_value(val, x, y, z)
                            
                        elif current_dim == "y":
                            cube.insert_value(val, z, y, x)
                            
                        else:
                            cube.insert_value(val, y, z, x)
    
        if has_clicked:
            in_small, coords = in_small_box(mouse_x, mouse_y, current_large)
            selected = None
            
            if in_small:
                #change current_large
                current_large = board_number_lookup[coords]
                
            elif in_large_box(mouse_x, mouse_y, current_large):
                #set current selection to something
                selected = (mouse_x, mouse_y)
                
            elif in_new_game(mouse_x, mouse_y):
                #generate new game
                solved_cube_ls = generate_3d_board()
                solution = copy.deepcopy(solved_cube_ls)
                game_cube = convert_to_game(solved_cube_ls)
                solved_cube = Sudoku3D(solution)
                cube = Sudoku3D(game_cube, False)
                
            elif in_solve(mouse_x, mouse_y):
                #solve game
                cube = solved_cube
                
            elif in_check(mouse_x, mouse_y):
                #get incorrect values
                incorrect = cube.check(solved_cube)
                
            elif in_x_face(mouse_x, mouse_y, vertices):
                current_dim = "x"
                
            elif in_y_face(mouse_x, mouse_y, vertices):
                current_dim = "y"
                
            elif in_z_face(mouse_x, mouse_y, vertices):
                current_dim = "z"
            
        # redraw everything
        get_all_grid_coordinates(current_large)
        update_display(cube, current_large, current_dim, incorrect, vertices, selected, mouse_x, mouse_y)    
    
        pygame.display.update()    
        FPSCLOCK.tick(FPS)        
    
        
        
if __name__ == '__main__':
    main()