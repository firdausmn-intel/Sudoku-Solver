import tkinter as tk
from PIL import Image, ImageTk
import random
import time
import nbimporter 
from SudokuBackend import SudokuSolver,CreateSudoku,ValidateSudoku,SudokuDifficulty,board_quest

root=tk.Tk()
root.title("Sudoku Solver")
root.geometry("390x560")
root.configure(bg="white")
label = tk.Label(root, text="Fill in the numbers and click solve",bg="white")
label.grid(row=0,column=1,columnspan=10)

errLabel = tk.Label(root, text="",fg="red",bg="white")
errLabel.grid(row=15,column=5,rowspan=2,columnspan=10)

solvedLabel = tk.Label(root, text="",fg="green",bg="white")
solvedLabel.grid(row=16,column=5,columnspan=10)

hintLabel = tk.Label(root, text="",fg="blue",bg="white")
hintLabel.grid(row=15,column=1,columnspan=5)

TimerLabel = tk.Label(root, text="Time: 00:00:00",bg="white")
TimerLabel.grid(row=16,column=1,columnspan=5,pady=10)


cells={} # A dictionary to store the current state of each cell in the Sudoku grid.
initial_state={} # A dictionary to keep track of the initial values of the cells when the puzzle is first loaded or generated.
undo_stack=[] # A list that functions as a stack to keep track of user actions for the undo feature.
difficulty_level=None #Initiating difficulty level


# Variables to keep track of the timer
start_time = None # A variable to store the starting time when the timer is activated.
timer_running = False # A boolean flag to indicate whether the timer is currently running.


def solve_gui():
    board=getValues() # Retrieves the current values
    sudoku_solver=SudokuSolver(board) # Initializes a SudokuSolver object
    sudoku_validate=ValidateSudoku(board) # Validates the initial Sudoku
    if sudoku_validate.validate():
        if sudoku_solver.solve():
            stop_timer()
            update_gui(sudoku_solver.board)
            solvedLabel.configure(text="Sudoku has been completed")
    else:
        errLabel.configure(text="No solution")

# Fill in the board with solutions
def update_gui(board):
    for i in range(len(board)):
        for j in range (len(board[i])):
            cell = cells[(i+2,j+1)]
            cell.delete(0,"end")
            cell.insert(0,str(board[i][j]))

def clearValues():
    global undo_stack
    undo_stack.clear()
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2,11):
        for col in range(1,10):
            cell=cells[(row,col)]
            if cell.get() != initial_state[(row, col)]:  # Check if the cell was modified by the user
                cell.delete(0,'end')
                cell.config(fg="blue")
                cell.config(validate="key", validatecommand=(reg, "%P", str(row), str(col))) # Run ValidateNumber function after clear


def newgame():
    errLabel.config(text="")
    solvedLabel.config(text="")
    hintLabel.config(text="")
    stop_timer()
    button_enabled()
    draw9x9Grid()
    enable_all_cells()
    for cell in cells.values():
        cell.config(fg="black")
        cell.delete(0,'end')
    board_q=board_quest()
    sudoku_create=CreateSudoku(board_q,difficulty_level)
    board=sudoku_create.board_create()
    if board:
        populateGridWithBoard(board)    
    else:
        errLabel.config(text="Sudoku is invalid!")
        button_disabled()
        readonly_all_cells()
        buttons=[btn_newgame, btneasy, btnmedium, btnhard]
        for button in buttons:
            button.config(state='disabled')

def undo():
    if undo_stack:
        row, col, previous_value, previous_color = undo_stack.pop()
        cell = cells[(row, col)]
        cell.delete(0, 'end')
        if previous_value: 
            cell.insert(0, previous_value) # If there was a previous value, insert it back
            cell.config(fg=previous_color) # Restore the previous color

        # If the cell is part of the initial puzzle, make it read-only again
        if initial_state.get((row, col)) != "":
            cell.config(state='readonly')
        else:
            cell.config(state='normal')
        cell.config(validate="key", validatecommand=(reg, "%P", str(row), str(col)))



def hint():
    board = getValues()  # Retrieves the current values
    sudoku_solver = SudokuSolver(board)  # Initializes a SudokuSolver object
    sudoku_validate = ValidateSudoku(board)  # Validates the initial Sudoku
    if sudoku_validate.validate():
        empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
        if empty_cells:  # Check if there are any empty cells left
            sudoku_solver.solve()
            row, col = random.choice(empty_cells)  # Choose a random empty cell
            hint_value = sudoku_solver.board[row][col]  # Get the value from the solved board
            cells[(row+2, col+1)].delete(0, 'end')  # Adjusting indices to match the grid layout
            cells[(row+2, col+1)].insert(0, str(hint_value))  # Insert the hint value
            cells[(row+2, col+1)].config(fg="blue")  # Optional: change the color to indicate a hint
            cells[(row+2, col+1)].config(state="readonly")  # Make the cell read-only
            max_hint()  # Update the hint count
            max_correct()  # Check if the puzzle is completed
    else:
        errLabel.configure(text="No solution")

def update_timer():
    if timer_running:
        # Calculate the elapsed time
        elapsed_time = time.time() - start_time
        # Convert the elapsed time into hours, minutes, and seconds
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Update the timer label
        TimerLabel.config(text="Time: {:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)))
        # Schedule the update_timer function to be called after 1000ms (1 second)
        root.after(1000, update_timer)

def start_timer():
    global start_time, timer_running
    if not timer_running:
        # Record the start time and set the timer to running
        start_time = time.time()
        timer_running = True
        update_timer()

def stop_timer():
    global timer_running
    timer_running = False

def draw3x3Grid(row, column, bgcolor):
    for i in range(3):
        for j in range(3):
            grid_row = row + i + 1
            grid_col = column + j + 1
            sv=tk.StringVar()

            e = tk.Entry(root, width=5, bg=bgcolor, justify='center',
                      validate="key", validatecommand=(reg, "%P", str(grid_row), str(grid_col)))
            e.grid(row=grid_row, column=grid_col, sticky="nsew", padx=1, pady=1, ipady=5) #users can enter their answer
            e.bind('<Key>', lambda event, r=grid_row, c=grid_col: key_pressed(event,r,c)) #trigger key_pressed function anytime a key in keyboard is pressed inside the box
            cells[(grid_row, grid_col)] = e
            
def draw9x9Grid():
    color="#D0ffff"
    for rowNo in range(1,10,3):
        for colNo in range(0,9,3):            
            draw3x3Grid(rowNo,colNo,color)
            if color =="#D0ffff": #light cyan color
                 color="#ffffd0" #light yellow color
            else:
                color="#D0ffff"

def ValidateNumber(P, row, col):
    row = int(row)  # Convert row to an integer
    col = int(col)  # Convert col to an integer
  
    # Adjust the row and col to match the board's indexing (0-based)
    board_row = row - 2
    board_col = col - 1
    # If the cell is cleared, reset the text color and allow the change
    if P == "":
        undo_stack.append((row, col, cells[(row, col)].get(), cells[((row, col))].cget('fg')))
        cells[((row, col))].delete(0,'end')
        cells[(row, col)].config(fg="black")
        return True
    
    # If the input is a single digit, check if it's valid
    if P.isdigit() and len(P) == 1:
        start_timer()
        num = int(P)
        undo_stack.append((row, col, cells[(row, col)].get(), cells[((row, col))].cget('fg')))
        # Temporarily set the cell to 0 to avoid conflict with itself during validation
        cells[(row, col)].delete(0, "end")
        cells[(row, col)].insert(0, "0")
        
        # Get the current state of the board
        board = getValues()
        sudoku_solver=SudokuSolver(board)
        # Restore the cell's value
        cells[(row, col)].delete(0, "end")
        cells[(row, col)].insert(0, P)
        
        # Check if the number is valid in the current board state
        if sudoku_solver.valid(num, (board_row, board_col)):
            cells[(row, col)].config(fg="green")
            max_correct()
            max_mistakes()
            max_hint()
            return True  # Allow the change
        else:
            cells[(row, col)].config(fg="red")
            max_mistakes()
            max_hint()
            return True
            
    else:
        # If the input is not a single digit, reject the change
        return False

reg=root.register(ValidateNumber)

def key_pressed(event,row,col):
    if event.keysym == "BackSpace" or "Delete":
        current_value=cells[(row,col)].get()
        current_color = cells[(row, col)].cget('fg') #get current color whether red or green
        # If the cell is about to be cleared, reset the text color and push to undo stack
        if len(current_value)==1:
            undo_stack.append((row,col,current_value,current_color))   
    cells[(row,col)].config(validate="key", validatecommand=(reg, "%P", str(row), str(col))) # Run ValidateNumber function after clear

def on_value_change(sv, row, col):
    value = sv.get()
    ValidateNumber(value, row, col)

def getValues():
    board=[]
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2,11):
        rows=[]
        for col in range(1,10):
            val = cells[(row,col)].get()
            if val=="":
                rows.append(0)
            else:
                rows.append(int(val))
        board.append(rows)
    return board

# Check how many valid numbers
def count_valid_numbers():
    count = 0
    for cell in cells.values():
        if cell.cget('fg') == 'green':
            count += 1
    return count

# Check how many invalid numbers
def count_invalid_numbers():
    count=0
    for cell in cells.values():
        if cell.cget('fg') == 'red':
            count += 1
    return count

# Check how many hint
def count_hint_numbers():
    count = 0
    for cell in cells.values():
        if cell.cget('fg') == 'blue':
            count += 1
    return count

def max_correct(): 
    # Update the valid number count if needed
    valid_count = count_valid_numbers()
    hint_count = count_hint_numbers()
    difficulty_new_level=difficulty_level-hint_count
    if valid_count==difficulty_new_level:
        solvedLabel.config(text="Congratulations! \nYou have completed the sudoku.")
        stop_timer()
        button_disabled()
        readonly_all_cells()

def max_mistakes(): 
     # Update the invalid number count if needed
    invalid_count = count_invalid_numbers()    
    if 0<invalid_count<3:
        errLabel.config(text=f"Mistakes: {invalid_count}")
    elif invalid_count>=3:
        errLabel.config(text=f"Oops! \nMax mistakes: {invalid_count}")
        readonly_all_cells()
        button_disabled()
        stop_timer()
    return invalid_count

def max_hint():
    hint_count=count_hint_numbers() # Get the current count of hints used
    hint_left=3-hint_count # Calculate the number of hints left
    if hint_count==3:
        hintLabel.config(text=f"You have used max hints: {hint_count}") # Update the hint label
        btnhint.config(state="disabled") # Disable the hint button
    else:
        hintLabel.config(text=f"Hints left: {hint_left}") # Update the hint label with hints left

# Button enabled
def button_enabled():
    buttons = [btnsolve,btnclear,btn_undo,btnhint]
    for button in buttons:
        button.config(state="normal")

# Button disabled
def button_disabled():
    buttons = [btnsolve,btnclear,btn_undo,btnhint]
    for button in buttons:
        button.config(state="disabled")

# Enable user to enter any number
def enable_all_cells():
    for cell in cells.values():
        cell.config(state='normal')
        
# Disable user from entering any number
def readonly_all_cells():
    for cell in cells.values():
        cell.config(state='readonly')

def populateGridWithBoard(board):
    global initial_state
    initial_state.clear()
    for i, row in enumerate(board):
        for j, num in enumerate(row):
            cell = cells[(i+2, j+1)]  # Adjusting indices to match the grid layout
            if num != 0:
                cell.insert(0, str(num))
                cell.config(fg="purple")
                cell.config(state='readonly') # Make the cell read-only
                
                initial_state[(i+2, j+1)] = str(num)  # Store the initial number
            else: 
                initial_state[(i+2,j+1)]=""

def easy():
    global difficulty_level
    difficulty_level=SudokuDifficulty.EASY()
    newgame()

def medium():
    global difficulty_level
    difficulty_level=SudokuDifficulty.MEDIUM()
    newgame()

def hard():
    global difficulty_level
    difficulty_level=SudokuDifficulty.HARD()
    newgame()

def expert():
    global difficulty_level
    difficulty_level=SudokuDifficulty.EXPERT()
    newgame()

# New game button
btn_newgame = tk.Button(root,command=newgame,text="New Game",fg='white',background='black')
btn_newgame.grid(row=1,column=1,columnspan=5,pady=20)

# Solve button
btnsolve=tk.Button(root,command=solve_gui,text="Solve",fg='white',background='black')
btnsolve.grid(row=1,column=5,columnspan=5,pady=20)

# Load the original image using Pillow
ori_image = Image.open("undo.png")
resize_image = ori_image.resize((30, 30), Image.Resampling.LANCZOS)
undo_image = ImageTk.PhotoImage(resize_image)

# Undo button
btn_undo = tk.Button(root, command=undo, image=undo_image,padx=0, pady=0, borderwidth=0,background='pink')
btn_undo.grid(row=17, column=1, columnspan=5)
btn_undo.image = undo_image

# Clear button
btnclear=tk.Button(root,command=clearValues,text="Clear",fg='white',background='#DC3545') # Bootstrap danger red
btnclear.grid(row=17,column=3,columnspan=5)

# Load the original image using Pillow
original_image = Image.open("bulb_icon.png")
resized_image = original_image.resize((30, 30), Image.Resampling.LANCZOS)
bulb_image = ImageTk.PhotoImage(resized_image)

# Hint button
btnhint = tk.Button(root, command=hint, image=bulb_image,padx=0, pady=0, borderwidth=0,background='deepskyblue')
btnhint.grid(row=17, column=5, columnspan=5)
btnhint.image = bulb_image

# Easy button
btneasy=tk.Button(root,command=easy,text="EASY",fg='white',background='deepskyblue')
btneasy.grid(row=18,column=0,columnspan=3,pady=10)

# Medium button
btnmedium=tk.Button(root,command=medium,text="MEDIUM",fg='white',background='dodgerblue')
btnmedium.grid(row=18,column=3,columnspan=3)

# Hard button
btnhard=tk.Button(root,command=hard,text="HARD",fg='white',background='royalblue')
btnhard.grid(row=18,column=6,columnspan=2)

# Expert button
btnexpert=tk.Button(root,command=expert,text="EXPERT",fg='white',background='navy')
btnexpert.grid(row=18,column=8,columnspan=3)

difficulty_level=5 # Set the difficulty level of the Sudoku game
newgame() # Initialize a new game with the set difficulty level
root.mainloop() # Start the Tkinter main event loop