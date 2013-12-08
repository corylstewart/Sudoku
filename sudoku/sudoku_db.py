import random

from google.appengine.ext import ndb

#create the Sudoku Puzzle class for the database
class Sudoku(ndb.Model):
    grid = ndb.StringProperty()
    solution = ndb.StringProperty()
    level = ndb.IntegerProperty()
    user = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now = True)

    #return a random puzzle of a certain level from the DB
    def get_puzzle(self, level):
        puzzles = Sudoku.query(Sudoku.level == level)
        puzzle = random.randint(1,puzzles.count())
        i = 0
        for p in puzzles:
            i+=1
            if i == puzzle:
                return p
    
    #put a new puzzle in the database
    def put_puzzle(self, grid, solution, level, user):
        exists = Sudoku.query(Sudoku.grid == grid)
        if exists.count() == 0:
            sudoku = Sudoku(grid = grid,
                            solution = solution,
                            level = level,
                            user = user)
            sudoku.put()

    #delete random puzzles from the database
    def delete_sudoku_db(self, limit = 500):
        to_delete = Sudoku.query().fetch(limit = limit)
        for puzzle in to_delete:
            puzzle.key.delete()

#read puzzle from a file and place them im the DB
class SudokuFile:
    def put_file_in_db(self, filename = 'sudoku.txt'):
        user = 'base'
        f = open(filename, 'r')
        for line in f:
            puzzle = line.split()
            solution = puzzle[0]
            grid = puzzle[1]
            level = int(puzzle[2])
            add_to_db = Sudoku().put_puzzle(grid, solution, level, user)


'''#create a grid string that reporesents a grid
def make_grid_string(grid):
    string = ''
    for i in xrange(len(grid)):
        for j in range(len(grid[i])):
            string += str(grid[i][j])
    return string

#create a grid that represents a grid string
def unmake_grid_string(string):
    grid = []
    for i in xrange(9):
        grid.append([])
        for j in xrange(9):
            n = int(string[:1])
            grid[i].append(n)
            string = string[1:]
    return grid'''

    
