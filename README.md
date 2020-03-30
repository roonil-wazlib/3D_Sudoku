# 3D_Sudoku
A Pygame project to generate and solve Sudoku games in 3 dimensions.


## Generalising Sudoku to higher dimensions

For the purposes of this game, a 'valid' Sudoku cube is considered to be a 9x9x9 cube of elements such that any 2 dimensional
'slice' of the cube is a valid 9x9 Sudoku board. That is to say, any row or column from any perspective contains every value
between 1 and 9 exactly once, and each 3x3 'subsqare' from any perspective has the same property.

## Generating the cube

The basis for each cube is a 'randomised' 2 dimensional board. The board is generated by continuously adding columns containing
the values 1-9, ordered with modular arithmetic such that the properties of a Sudoku board are satisfied. Thus we get an ordered
2x2 board that looks like:

1 2 3 4 5 6 7 8 9

4 5 6 7 8 9 1 2 3

7 8 9 1 2 3 4 5 6

2 3 4 5 6 7 8 9 1

5 6 7 8 9 1 2 3 4

8 9 1 2 3 4 5 6 7

3 4 5 6 7 8 9 1 2

6 7 8 9 1 2 3 4 5

9 1 2 3 4 5 6 7 8


Then, in order to give the game a semi-random appearance, the board is 'shuffled' such that the Sudoku properties are maintained.
Thus, we can shuffle rows and columns within each 3x9 and 9x3 rectangle, and we can shuffle the orders of the rectangles within
the overall square.

Additionally, we also pseudo-randomly determine a bijection to relabel each element.

The 3 dimensional cube is then generated similarly, by taking the shuffled 2 dimensional plane, and reordering it slightly each
iteration and laying them back to back. Inductively, we could define this process for Sudoku hypercubes of arbitrary dimensions.

Finally, now that we have a solution, a function removes elements from the cube at random until there are 500 blank gaps to be
completed by the user (leaving 229 values filled in). This does guarantee the existence of at least one solution, however, it does
not guarantee the existence of a unique solution. Luckily, the distribution of the blank squares is highly unlikely to result in
a puzzle that can not be uniquely solved, so this is not of major concern.


## How the game works

The game is implemented using Pygame. The view consists of 9 numbered Sudoku squares, corresponding to the 9 stacked layers of 
the board as viewed from the current perspective. This perspective can be changed at any time, either by selecting the face of 
the cube on the graphic on the right hand side, or by selecting x y or z using the keyboard. The 9 squares will repopulate at
this time.

When hovering over a cell on the selected board, the cells in the corresponding rows, columns and subsquares will be highlighted
in each of the 9 boards. These differenct coloured highlights represent the cells that are within the same row/column in any dimension
(yellow), or in the same 3x3 subsquare (blue, pink, purple). Within each of those colours, no value can be repeated.

To edit a square, select it with your mouse, and use your keyboard to add a value. Backspace deletes the value in that cell. At any
time the user may check their solution by clicking the check button, and any incorrect values will be highlighted in red. Users
can also generate a new game, or give up and click the solve button.


## Solving the puzzle (automatically)

The solve button does not immediately display the solution, although this is stored from the time of puzzle generation. Instead, it
runs the solver algorithm, and visualises it's progress by highlighting the squares corresponding to the cell currently being looked
at by the solver.

The solver works by looping through the 729 cells in the puzzle systematically, at each step calculating the set of all possible values
that can go in that cell by looking at the corresponding rows, columns and subsquares. When that set has a size of 1, that element is
inserted into the puzzle. This proceeds until all cells have been filled.