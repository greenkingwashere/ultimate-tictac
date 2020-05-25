import square, misc



class board:
    """Objects representing a board, containing squares
    indexes:
    0 1 2
    3 4 5
    6 7 8
    """
    lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]] #all lines on the board (left to right, up to down, diagnals)





    def __init__(self):
        """Initialize a board
        squares: all 9 squares of the board, starting at the top left and ending at the bottom right, start off empty
        winner: if the board is completed, this is the winner of the board.
        active: if the board can be played on for that turn
        """
        self.squares = [square.square.none, square.square.none, square.square.none, square.square.none, square.square.none, square.square.none, square.square.none, square.square.none, square.square.none]
        self.winner = square.square.none
        self.active = True

    def place(self, tile, x):
        """Place a tile on the board. Returns true or false if it works or not"""
        if (self.squares[x] == square.square.none and self.winner == square.square.none and self.active):
            self.squares[x] = tile
            self.update()
            return True
        return False

    def update(self):
        """Refresh a board to check for winners"""
        if (self.isFull()):
            self.winner = square.square.draw
            self.active = False
        elif (self.isCompleted() != square.square.none):
            self.winner = self.isCompleted()
            self.active = False

    def numOfTile(self, tile):
        """Check the number of a certain tile on the board"""
        total = 0
        for i in self.squares:
            if (i == tile):
                total += 1
        return total

    def almostCompleted(self, tile):
        """Check if a board is one tile away from being completed by a certain tile"""
        for i in board.lines:
            if ((self.squares[i[0]] == square.square.none and self.squares[i[1]] == tile and self.squares[i[2]] == tile) or (self.squares[i[0]] == tile and self.squares[i[1]] == square.square.none and self.squares[i[2]] == tile) or (self.squares[i[0]] == tile and self.squares[i[1]] == tile and self.squares[i[2]] == square.square.none)):
                return True
        return False

    def isCompleted(self):
        """Checks if a board is completed (3 in a row), returns the winner (or none)"""
        for i in board.lines:
            if (self.squares[i[0]] == self.squares[i[1]] and self.squares[i[1]] == self.squares[i[2]] and (self.squares[i[0]] == square.square.x or self.squares[i[0]] == square.square.o)):
                return self.squares[i[0]]
        return square.square.none

    def isFull(self):
        """Returns true if the board is full"""
        for i in self.squares:
            if (i == square.square.none):
                return False
        return True
