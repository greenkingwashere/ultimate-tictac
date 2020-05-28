import sys, random, time, os, datetime, square, board, misc, learning










class game:
    """A game object. Contains the 9 boards and other attributes associated with a game.
    Also contains the functions required to play the game to supplement the helper function in board.py"""


    def __init__(self):
        """Game object"""
        self.boards = [board.board(), board.board(), board.board(), board.board(), board.board(), board.board(), board.board(), board.board(), board.board()]
        self.turn = 1 #cosmetic move count 
        self.player = square.square.x #current player to move, starts on X
        self.prev = None #previous move, used when printing the board.

    def __eq__(self, other):
        """Overrides default ==. Ignores irrelevent attributes when comparing games"""
        for i in range(0,9):
            for j in range(0,9):
                if (self.boards[i].squares[j] != other.boards[i].squares[j]):
                    return False
        if (self.player != other.player):
            return False
        return True

    def __str__(self):
        """Print the boards for str(self)"""
        final = ""

        key = {0:[0,1,2],1:[3,4,5],2:[6,7,8]}
        for i in range(0,3):
            for j in range(0,3):
                for k in range(0,3):
                    for l in range(0,3):
                        if (self.prev == [key[i][k], key[j][l]]):
                            final += "\033[34m "+self.boards[key[i][k]].squares[key[j][l]].value+"\033[00m"
                        elif (self.boards[key[i][k]].active):
                            final += "\033[36m "+self.boards[key[i][k]].squares[key[j][l]].value+"\033[00m"
                        elif (self.boards[key[i][k]].winner == square.square.x):
                            final += "\033[32m "+self.boards[key[i][k]].squares[key[j][l]].value+"\033[00m"
                        elif (self.boards[key[i][k]].winner == square.square.o):
                            final += "\033[31m "+self.boards[key[i][k]].squares[key[j][l]].value+"\033[00m"
                        elif (self.boards[key[i][k]].winner == square.square.draw):
                            final += "\033[33m "+self.boards[key[i][k]].squares[key[j][l]].value+"\033[00m"
                        else:
                            final += " "+self.boards[key[i][k]].squares[key[j][l]].value
                    final += "\t"
                final += "\n"
            final += "\n\n"
        return final

    def switchPlayer(self):
        """Switches players from x to o or vice versa"""
        if (self.player == square.square.o):
            self.player = square.square.x
        elif (self.player == square.square.x):
            self.player = square.square.o

    def setAllInactive(self):
        """Set all boards to inactive"""
        for i in self.boards:
            i.active = False

    def setAllActive(self):
        """Set all boards to active if not done"""
        for i in self.boards:
            if (i.winner == square.square.none):
                i.active = True

    def allCompleted(self):
        """Returns true if all boards can't be played on"""
        for i in self.boards:
            if (i.winner == square.square.none):
                return False
        return True
    
    def isFull(self):
        """Returns true if all boards are completly full"""
        for i in self.boards:
            if (not i.isFull()):
                return False
        return True

    def isFinished(self):
        """Returns the winner if there is one, otherwise returns none"""
        for i in board.board.lines:
            if (self.boards[i[0]].winner == self.boards[i[1]].winner and self.boards[i[1]].winner == self.boards[i[2]].winner and self.boards[i[0]].winner != square.square.none and self.boards[i[0]].winner != square.square.draw):
                return self.boards[i[0]].winner
        if (self.isFull() or self.allCompleted()):
            return square.square.draw
        return square.square.none

    def place(self, boardX, squareX, verbose=False):
        """Try to make a move, and sets up boards for next move"""
        if (self.boards[boardX].place(self.player, squareX)):
            if (not self.boards[squareX].isFull() and self.boards[squareX].winner == square.square.none):
                self.setAllInactive()
                self.boards[squareX].active = True
            else:
                self.setAllActive() #wildcard!!
            if (self.player == square.square.o):
                self.turn += 1
            self.switchPlayer()
            self.prev = [boardX, squareX]
            return True
        return False



    # ============= HELPER FUNCTIONS FOR AI BELOW ===================

    def getAllPossibleMoves(self):
        """Returns a list of every legal move in the current position. Use len() to get number of legal moves"""
        final = []
        for i in range(0,9):
            for j in range(0,9):
                if (self.boards[i].active and self.boards[i].squares[j] == square.square.none):
                    final.append([i,j])
        return final

    def numCompleted(self, tile):
        """Get number of completed boards by a certain player"""
        total = 0
        for i in self.boards:
            if (i.winner == tile):
                total += 1
        return total

    def numCenterCompleted(self, tile):
        """If the center board is completed by tile, return 1"""
        if (self.boards[4].winner == tile):
            return 1
        return 0

    def numCornerCompleted(self, tile):
        """How many corner boards are won by tile"""
        total = 0
        for i in [0,2,6,8]:
            if (self.boards[i].winner == tile):
                total += 1
        return total

    def numSideCompleted(self, tile):
        """How many side boards are won by tile"""
        total = 0
        for i in [1,3,5,7]:
            if (self.boards[i].winner == tile):
                total += 1
        return total

    def numAlmostCompleted(self, tile):
        """Number of boards almost completed by a certain tile"""
        total = 0
        for i in self.boards:
            if (i.almostCompleted(tile)):
                total += 1
        return total

    def almostCompleted(self, tile):
        """Returns true if the player has 2 in a row"""
        for i in board.board.lines:
            if ((self.boards[i[0]].winner == square.square.none and self.boards[i[1]].winner == tile and self.boards[i[2]].winner == tile) or (self.boards[i[0]].winner == tile and self.boards[i[1]].winner == square.square.none and self.boards[i[2]].winner == tile) or (self.boards[i[0]].winner == tile and self.boards[i[1]].winner == tile and self.boards[i[2]].winner == square.square.none)):
                return True
        return False
    
    def total(self, tile):
        """Returns number of tiles on the board"""
        total = 0
        for i in self.boards:
            if (i.winner == square.square.none and not i.isFull()):
                total += i.numOfTile(tile)
        return total

    def squaresOnCenter(self, tile):
        """Returns number of centered squares"""
        total = 0
        for i in self.boards:
            if (i.squares[4] == tile):
                total += 1
        return total

    def squaresOnCorners(self, tile):
        """Returns number of corner squares"""
        total = 0
        for i in self.boards:
            for j in [0,2,6,8]:
                if (i.squares[j] == tile):
                    total += 1
        return total

    def squaresOnSides(self, tile):
        """Returns number of side squares"""
        total = 0
        for i in self.boards:
            for j in [1,3,5,7]:
                if (i.squares[j] == tile):
                    total += 1
        return total

    # ============= END HELPERS ======================




    def start(self, agent1=None, agent2=None, verbose=True, debug=False, useHistory=True):
        """
        Play a game. Agents are whatever is playing; none is a human and otherwise it is a learning object.
        """


        if (verbose):
            print("Starting game.")

        try:

            while True:
                if (verbose):
                    os.system("clear") #clear the screen
                    print(str(self))
                    print("Turn "+str(self.turn)+"")
                    if (agent1 != None):
                        print("Eval: ", end="")
                        misc.printEval(agent1.eval(self, debug=debug))
                    elif (agent2 != None):
                        print("Eval: ", end="")
                        misc.printEval(agent2.eval(self, debug=debug))
                    if (debug):
                        print("Number of possible moves: "+str(len(self.getAllPossibleMoves())))
                        print("Winners: ", end="")
                        for i in self.boards:
                            print(i.winner.value+", ", end="")
                        print("\nhistory len: "+str(len(learning.history.all))+" bytes: "+str(sys.getsizeof(learning.history.all)))


                while True:
                    try:
                        if ((self.player == square.square.x and agent1 == None) or (self.player == square.square.o and agent2 == None)):
                            if (verbose):
                                print("Player "+self.player.value+"'s move (board# square#): ", end="", flush=True)
                            rawinput = input()
                            if (rawinput == "debug"):
                                debug = not debug
                                continue
                            move = [int(rawinput.split(' ')[0]) - 1, int(rawinput.split(' ')[1]) - 1]
                        elif (self.player == square.square.x): #agent1's move
                            move = agent1.choose(self, depth=agent1.depth, useHistory=useHistory)
                        elif (self.player == square.square.o): #agent2's move
                            move = agent2.choose(self, depth=agent2.depth, useHistory=useHistory)
                        if (self.place(move[0],move[1])):
                            break
                        else:
                            raise IndexError
                    except (IndexError, ValueError):
                        misc.printColor("Invalid move")
                if (self.isFinished() != square.square.none):
                    if (verbose):
                        if (self.isFinished() == square.square.draw):
                            misc.printColor("Game ended as a draw", 34)
                        else:
                            misc.printColor("Player "+self.isFinished().value+" is victorious!", 32)
                    return self.isFinished()



        except KeyboardInterrupt:
            if (verbose):
                misc.printColor("\nGame interrupted")
        #except Exception as e:
            #if (verbose):
                #misc.printException(e)


