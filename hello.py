import numpy as np


board = np.zeros((3,3),dtype=int)  # Initialize a 3x3 board with zeros
print(board)

def print_board(b):
  symbols = {0: ' ', 1: 'X', -1: 'O'}
  for r in range(3):
    row= " | ".join(symbols[val] for val in b[r])
    print(" "+row)
    if r < 2:
      print("---+---+---")
  print()
def check_winner(b):
  if 3 in np.sum(b,axis=1) or 3 in np.sum(b,axis=0):
    return "X wins"
  if -3 in np.sum(b,axis=1) or -3 in np.sum(b,axis=0):
    return "O wins"
  if  np.trace(b)==3 or np.trace(np.fliplr(b))==3:
    return "X wins"
  if np.trace(b)==-3 or np.trace(np.fliplr(b))==-3:
    return "O wins"
  if not 0 in b:
    return "Draw"
  return None


current = 1
print("Welcome to Tic Tac Toe!")
 


while True:
  if current == 1:
     player = 'X'
  else:
    player = 'O'


  try:
    row = int(input(player + "- Enter the row (0,1,2)" ))
    col = int(input(player + "- Enter the column (0,1,2)" ))
  except ValueError:
    print("please enter valid integers for row and column.\n")
    continue
  if row<0 or row>2 or col<0 or col>2:
    print("Row and column must be between 0 and 2.\n")
    

  if board[row,col] !=0:
    print("Cell already taken. Choose another one.\n")
    

  board[row,col] = current
  print_board(board)

  result = check_winner(board)

  if result is not None:
    if result == "Draw":
      print("The game is a draw!")
    else:
      print(result)

    break
  if current == 1:
    current = -1
  else: 
    current = 1
