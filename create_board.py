import pygame, sys
from pygame.locals import *

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
PADDING = 25
WINDOW_DIMENSION = LARGE_DIMENSION * 2 + (PADDING * 4)


FPSCLOCK = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((WINDOW_DIMENSION, WINDOW_DIMENSION))

BLACK = (0, 0, 0)
WHITE = (255,255,255)
GRAY = (200, 200, 200)

FPS = 10


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
    # possible coordinates for small grids (top-left corners)
    possible_coordinates = [PADDING, int((WINDOW_DIMENSION - SMALL_DIMENSION) / 2), WINDOW_DIMENSION - SMALL_DIMENSION - PADDING]
    
    # draw the small grids
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                pass
            else:
                print(possible_coordinates[i], possible_coordinates[j])
                draw_small_grid(possible_coordinates[i], possible_coordinates[j])


    # draw the large grid
    start_x = start_y = (2 * PADDING) + SMALL_DIMENSION
    draw_large_grid(start_x, start_y)
    
    
    
def main():
    pygame.init()
    pygame.display.set_caption('Pls work') 
    
    DISPLAY.fill(WHITE)
    
    draw_all_grids()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)   
        
        
if __name__ == '__main__':
    main()