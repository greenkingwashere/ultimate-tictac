import square, color




class board:
    lines = [[[0,0],[0,1],[0,2]], [[1,0],[1,1],[1,2]], [[2,0],[2,1],[2,2]], [[0,0],[1,0],[2,0]], [[0,1],[1,1],[2,1]], [[0,2],[1,2],[2,2]], [[0,0],[1,1],[2,2]], [[2,0],[1,1],[0,2]]]
    inactiveColor = 0
    activeColor = 31
    finishedColor = "0;34;40"
    lastColor = "0;36;40"

    def __init__(self):
        self.squares = [[square.square.none,square.square.none,square.square.none],[square.square.none,square.square.none,square.square.none],[square.square.none,square.square.none,square.square.none]]
        self.winner = square.square.none
        self.active = True
        self.verbose = False
    
  
    def place(self, tile, x, y):
        if (self.squares[x][y] == square.square.none and self.winner == square.square.none and self.winner == square.square.none and self.active):
            self.squares[x][y] = tile
            self.update()
            return True
        else:
            return False

    def update(self):
        if (not self.isCompleted() and self.isFull()):
            self.winner = square.square.draw
            self.active = False
            if (self.verbose):
                print("Board full")

    def num(self, dummy):
        total = 0
        for i in self.squares:
            for j in i:
                if (j == dummy):
                    total += 1
        return total
    def almostCompleted(self, dummy):
        for i in board.lines:
            

            if (  (self.squares[i[0][0]][i[0][1]] == square.square.none and self.squares[i[1][0]][i[1][1]] == dummy and self.squares[i[2][0]][i[2][1]] == dummy) or (self.squares[i[1][0]][i[1][1]] == square.square.none and self.squares[i[0][0]][i[0][1]] == dummy and self.squares[i[2][0]][i[2][1]] == dummy) or (self.squares[i[2][0]][i[2][1]] == square.square.none and self.squares[i[0][0]][i[0][1]] == dummy and self.squares[i[1][0]][i[1][1]] == dummy) ):
                return True
        return False
                

    def isCompleted(self):
        for i in board.lines:
            if (self.squares[i[0][0]][i[0][1]] == self.squares[i[1][0]][i[1][1]] and self.squares[i[2][0]][i[2][1]] == self.squares[i[1][0]][i[1][1]] and (self.squares[i[0][0]][i[0][1]] == square.square.x or self.squares[i[0][0]][i[0][1]] == square.square.o)):
                self.winner = self.squares[i[0][0]][i[0][1]]
                self.active = False
                if (self.verbose):
                    print("Board completed as "+self.squares[i[0][0]][i[0][1]].value)
                return True
        return False

    def isFull(self):
        for i in self.squares:
            for j in i:
                if (j == square.square.none):
                    return False
        return True

  
  
  
