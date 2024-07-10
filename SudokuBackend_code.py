def board_quest():   

    board_ques=[
    [7,8,0,4,3,0,0,2,0],
    [0,0,0,0,7,5,0,0,0],
    [0,9,3,0,0,1,0,0,8],
    [0,0,0,9,0,3,0,0,0],
    [2,6,0,0,0,8,0,0,4],
    [9,0,4,0,6,0,7,8,5],
    [0,0,0,0,0,0,6,0,0],
    [0,2,0,0,0,0,4,9,0],
    [3,0,9,0,1,0,8,0,0],
    ]
    return board_ques

import random

# (This cell contains the SudokuSolver class code)
class SudokuSolver:

    def __init__(self,board):
        self.board=board

     # Find an empty box in the sudoku
    def find_empty(self): 
        """  
        Used to find an empty box in the sudoku
          Parameters:
          i (int): Starting from 0 until 8 for row of the sudoku
          j (int): Starting from 0 until 8 for column of the sudoku

          Returns:
          int: i and j
          
          If no empty box left means sudoku is completed, 
          return None
          """
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]==0: #if box is empty
                    return(i,j)
                #if sudoku is completed
        return None
    
    #Check if number conflicts with row/column/box
    def valid(self, num, pos):
        """
        Check if the inserted number is conflicting with the row, column and 3x3 box
        Return True if no conflict
        Return False if conflict
        """
        #Check Row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i]==num and pos[1] !=i:#second condition is to not bother checking the box that we just add the number
                return False   
            
        for i in range(len(self.board)):#Check column
            if self.board[i][pos[1]] == num and pos[0] !=i: 
                 return False

        #Check box (3x3)
        box_i=pos[0]//3 #i 
        box_j=pos[1]//3 #j
        
        for i in range(box_i*3,box_i*3+3):
             for j in range(box_j*3,box_j*3+3):
                  if self.board[i][j] == num and (i,j) !=pos:
                       return False
        
        return True
    
    def solve(self):
        # Solve the sudoku using backtracking algorithm
        find = self.find_empty()
        if not find: #if sudoku is complete
            return True
        else:
             row, col = find
             for i in range(1,10):
                if self.valid(i, (row,col)):
                    self.board[row][col]=i
                    if not self.solve():
                        self.board[row][col]=0  #backtrack
                    else:
                         return True                          
        return False

class CreateSudoku:
    def __init__(self,board,REMOVE_CELLS_NO):
        self.board=board
        self.REMOVE_CELLS_NO=REMOVE_CELLS_NO

    # Create a new sudoku puzzle by removing cells from a solved board
    def board_create(self):  
        sudoku_validate=ValidateSudoku(self.board)
        
        sudoku_solver=SudokuSolver(self.board)
        if sudoku_validate.validate():
            if sudoku_solver.solve():
                 self.remove_cells(self.REMOVE_CELLS_NO)
                 return self.board        
        return False
        
    # Remove a specified number of cells from the board
    def remove_cells(self, num_cells_to_remove):
        # Get all possible cell coordinates and shuffle them
        cells = [(i, j) for i in range(9) for j in range(9)] 
        # Select the desired number from them 
        k=num_cells_to_remove
        for i, j in random.sample(cells,k):
            self.board[i][j] = 0

class ValidateSudoku:
    #to validate the sudoku prior to starting the game

    def __init__(self,board):
        self.board=board
        
    # Validate a row in the sudoku puzzle
    def is_valid_row(self,row):
        row_values = [self.board[row][col] for col in range(9) if self.board[row][col] != 0]
        return len(row_values) == len(set(row_values))

    # Validate a column in the sudoku puzzle
    def is_valid_col(self, col):
        col_values = [self.board[row][col] for row in range(9) if self.board[row][col] != 0]
        return len(col_values) == len(set(col_values))

    # Validate a 3x3 box in the sudoku puzzle
    def is_valid_box(self, box_row, box_col):
        box_values = []
        for row in range(box_row * 3, box_row * 3 + 3):
            for col in range(box_col * 3, box_col * 3 + 3):
                cell_value = self.board[row][col]
                if cell_value != 0:
                    box_values.append(cell_value)
        return len(box_values) == len(set(box_values))

    # Validate the entire sudoku puzzle
    def validate(self):
        for i in range(len(self.board[0])):
            if not self.is_valid_row(i):
                return False
            if not self.is_valid_col(i):
                return False
             
            for i in range(3):
                for j in range(3):
                    if not self.is_valid_box(i,j):
                        return False
        return True

class SudokuDifficulty:
    # Define class-level constants for difficulty levels
    
    @staticmethod
    def EASY():
        return 32
        
    @staticmethod
    def MEDIUM():
        return 42
        
    @staticmethod
    def HARD():
        return 50
    
    @staticmethod
    def EXPERT():
        return 61