# 3D_Sudoku
A Pygame project to generate and solve Sudoku games in 3 dimensions.


## Generalising Sudoku to higher dimensions

For the purposes of this game, a 'valid' Sudoku cube is considered to be a 9x9x9 cube of elements such that any 2 dimensional
'slice' of the cube is a valid 9x9 Sudoku board. That is to say, any row or column from any perspective contains every value
between 1 and 9 exactly once, and each 3x3 'subsquare' from any perspective has the same property. This has the advantage of being a definition that could be extended to any dimension if you were really bored, but it is slightly counter intuitive in that one might expect the 3x3x3 'subcubes' to behave similarly to the 3x3 'subsquares' in 2 dimensions. Naturally they can not, as we still only have 9 elements, not the 27 here required for uniqueness.

## Generating the cube

The basis for each cube is a 'randomised' 2 dimensional board. The board is generated by continuously adding columns containing
the values 1-9, ordered with modular arithmetic such that the properties of a Sudoku board are satisfied. Thus we get an ordered
2D board that looks like:

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
We can shuffle rows and columns within each 3x9 and 9x3 rectangle, and we can shuffle the orders of the rectangles within
the overall square.

Additionally, we also pseudo-randomly determine a bijection that relabels each element to make the result 'feel' even more random.

The 3 dimensional cube is then generated similarly, by taking the shuffled 2 dimensional plane, and reordering it slightly each
iteration and laying them back to back. Inductively, we could define this process for Sudoku hypercubes of arbitrary dimensions. 

This algorithm is not capable of generating every single 3D Sudoku board - nowhere near. In fact every cube generated is isomorphic under some combination of row and column swaps and relabelling. For the purposes of a game, this is a non-issue.

Finally, now that we have a solution, a function removes elements from the cube at random until there are 500 blank gaps to be
completed by the user (leaving 229 values filled in). This does guarantee the existence of at least one solution, however, it does
not guarantee the existence of a unique solution. Luckily, the distribution of the blank squares is highly unlikely to result in
a puzzle that can not be uniquely solved, so this is not of major concern. The problem of determining whether an arbitrary Latin Square is uniquely completable is an open one, so it is difficult to improve this method particularly easily.


## Optimising Cube Difficulty

While finding a solvable cube is not hard and can be done easily just by removing (say) 500 elements at random, this is not the hardest the game can be. We here define difficulty by the number of blank spaces in the generated game, but are still looking for uniquely solvable games. Therefore, games that have so many blank spaces that there is more than one viable solution are not considered. Also define infomation to represent what we know about the number of possibilities there are for values that can fill each of the remaining blank spaces at any given time. Ie, we know more about a space that could contain {1, 7} than one that could contain {1,3,5,6,7,9}. Finally if a filled space shares a row, column or subsquare with another, say they 'threaten' eachother, analagously to the Rook Problem.

In order to address the problem of maximising difficuly, we first make some approximations. For a given integer n representing the number of blank spaces, it may or may not be possible to arrange them such that the cube is uniquely solvable, but even if it is, not every arrangement will be. Checking every arrangement of blank spaces is not an option - there are 729! / n! of them - far too many to compute. Instead, observe that for any non-blank space added to the cube, we gain the most 'infomation' from it if it 'threatens' the fewest possible number of other filled in spaces. Thus we are more likely to find a unique solution by considering game permutations where the filled/blank spaces are as evenly distributed as possible - ie, the average number of elements that each filled space threatens is minimised.

A method already exists for solving similar problems - Latin Hypercube Sampling (LHS). I attempted to modify this algorithm to do a similar job on my 3D Sudoku cube. The immediate issue is that LHS is only defined for working with independent variables. In the case of a cube, that's x, y and z coordinates. However, squares may also threaten eachother within subsquares, as well as when sharing x, y or z values, and subsquare number (however we might define this ordering) is clearly not independent of coordinates. I have not found a satisfactory way around this hitch.

To simplify the issue, the cube is partioned into different sections and 1 space from each is selected each iteration of the algorithm (which iterates until n blank squares remain). The selection is done in a manner similar to LHS. This ensures that within each iteration, we can prevent any 2 selected squares from threatening one another. This does not work between successive iterations. Additionally, because the Sudoku cube is 3-dimensional, it is impossible to partition into subsquares, as these overlap when considering different planes. Instead, the cube is partitioned into the 27 subcubes, another approximationt that reduces the evenness of the result.

As non-ideal as the resulting game is, it is a much more even result than just randomly selecting elements. Using the lhs algorithm and the solver, I have determined that there exist solvable Sudoku cubes for any number of blank spaces <= 628, much better than my bound using a random generator, which sat at around 570.


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
