import os
import time
# this class is used to set up the methods for each individual cell that will be used in the grid
class Cell:
  def __init__(self):
    self.sym = " "
  def __str__(self):
    return self.sym
  def value(self):
    return self.sym
  def move(self, sym):
    self.sym = sym
  def isBlank(self):
    return self.sym == " "
  def isSet(self,sym):
    return self.sym == sym

# this is the grid class    
class Grid:
  def __init__(self):
    # the grid class defines a sizexsize grid
    # there is a list of tokens that can be placed and the starting symbol is pos 0 of this list
    # winning symbol is set if there is a win
    # the sqs is the numbers of empty grid spaces left - this is used for a draw
    self.size = 3
    self.syms = ["x","o"]
    self.next = 0
    self.winSym = ""
    self.cells = [[Cell() for c in range(self.size)] for r in range(self.size)]
    self.sqs = [r*3+c+1 for r in range(self.size) for c in range(self.size) if self.cells[r][c].isBlank()]
  def inSqs(self,n):
    return n in self.sqs
  def moves(self):
    # this prints the available moves in the format   1|2|3
    #                                                 -----
    #                                                 4|5|6
    #                                                 -----
    #                                                 7|8|9
    # where the numbers are replaced with space if the cell is not blank
    nl = "\n-----\n"
    return (nl.join(['|'.join([str(r*3+c+1) if self.cells[r][c].isBlank() else " " for c in range(self.size)]) for r in range(self.size)])+"\n")
  def out(self):
    # this prints the grid out as in the format   1|2|3
    #                                             -----
    #                                             4|5|6
    #                                             -----
    #                                             7|8|9
    # where the numbers are replaced with either
    # x, o or space   
    print("Your grid looks currently like this: \n")
    nl = "\n-----\n"
    return (nl.join(['|'.join([self.cells[r][c].sym for c in range(self.size)]) for r in range(self.size)])+"\n")
  def checkRow(self, r):
    # this checks if the first cell in the row is equal to the second cell and the second cell is equal to the third by changing 
    # the column number from 0 - 1
    return [True,True] == ([self.cells[r][c].sym == self.cells[r][c+1].sym for c in range(self.size-1)])
  def checkCol(self, c):
    # this checks if the first cell in the col is equal to the second cell and the second cell is equal to the third by changing
    # the row number from 0 - 1
    return [True,True] == ([self.cells[r][c].sym == self.cells[r+1][c].sym for r in range(self.size-1)])
  def checklDiag(self):
    # this checks if the cells in the diagonal where row = col (so 0,0 = 1,1 and 1,1 = 2,2) by changing the row & column number
    # from 0 - 1
    return [True,True] ==  ([self.cells[x][x].sym == self.cells[x+1][x+1].sym for x in range(self.size-1)])
  def checkrDiag(self):
    # this checks if the cells in the diagonal where 2 = row + col (so 0,2 = 1,1 and 1,1 = 2,0) by changing the row from 0 = 1
    # and calculating the column number by subtracting the row from 2
    return [True,True] == ([self.cells[x][2-x].sym == self.cells[x+1][2-(x+1)].sym for x in range(self.size-1)])
  def checkWin(self):
    # this returns true if the winSym has been set to x or o - used for the 4 win conditions
    if self.winSym in self.syms:
      return True
    else:
      return False
  def draw(self):
    # this counts the number of grid spaces in the grid & returns true if there are no spaces left
    return len(self.sqs) == 0
  def rowWin(self):
    # this checks each row in the grid and returns true if any of them contain 3 identical non-blank characters
    for r in range(self.size):
      if not(self.cells[r][0].isBlank()) and (self.checkRow(r)):
        self.winSym = self.cells[r][0].sym
        r = self.size
    return self.checkWin()  
  def colWin(self):
    # this checks each column in the grid and returns true if any of them contain 3 identical non-blank characters
    for c in range(self.size):
      if not(self.cells[0][c].isBlank()) and (self.checkCol(c)):
        self.winSym = self.cells[0][c].sym
        c = self.size
    return self.checkWin()
  def rWin(self):
    # this checks each cell in the 0,0; 1,1; 2,2 diagonal and returns true if it contains 3 identical non-blank characters
    if not(self.cells[1][1].isBlank()) and (self.checkrDiag()):
        self.winSym = self.cells[1][1].sym
    return self.checkWin()
  def lWin(self):
    # this checks each cell in the 0,2; 1,1; 2,0 diagonal and returns true if it contains 3 identical non-blank characters
    if not(self.cells[1][1].isBlank()) and (self.checklDiag()):
        self.winSym = self.cells[1][1].sym
    return self.checkWin()
  def gameOver(self):
    # this is the game over check which will return true for a draw or 3 in a row
    return self.rowWin() or self.colWin() or self.rWin() or self.lWin() or self.draw()
  def move(self,r,c):
    # this places the next symbol in the grid square selected r = row, c = col
    # toggles the next available symbol by adding one and getting the remainder when divided by 2 (is it even!)
    # and prints out the grid
    os.system('clear')
    self.cells[r][c].move(self.syms[self.next])
    self.sqs = [r*3+c+1 for r in range(self.size) for c in range(self.size) if self.cells[r][c].isBlank()]
    self.next = (self.next+1)%2
    #print("Your grid looks currently like this: \n")
    print(self.out())
    if not(self.gameOver()):
      print("Available moves are: \n")
    else:
      if grid.winSym in grid.syms:
        print(f"{grid.winSym} won that game!\n")
      else:
        print("That was a draw!\n")

def getRC(n):
  return (n-1)//3,(n-1)%3
  
def pickSquare():
  sqValid = False
  while not(sqValid):
    print(grid.moves())
    try:
      n = int(input("Pick a square: "))
      if not(grid.inSqs(n)):
        print("That is not an available move")
        time.sleep(2)
        raise Exception ("Move error")
    except:
      os.system("clear")
      print(grid.out())
      print("Try again! \n")
    else:
      sqValid = True
      return getRC(n)

def instructions():
  print("Welcome to MrYoungCS' version of TicTacToe\n")
  print(grid.out())
  print("Available moves are: \n")
  
endGame = True
while endGame:
  os.system("clear")
  grid = Grid()
  instructions()
  while not(grid.gameOver()):
    r,c = pickSquare()
    grid.move(r,c)
  endGame = input("Would you like to play again? (y/n) ").lower() == "y"
