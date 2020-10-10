import numpy as np
import os
import random


class Game2048:
  def __init__(self):

    print("wlecome to 2048! \n\n")
    print("to move the blocks to the right type d")
    print("to move the blocks to the left type a")
    print("to move the blocks up type w")
    print("to move the blocks down type s")
    print("to end the game type e")
    input("press enter key start ")
    print("\n \n ")

    self.gameArr = np.zeros((4,4))
    self.options = [2,2,2,2,2,4,2,2,2,2]

  def randomAdder(self):
    xDir = random.randint(0,3)
    yDir = random.randint(0,3)
    newNumber = random.choice(self.options)

    if self.gameArr[yDir,xDir] == 0:
      self.gameArr[yDir,xDir] = newNumber

    else:
      self.randomAdder()

  def columnToList(self, column):
    l1 = []

    for i in range (4):
      l1.append(self.gameArr[i,column])

    return l1

  def listToColumn(self,column, List):
    for i in range(4):
      self.gameArr[i,column] = List[i] 
    
  def combiner(self,direction):

    if direction == "right":
      for Y in range (4):
        for X in range (3,0,-1):
            if self.gameArr[Y,X] and self.gameArr[Y,X-1] == self.gameArr[Y,X]:
                self.gameArr[Y,X] += self.gameArr[Y,X-1]
                rowList = self.gameArr[Y]
                rowList = np.delete(self.gameArr[Y], X-1, 0)
                newRow = np.insert(rowList, 0, 0)
                self.gameArr[Y] = np.array(newRow)
    
    elif direction == "left":
      for Y in range (4):
        for X in range (3):
          if self.gameArr[Y,X] and self.gameArr[Y,X+1] == self.gameArr[Y,X]:
            self.gameArr[Y,X] += self.gameArr[Y,X+1]
            rowList = self.gameArr[Y]
            rowList = np.delete(self.gameArr[Y], X+1, 0)
            newRow = np.append(rowList, 0)
            self.gameArr[Y] = np.array(newRow)

    elif direction == "up":
      for X in range (4):
        for Y in range(3):
          if self.gameArr[Y,X] and self.gameArr[Y+1,X] == self.gameArr[Y,X]:
            self.gameArr[Y,X] += self.gameArr[Y+1,X]
            column = self.columnToList(X)
            del(column[Y+1])
            column.append(0)
            self.listToColumn(X,column)

    elif direction == "down":
      for X in range (4):
        for Y in range(3,0,-1):
          if self.gameArr[Y,X] and self.gameArr[Y-1,X] == self.gameArr[Y,X]:
            self.gameArr[Y,X] += self.gameArr[Y-1,X]
            columnList = self.columnToList(X)
            del(columnList[Y-1])
            newColumn = [0]
            newColumn.extend(columnList)
            self.listToColumn(X,newColumn)

  def moveRight(self):
    for Y in range(4):
      for _ in range(3):
        for X in range(3):
          if self.gameArr[Y,X+1] == 0:
            self.gameArr[Y,X+1] = self.gameArr[Y,X]
            self.gameArr[Y,X] = 0

  def moveLeft(self):
    for Y in range(4):
      for _ in range (3):
        for X in range(3,0,-1):
          if self.gameArr[Y,X-1] == 0:
            self.gameArr[Y,X-1] = self.gameArr[Y,X]
            self.gameArr[Y,X] = 0

  def moveUp(self):
    for X in range(4):
      for _ in range(3):
        for Y in range (3,0,-1):
          if self.gameArr[Y-1,X] == 0:
            self.gameArr[Y-1,X] = self.gameArr[Y,X]
            self.gameArr[Y,X] = 0

  def moveDown(self):
    for X in range(4):
      for _ in range(3):
        for Y in range(3):
          if self.gameArr[Y+1,X] == 0:
            self.gameArr[Y+1,X] = self.gameArr[Y,X]
            self.gameArr[Y,X] = 0

  def nextRound(self):
    diffList = []

    after = np.copy(self.gameArr)
    
    for Y in range(4):
      for X in range(4):
        diff = after[Y,X]-self.previous[Y,X]
        if diff != 0:
          diffList.append(1)
    
    if len(diffList) == 0:
      self.turns -= 1

    else:
      self.randomAdder()
      self.clear()
      print(self.gameArr)
    
  def clear(self):
    os.system( 'clear' )


  def play(self):
  
    self.randomAdder()
    self.randomAdder()
    self.turns = 0

    print(self.gameArr)

    while 2048 not in self.gameArr and 0 in self.gameArr:

      self.turns += 1

      self.previous = np.copy(self.gameArr)


      choice = input()
      if choice == "s":
        self.moveDown()
        self.combiner("down")

      elif choice == "w":
        self.moveUp()
        self.combiner("up")

      elif choice == "d":
        self.moveRight()
        self.combiner("right")

      elif choice == "a":
        self.moveLeft()
        self.combiner("left")
      
      elif choice == "e":
        self.turns -= 1
        break

      else:
        print("invalid choice")
        continue

      self.nextRound()



    print("the game is over")
    HS  = int(np.max(self.gameArr))
    print(f"you played {self.turns} turns with a highscore of {HS}")

    if 2048 in self.gameArr:
      print("YOU WON :), congratulations")

    elif 0 not in self.gameArr:
      print("you lost :(, good luck next time")


game = Game2048()
game.play()
