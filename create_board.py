import pygame, sys
from pygame.locals import *

# BUILD UP DIMENSIONS FROM SMALLEST UNIT TO PREVENT ROUNDING ERROR

# small grid dimensions
SMALL_CELL_SIZE = 20
SMALL_SQUARE_SIZE = SMALL_CELL_SIZE * 3
SMALL_DIMENSION = SMALL_SQUARE_SIZE * 3

# large grid dimensions
LARGE_CELL_SIZE = SMALL_CELL_SIZE * 3
LARGE_SQUARE_SIZE = LARGE_CELL_SIZE * 3
LARGE_DIMENSION = LARGE_SQUARE_SIZE * 3

# window dimensions
WINDOW_DIMENSION = LARGE_DIMENSION * 2


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
        pygame.draw.line(DISPLAY, GRAY, (i,y), (i, SMALL_DIMENSION+y))
    for j in range (x, SMALL_DIMENSION + x, SMALL_CELL_SIZE): # horizontal
        pygame.draw.line(DISPLAY, GRAY, (x,j), (SMALL_DIMENSION+x, j))

    # draw thick lines
    for i in range(y, SMALL_DIMENSION + y + 1, SMALL_SQUARE_SIZE): # vertical
        pygame.draw.line(DISPLAY, BLACK, (i,y), (i, SMALL_DIMENSION+y))
    for j in range (x, SMALL_DIMENSION + x + 1, SMALL_SQUARE_SIZE): # horizontal
        pygame.draw.line(DISPLAY, BLACK, (x,j), (SMALL_DIMENSION+x, j))

    return None

    
def main():
    pygame.init()
    pygame.display.set_caption('Pls work') 
    
    DISPLAY.fill(WHITE)
    draw_small_grid(10,10)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)   
        
        
if __name__ == '__main__':
    main()