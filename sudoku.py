import sys, copy, time, random

class BoardManipulations:
    '''manipulates the grid and string of the sudoku board'''

    #create a test for grid_string inputs
    def assert_string(self, grid_string):
        assert len(grid_string) == 81, 'String is not of length 81'

    #create a test for grid inputs
    def assert_grid(self, grid):
        assert type(grid) == type([]), 'Grid is not a list'
        assert len(grid) == 9, 'Grid does not have 9 rows'
        for row in grid:
            assert len(row) == 9, 'One of the rows in the Grid does not have nine columns'
    
    #create a blank grid
    def blank_grid(self):
        return [[0 for j in xrange(9)] for i in xrange(9)]

    #create blank grid string
    def blank_grid_string(self):
        return '0'*81

    #convert a string to a grid
    def convert_string_to_grid(self, puzzle_string):
        self.assert_string(puzzle_string)
        puzzle_grid = self.blank_grid()     #create a blank grid
        for i in xrange(9):
            for j in xrange(9):
                puzzle_grid[i][j] = int(puzzle_string[:1])  #take the first number and place it in the grid
                puzzle_string = puzzle_string[1:]           #remove the first number from the grid
        return puzzle_grid

    #convert a grid to a string
    def convert_grid_to_string(self, puzzle_grid):
        self.assert_grid(puzzle_grid)
        puzzle_string = ''                                  #create empty string
        for i in xrange(9):                                 #walk along the grid and
            for j in xrange(9):                             #append puzzle_string
                puzzle_string = puzzle_string + str(puzzle_grid[i][j])
        return puzzle_string

    #switch the columns and the rows
    def make_rows(self, puzzle_grid):
        self.assert_grid(puzzle_grid)
        new_grid = self.blank_grid()                        #create empty_grid
        for i in xrange(9):                                 #take each column of the puzzle
            for j in xrange(9):                             #and make a new row on the new grid
                new_grid[i][j] = puzzle_grid[j][i]
        return new_grid


    #switch the squares and the rows
    def make_squares(self, puzzle_grid):
        self.assert_grid(puzzle_grid)
        square = []                                         #create an empty list to contain the contents of a square
        squares = []                                        #create a list that will contain the square lists
        for y in xrange(0,3):                               #create each of the squares
            for z in xrange(0,3):                           #and append the square list with each value
                for i in xrange(0,3):
                    for j in xrange(0,3):
                        square.append(puzzle_grid[(i+(y*3))][(j+(z*3))])
                squares.append(square)                      #append squares list with each square
                square = []
        return squares

    #removes zeros from the board a places a list of number 1-9
    #this creates the possible numbers that can be located in each grid
    def place_lists(self, puzzle_grid):
        self.assert_grid(puzzle_grid)
        new_grid = copy.deepcopy(puzzle_grid)
        for i in xrange(9):
            for j in xrange(9):
                if new_grid[i][j] == 0:
                    new_grid[i][j] = [x for x in xrange(1,10)]
        return new_grid

    #removes any lists from the board and replaces them with a zero
    #creates a grid with no lists in it for display on a grid
    def remove_lists(self, puzzle_grid):
        self.assert_grid(puzzle_grid)
        new_grid = copy.deepcopy(puzzle_grid)
        for i in xrange(9):
            for j in xrange(9):
                if type(new_grid[i][j]) == type([]):
                    new_grid[i][j] = 0
        return new_grid

class CycleManipulations(BoardManipulations):
    '''this class allows each technique to be applied to the grid
    across its rows, cols and squares'''

    #cycles through any true/false type function
    def cycle_tf(self, puzzle_grid, function):
        new_grid = copy.deepcopy(puzzle_grid)
        if function(new_grid):
            new_grid = self.make_rows(new_grid)
            if function(new_grid):
                new_grid = self.make_rows(new_grid)
                new_grid = self.make_squares(new_grid)
                if function(new_grid):
                    return True
        return False

    #cycles through any manipulation type function
    def cycle_technique(self, puzzle_grid, function):
        new_grid = copy.deepcopy(puzzle_grid)
        new_grid = function(new_grid)
        new_grid = self.make_rows(new_grid)
        new_grid = function(new_grid)
        new_grid = self.make_rows(new_grid)
        new_grid = self.make_squares(new_grid)
        new_grid = function(new_grid)
        new_grid = self.make_squares(new_grid)
        return new_grid


class BoardStatus(BoardManipulations, CycleManipulations):
    '''Checks status of the board.  Checks for valid and finished boards'''

    #check to see if board is a valid sudolu board
    def check_valid_grid(self, puzzle_grid):
        self.assert_grid(puzzle_grid)
        if self.check_minimum(puzzle_grid):    #check to see if there are at least 17 knowns
            if self.cycle_tf(puzzle_grid, self.check_numbers):  #check to see if there are any repeated numbers
                if self.check_blank_lists(puzzle_grid):         #check to see if there are any blank lists, helpful for debugging
                    return True
        return False

    #make sure there are at least 17 knowns which is the least number
    #of knowns you can have and still have a solvable puzzle
    def check_minimum(self, puzzle_grid):
        self.assert_grid(puzzle_grid)
        count = 0
        for i in xrange(9):
            for j in xrange(9):     #check to see is cell contains an int that is not a zero
                if type(puzzle_grid[i][j]) == type(int()) and puzzle_grid[i][j] <> 0:
                    count += 1
        if count < 17: return False
        else: return True

    #make sure that there are no reapeated number in each row
    def check_numbers(self, puzzle_grid):
        self.assert_grid(puzzle_grid)
        for row in puzzle_grid:             #for each row count the number
            for number in xrange(1,10):     #of times each number is contained
                if row.count(number) > 1:   #if more than one the grid is not valid
                    return False
        return True

    def check_blank_lists(self, puzzle_grid):
        for row in puzzle_grid:             #if the cell contains a list that has a length
            for col in row:                 #of zero the solve made an error and removed a possibility
                if type(col) == type([]) and len(col) == 0:
                    return False
        return True

    #check to see that a board is complete and valid
    def check_done(self, puzzle_grid):
        count = 0
        for row in puzzle_grid:
            for col in row:                     #check to see that each cell contains an int
                if type(col) == type(int()) and col <> 0:
                    count += 1
        if count <> 81: return False                        #and that the puzzle is valid if so
        else: return self.check_valid_grid(puzzle_grid)     #the puzzle has been solved


class SudokuTechniques(CycleManipulations):

    #check if the lenght of a unknown is exactly one and make it a known
    def remove_single_lists(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)       #if a list contains only one element then we
        for i in xrange(9):                         #know that is the value if the cell
            for j in xrange(9):
                if type(new_grid[i][j]) == type([]):
                    if len(new_grid[i][j]) == 1:
                        new_grid[i][j] = new_grid[i][j][0]
        return new_grid

    #check to see if a number is known because it occurs only once
    def remove_lonely(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)
        for i in xrange(9):
            numbers = []    #create a empty list for a total count of numbers
            list_of_lists = [x for x in new_grid[i] if type(x) == type([])]   #create a list of all of the unknown lists
            for list in list_of_lists:  #break the lists down and append the numbers list with all of the numbers
                for number in list:     #in each of the lists
                    numbers.append(number)
            for j in xrange(9):
                if type(new_grid[i][j]) == type(int()):   #append the numbers list with all of the known numbers
                    numbers.append(new_grid[i][j])
            remove = []         #create an empty list for numbers that will be knowns
            for j in xrange(1,10):
                if numbers.count(j) == 1:   #if the number occers only once in the grid append the remove list
                    remove.append(j)
            for number in remove:   #the numbers in the remove list are now knowns
                for j in xrange(9): #and can be placed as knowns in the board
                    if type(new_grid[i][j]) == type([]):  #find the unknown list that contains the known number
                        if number in new_grid[i][j]:      #set the unknown list to a known number
                            new_grid[i][j] = number
        return new_grid

    #cycle through the puzzle and remove lonely
    def remove_lonely_whole_puzzle(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)
        new_grid = self.cycle_technique(new_grid, self.remove_lonely)
        return new_grid

    #remove unkowns for the lists by using knowns within each row
    def remove_numbers(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)
        for row in new_grid:
            found = []      #create an empty list for known numbers
            for col in row:
                if type(col) == type(int()):
                    found.append(col)      #append the known list with known numbers
            for number in found:    #for each known remove the known from each
                for col in row:     #list of unknowns
                    if type(col) == type([]):
                        if number in col:
                            col.remove(number)
        new_grid = self.remove_single_lists(new_grid)  #check to see if unknowns are now known
        new_grid = self.remove_lonely(new_grid)        #check to see all of the unkowns contain exactly one number
        return new_grid

    #cycle through the puzzle and remove numbers that are known
    def remove_number_whole_puzzle(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)
        new_grid = self.cycle_technique(new_grid, self.remove_numbers)
        return new_grid


    #look for sets of pairs, triplets, and quads and take those sets out of other unknown lists
    def remove_sets(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)
        for k in xrange(2,5):
            for i in xrange(9):
                found = []
                for j in xrange(9):
                    #if the unkown is of length k and has a k-1 matches it is a set and can be added to the found list
                    if type(new_grid[i][j]) == type([]) and len(new_grid[i][j]) == k and \
                                new_grid[i].count(new_grid[i][j]) == k and new_grid[i][j] not in found:
                        found.append(new_grid[i][j])
                #for the sets found the members of the set can be removed from any other list of unkowns
                for list in found:
                    for number in list:
                        for j in xrange(9):
                            #if the unkown list is not member of the set but, contains a member of the set can be
                            #removed from that list
                            if type(new_grid[i][j]) == type([]) and new_grid[i][j] <> list and \
                                        number in new_grid[i][j]:
                                new_grid[i][j].remove(number)
        return new_grid

    #cycle through the grid and remove sets
    def remove_sets_whole_puzzle(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)
        new_grid = self.cycle_technique(new_grid, self.remove_sets)
        return new_grid


    #Look for the hidden pairs of a board.  A hidden pair is a set of pairs who have other unknowns making
    #the fact that they are actually a member of a pair
    def remove_hidden_pairs(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)
        for i in xrange(9):
            count = {}  #create a dictionary that will keep count of occurances of unkowns
            for j in xrange(9):
                if type(new_grid[i][j]) == type([]):  #find a list of unknown
                    for number in xrange(1,10):     #cycle through number 1-9
                        if number in new_grid[i][j]:  #if a number is found add it to the count of that number
                            if number not in count:
                                count[number] = [0,[]]
                            count[number][0] = count[number][0] + 1 #add to the count
                            count[number][1].append(j)              #add the location of the number
            for key1 in count:      #cycle through the dictionary for key1
                for key2 in count:  #cycle through the dictionary for key2
                    #if key1 and key 2 are different,both have a count of 2 and 
                    #share the same locations they are a hidden pair
                    if key1 <> key2 and count[key1] == count[key2] and count[key1][0] == 2:
                        #set the new value of the unkown to the values of key1 and key2
                        for col in count[key1][1]:
                            new_grid[i][col] = [key1, key2]
            #sort the unkowns so that the are in numeric order
            for j in xrange(9):
                if type(new_grid[i][j]) == type([]):
                    new_grid[i][j].sort()
        return new_grid

    #cycle through the puzzle and find the hidden pairs
    def remove_hidden_pairs_whole_puzzle(self, puzzle_grid):
        new_grid = copy.deepcopy(puzzle_grid)
        new_grid = self.cycle_technique(new_grid, self.remove_hidden_pairs)
        return new_grid


class SudokuSolver(BoardManipulations, BoardStatus, SudokuTechniques):
    '''This class contains the functions that solve puzzles of varying degrees of difficulty'''

    #level one only applies the removing of numbers based on know cells
    def level_one(self, puzzle_grid):
        new_grid = []
        old_grid = copy.deepcopy(puzzle_grid)       #create a reference point to see if progress
        k = 0                                       #is being made, create a counter to make sure
        while new_grid <> old_grid and k < 500:     #no infinites loops are created
            k += 1
            new_grid = self.remove_number_whole_puzzle(old_grid)    #try to solve the grid
            if new_grid <> old_grid:                                #if the grid has improved
                old_grid = copy.deepcopy(new_grid)                  #set the improved grid to the old
                new_grid = []                                       #grid and try to imporve again
        return new_grid                                             #if no further improvements are made return grid

    #level two apllies finding sets to the solver
    def level_two(self, puzzle_grid):
        new_grid = []
        old_grid = copy.deepcopy(puzzle_grid)
        k = 0 
        while new_grid <> old_grid and k < 500:
            k += 1
            new_grid = self.remove_sets_whole_puzzle(old_grid)
            new_grid = self.level_one(new_grid)
            if new_grid <> old_grid:
                old_grid = copy.deepcopy(new_grid)
                new_grid = []
        return new_grid

    #level three applies finding hidden pairs to the solver
    def level_three(self, puzzle_grid):
        new_grid = []
        old_grid = copy.deepcopy(puzzle_grid)
        k = 0 
        while new_grid <> old_grid and k < 500:
            k += 1
            new_grid = self.remove_hidden_pairs_whole_puzzle(old_grid)
            new_grid = self.level_two(new_grid)
            if new_grid <> old_grid:
                old_grid = copy.deepcopy(new_grid)
                new_grid = []
        return new_grid

    #brute force cycles through each cell and each possibility
    #then puts that puzzle back into the solver, misses some solutions
    def brute_force(self, puzzle_grid):
        solutions = []
        if self.check_done(puzzle_grid):
            if puzzle_grid not in solutions:
                solutions.append(puzzle_grid)
                print 'hi'
                return
        new_grid = copy.deepcopy(puzzle_grid)
        for i in xrange(9):
            for j in xrange(9):
                if type(new_grid[i][j]) == type([]):
                    for number in new_grid[i][j]:
                        newer_grid = copy.deepcopy(new_grid)
                        newer_grid[i][j] = number
                        solution = self.level_three(newer_grid)
                        if self.check_done(solution):
                            if solution not in solutions:
                                solutions.append(solution)
        return solutions

    #still working on a better brute force method
    def brute_force2(self, puzzle_grid):
        solutions = []
        new_grid = copy.deepcopy(puzzle_grid)
        for i in xrange(9):
            for j in xrange(9):
                if type(new_grid[i][j]) == type([]):
                    for number in new_grid[i][j]:
                        newer_grid = copy.deepcopy(new_grid)
                        newer_grid[i][j] = number
                        solution = self.level_three(newer_grid)
                        if self.check_done(solution):
                            if solution not in solutions:
                                solutions.append(solution)
        return solutions

class BoardMutations(BoardManipulations):
    'this class mutates valid grid to create new valid grids'

    def __init__(self, m=10, n=1):
        #start with a valid grid
        self.grid = [[1,7,4,2,8,5,3,9,6],
                     [3,9,6,4,1,7,5,2,8],
                     [8,5,2,9,6,3,1,7,4],
                     [4,1,7,5,2,8,6,3,9],
                     [6,3,9,7,4,1,8,5,2],
                     [2,8,5,3,9,6,4,1,7],
                     [7,4,1,8,5,2,9,6,3],
                     [9,6,3,1,7,4,2,8,5],
                     [5,2,8,6,3,9,7,4,1]]
        self.n = n
        self.m = m
        self.make_valid_grid()

    #create a new valid grid by switching rows in a group
    def switch_rows(self):
        for i in xrange(self.n):
            group = random.randint(0,2)
            one = random.randint(0,2)
            two = random.randint(0,2)
            while one == two:
                two = random.randint(0,2)
            col1 = group*3 + one
            col2 = group*3 + two
            self.grid[col1],self.grid[col2] = self.grid[col2],self.grid[col1]

    #create a new valid grid by switch the places of two numbers in
    #each of the rows
    def switch_numbers(self):
        for k in xrange(self.n):
            n1 = random.randint(1,9)                #select two random numbers
            n2 = random.randint(1,9)
            while n1 == n2:                         #make sure they are different
                n2 = random.randint(1,9)
            for i in xrange(9):
                for j in xrange(9):
                    if self.grid[i][j] == n1:       #swap the locations of the numbers
                        self.grid[i][j] = n2
                    elif self.grid[i][j] == n2:
                        self.grid[i][j] = n1

    #apply switch numbers and switch rows to create a new valid grid
    #for creating new puzzles
    def make_valid_grid(self):
        for i in xrange(self.m):
            self.switch_rows()          #switch rows
            self.make_rows(self.grid)   #switch rows and cols
            self.switch_rows()          #switch rows
            self.switch_numbers()       #switch numbers

class Sudoku:
    '''this class solves a puzzle'''    

    def solve_sudoku(self, puzzle, use_brute_force = False):
        '''Enter a puzzle that is either a list of lists or a string
    place zeros where unknown cells are located'''
        start = time.time()                         #set a starting time to measure performance                        
        self.level = 0                              #set initial values to variables
        self.multiple_solutions = False
        self.solution = False
        self.solution_string = False
        self.solution_time = 0
        self.solved = False
        self.valid = False
        sudoku = SudokuSolver()                     #instantiate the solver class
        if type(puzzle) == type(str()):             #check to see if the puzzle is a list or string type
            self.puzzle_string = puzzle             #set values of the puzzle grid and puzzle string
            self.puzzle_grid = sudoku.convert_string_to_grid(puzzle)
        else:
            self.puzzle_grid = puzzle   
            self.puzzle_string = sudoku.convert_grid_to_string(puzzle)    
        self.valid = sudoku.check_valid_grid(self.puzzle_grid)      #make sure the puzzle is valid
        if not self.valid:                                          #if not valid return no solution
            return
        self.solution = copy.deepcopy(self.puzzle_grid)             #create a reference point
        self.solution = sudoku.place_lists(self.solution)           #place the possible lists on the grid

        #apply level one
        self.solution = sudoku.level_one(self.solution)             #apply the level one techniques
        self.solved = sudoku.check_done(self.solution)              #if solved set the rest of the varibles
        if self.solved:                                             #and return
            self.solution_time = time.time() - start
            self.level = 1
            self.solution_string = sudoku.convert_grid_to_string(self.solution)
            return self.solution

        #apply level two
        self.solution = sudoku.level_two(self.solution)             #if not apply the level two techniques
        self.solved = sudoku.check_done(self.solution)              #check to see if the puzzle is solved
        if self.solved:                                             #if solved set the rest of the variables
            self.solution_time = time.time() - start                #and return
            self.level = 2
            self.solution_string = sudoku.convert_grid_to_string(self.solution)
            return self.solution

        #apply level three
        self.solution = sudoku.level_three(self.solution)           #if not apply the level three techniques
        self.solved = sudoku.check_done(self.solution)              #check to see if the puzzle is solved
        if self.solved:                                             #if solved set the rest of the variables
            self.solution_time = time.time() - start                #and return
            self.level = 3
            self.solution_string = sudoku.convert_grid_to_string(self.solution)
            return self.solution

        #if using brute force apply brute force
        if use_brute_force:
            solutions = sudoku.brute_force(self.solution)           #brute force returns a list of solutions
            if len(solutions) == 1:                                 #if one solution is found set solution
                self.solution = solution[0]                         #to the first value of the list
                self.solution_string =sudoku.convert_grid_to_string(self.solution)  #and return
                self.solution_time = time.time() - start
                self.level = 10
                self.solved = True
                return
            elif len(solutions) > 1:                                #if multiple solutions
                self.solution = solutions                           #set solution to the list
                self.solution_string = ''                           #set the solution string to empty string
                self.solution_time = time.time() - start
                self.level = 11
                self.solved = True
                self.multiple_solutions = True                      #set multiple solutions to True
                return
            else:
                self.solution = []                                  #if not solutions were found
                self.solution_string = ''                           #return the empty list and empty string
                self.solution_time = time.time() - start
                self.level = 100

class SudokuMaker:
    def __init__(self):
        self.make_sudoku()

    def make_sudoku(self):       
        manipulate = BoardManipulations()                           #instantiate an intance of BoardManipulations
        validate = BoardStatus()                                    #BoardStatus
        solver = Sudoku()                                           #Sudoku
        self.solution = BoardMutations().grid                       #create a unique solution grid
        grid = copy.deepcopy(self.solution)                         #create a refernce point
        self.solution_string = manipulate.convert_grid_to_string(self.solution) #make the make the solution string
        numbers = [x for x in xrange(1,10)]                         #create a list of numbers 1-9
        random.shuffle(numbers)                                     #shuffle the numbers
        locations = {}                                              #create empty dict that will contain the locations
        for number in numbers:                                      #of numbers on the grid by thier coordinates
            locations[number] = []                                  #add number to the dict as a key
        for i in xrange(9):
            for j in xrange(9):
                locations[grid[i][j]].append([i,j])                 #append the location on the number to the list
        for number in numbers:
            random.shuffle(locations[number])                       #shuffle the locations of the number around
            for location in locations[number]:                      #for each location of then number on the grid
                new_grid = copy.deepcopy(grid)                      #create a new copy of the grid
                new_grid[location[0]][location[1]] = 0              #change the value of the cell to zero
                solver.solve_sudoku(new_grid)                       #try to solve the new grid
                if solver.solved:                                   #if it can be solved
                    grid = copy.deepcopy(new_grid)                  #set the new puzzle to the value of the grid
                    self.level = solver.level                       #record the difficulty of the grid
                    self.puzzle = copy.deepcopy(grid)               #set the new puzzle to the value of the puzzle
                    self.puzzle_string = manipulate.convert_grid_to_string(grid)    #set the puzzle string
                else:
                    new_grid[location[0]][location[1]] = number     #if no solution can be found replace the number
                    grid = copy.deepcopy(new_grid)                  #and try again
        
class SamplePuzzles:
    'Sample puzzles to use with the solver'

    def __init__(self):
        self.easy_grid = [[0, 0, 0, 2, 0, 0, 0, 0, 9], 
                          [0, 0, 4, 0, 0, 0, 0, 0, 0], 
                          [0, 1, 0, 0, 0, 0, 3, 2, 0], 
                          [9, 0, 0, 7, 0, 8, 4, 0, 0], 
                          [4, 0, 0, 1, 0, 0, 0, 7, 5], 
                          [5, 8, 0, 0, 0, 4, 0, 0, 1], 
                          [0, 5, 0, 0, 0, 0, 1, 0, 0], 
                          [2, 0, 0, 0, 0, 9, 5, 0, 0], 
                          [0, 0, 0, 0, 0, 5, 0, 0, 0]]

        self.medium_grid = [[1, 0, 0, 0, 0, 0, 0, 2, 6], 
                            [0, 0, 0, 0, 0, 0, 1, 0, 0], 
                            [4, 0, 0, 7, 0, 0, 9, 0, 0], 
                            [0, 0, 9, 0, 0, 6, 0, 1, 0], 
                            [0, 0, 3, 9, 0, 0, 6, 0, 0], 
                            [0, 0, 2, 3, 7, 1, 0, 0, 0], 
                            [0, 5, 0, 6, 0, 2, 0, 7, 0], 
                            [0, 6, 0, 0, 0, 0, 5, 0, 9], 
                            [0, 0, 1, 0, 0, 5, 0, 0, 0]]

        self.hard_grid = [[0, 0, 2, 0, 0, 0, 0, 3, 0], 
                          [0, 3, 0, 0, 4, 0, 0, 8, 0], 
                          [0, 9, 0, 0, 0, 7, 0, 0, 0], 
                          [0, 0, 0, 5, 0, 4, 0, 0, 0], 
                          [8, 0, 0, 0, 3, 0, 0, 4, 0], 
                          [2, 0, 0, 0, 8, 0, 0, 7, 3], 
                          [0, 0, 0, 0, 0, 0, 5, 0, 0], 
                          [0, 0, 4, 1, 0, 0, 0, 0, 0], 
                          [0, 0, 7, 4, 5, 2, 8, 1, 0]]

        self.easy_string = '509304002200900060064020000000000000003000905010000300020005000000012090900030700'
        self.medium_string = '280060004076500038000000067000040000800007000090003000007009300000000049005800070'
        self.hard_string = '600001507405000080000007002000000050000062100008050090090800000010070000050090000'