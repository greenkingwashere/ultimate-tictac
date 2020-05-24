import sys, random, time, os, datetime
import square
import board
import color
import learning


class game:
    key = {0:[0,0],1:[0,1],2:[0,2],3:[1,0],4:[1,1],5:[1,2],6:[2,0],7:[2,1],8:[2,2]}
    
    def __init__(self, verbose=False):
        self.boards = [[board.board(),board.board(),board.board()],[board.board(),board.board(),board.board()],[board.board(),board.board(),board.board()]]
        self.turn = 1
        self.player = square.square.x
        self.verbose = verbose
        self.prev = None
  
    def __eq__(self, other):
        """Overrides the == for this object, used for ignoring useless attributes when comparing games that would otherwise be identical"""
        if (self.boards == other.boards and self.player == other.player):
            return True
        return False

    def __str__(self):
        final = "\n"
        for i in range(0,3):
            for j in range(0,3):
                for l in range(0,3):
                    for k in range(0,3):
                        
                        if (self.prev != None and self.prev == [i,l,j,k]):
                            
                            final += "\033["+str(board.board.lastColor)+"m "+self.boards[i][l].squares[j][k].value+"\033[00m "
                        elif (self.boards[i][l].active):
                            final += "\033["+str(board.board.activeColor)+"m "+self.boards[i][l].squares[j][k].value+"\033[00m "
                        elif (self.boards[i][l].winner != square.square.none):
                            final += "\033["+str(board.board.finishedColor)+"m "+self.boards[i][l].squares[j][k].value+"\033[00m "
                        #elif (i[l].almostCompleted(square.square.x) or i[l].almostCompleted(square.square.o)):
                            #final += "\033["+str(33)+"m "+i[l].squares[j][k].value+"\033[00m "
                        else:
                            final += "\033["+str(board.board.inactiveColor)+"m "+self.boards[i][l].squares[j][k].value+"\033[00m "
                    final += "\t"
                final += "\n"
            final += "\n\n"
        return final
    def switch(self):
        if (self.player == square.square.x):
            self.player = square.square.o
        elif (self.player == square.square.o):
            self.player = square.square.x
    def setAllInactive(self):
        for i in self.boards:
            for j in i:
                j.active = False
    def setAllActive(self):
        for i in self.boards:
            for j in i:
                if (j.winner == square.square.none):
                    j.active = True
                else:
                    j.active = False
    def isFull(self):
        for i in self.boards:
            for j in i:
                if (not j.isFull()):
                    return False
        return True
    def allCompleted(self):
        for i in self.boards:
            for j in i:
                if (j.winner == square.square.none):
                    return False
        return True
    def isCompleted(self):
        for i in board.board.lines:
            if (self.boards[i[0][0]][i[0][1]].winner == self.boards[i[1][0]][i[1][1]].winner and self.boards[i[2][0]][i[2][1]].winner == self.boards[i[1][0]][i[1][1]].winner and (self.boards[i[0][0]][i[0][1]].winner == square.square.x or self.boards[i[0][0]][i[0][1]].winner == square.square.o)):
                return self.boards[i[0][0]][i[0][1]].winner
        if (self.isFull() or self.allCompleted()):
            return square.square.draw
        return None
    def numCompleted(self, dummy):
        total = 0
        for i in self.boards:
            for j in i:
                if (j.winner == dummy):
                    total += 1
        return total
    def numCenterCompleted(self, dummy):
        if (self.boards[1][1].winner == dummy):
            return 1
        return 0
    def numCornerCompleted(self, dummy):
        total = 0
        if (self.boards[0][0] == dummy):
            total += 1
        if (self.boards[2][0] == dummy):
            total += 1
        if (self.boards[0][2] == dummy):
            total += 1
        if (self.boards[2][2] == dummy):
            total += 1
        return total
    def numSideCompleted(self, dummy):
        total = 0
        if (self.boards[1][0] == dummy):
            total += 1
        if (self.boards[0][1] == dummy):
            total += 1
        if (self.boards[1][2] == dummy):
            total += 1
        if (self.boards[2][1] == dummy):
            total += 1
        return total

    def numAlmostCompleted(self, dummy):
        total = 0
        for i in self.boards:
            for j in i:
                if (j.almostCompleted(dummy)):
                    total += 1
        return total
    def almostCompleted(self, dummy):
        for i in board.board.lines:
            

            if (  (self.boards[i[0][0]][i[0][1]].winner == square.square.none and self.boards[i[1][0]][i[1][1]].winner == dummy and self.boards[i[2][0]][i[2][1]].winner == dummy) or (self.boards[i[1][0]][i[1][1]].winner == square.square.none and self.boards[i[0][0]][i[0][1]].winner == dummy and self.boards[i[2][0]][i[2][1]].winner == dummy) or (self.boards[i[2][0]][i[2][1]].winner == square.square.none and self.boards[i[0][0]][i[0][1]].winner == dummy and self.boards[i[1][0]][i[1][1]].winner == dummy) ):
                return True
        return False
    def total(self, dummy):
        total = 0
        for i in self.boards:
            for j in i:
                if (j.winner == square.square.none and not j.isFull()):
                    total += j.num(dummy)
        return total
    def place(self, boardX, boardY, squareX, squareY):
        if (self.boards[boardX][boardY].place(self.player, squareX, squareY)):
            if (not self.boards[squareX][squareY].isFull() and self.boards[squareX][squareY].winner == square.square.none):
                self.setAllInactive()
                self.boards[squareX][squareY].active = True
            else:
                self.setAllActive()
            if (self.player == square.square.x):
                self.turn += 1
            self.switch()
            self.prev = [boardX, boardY, squareX, squareY]
            return True
        return False
    def getAllPossibleMoves(self):
        final = []
        for i in range(0,3):
            for j in range(0,3):
                for l in range(0,3):
                    for k in range(0,3):
                        if (self.boards[i][j].active and self.boards[i][j].squares[l][k] == square.square.none):
                            final.append([i,j,l,k])
        
        return final
    def squaresOnCenter(self, dummy):
        """gets number of squares in center slots (not boards)"""
        final = 0
        for i in self.boards:
            for j in i:
                if (j.squares[1][1] == dummy):
                    final += 1
        return final
    def squaresOnSide(self, dummy):
        """gets number of squares in side slots (not boards)"""
        final = 0
        for i in self.boards:
            for j in i:
                if (j.squares[0][1] == dummy):
                    final += 1
                if (j.squares[1][0] == dummy):
                    final += 1
                if (j.squares[2][1] == dummy):
                    final += 1
                if (j.squares[1][2] == dummy):
                    final += 1
        return final
    def squaresOnCorner(self, dummy):
        """gets number of squares in corner slots (not boards)"""
        final = 0
        for i in self.boards:
            for j in i:
                if (j.squares[2][2] == dummy):
                    final += 1
                if (j.squares[0][0] == dummy):
                    final += 1
                if (j.squares[2][0] == dummy):
                    final += 1
                if (j.squares[0][2] == dummy):
                    final += 1
        return final

    def start(self, agent1=None, agent2=None, depth=5, log=False):
        """agents are players. If none they are humans. Otherwise they are machines"""


        if (log):
            text = ""

        if (self.verbose):
            print("Starting game")

        try:
            while True:

                while True:
                    #time.sleep(1)
                    if (self.verbose):
                        os.system("clear")
                        print(self)
                        print("Turn: "+str(self.turn))
                        print("History size in bytes: "+str(sys.getsizeof(learning.history.all)))
                        if (agent1 != None):
                            color.printColor("Eval: "+str(agent1.eval(self)), 33)
                        elif (agent2 != None):
                            color.printColor("Eval: "+str(agent2.eval(self)), 33)


                    if (self.player == square.square.x and agent1 != None):
                        #print("Entering agent1")
                        try:
                            attempt = agent1.choose(self, depth=depth)
                            #print("AI Attempt: "+str(attempt))
                            
                        except KeyError:
                            color.printColor("INVALID MOVE BY AGENT 1")
                            continue

                    elif (self.player == square.square.o and agent2 != None):
                        try:
                            attempt = agent2.choose(self, depth=depth)
                            #print("AI Attempt: "+str(attempt))
                            
                        except KeyError:
                            color.printColor("INVALID MOVE BY AGENT 2")
                            continue
                    else:
                        if (self.verbose):
                            print("Player "+self.player.value+"'s turn (board# square#): ",end="")
                        ghost = input()

                        if (len(ghost.split(' ')) == 2):
                            try:
                                boardNum = game.key[(int(ghost.split(' ')[0]) - 1)]
                                squareNum = game.key[(int(ghost.split(' ')[1]) - 1)]


                                attempt = [boardNum[0], boardNum[1], squareNum[0], squareNum[1]]

                                #if (not self.boards[game.key[boardNum][0]][game.key[boardNum][1]].place(self.player, game.key[squareNum][0], game.key[squareNum][1])):
                                    #raise ZeroDivisionError
                            except KeyError:
                                if (self.verbose):
                                    print("Input error")
                                continue
                    
                           
                    if (not self.place(attempt[0], attempt[1], attempt[2], attempt[3])):
                        continue
                        if (self.verbose):
                            print("Error making move")
                    
                    

                    
                    if (log):
                        text += "MOVE "+str(attempt[0])+" "+str(attempt[1])+" "+str(attempt[2])+" "+str(attempt[3])+": "
                        if (self.player == square.square.x):
                            #remember player is already switched
                            text += "player o"
                            if (agent2 != None):
                                text += " cpu\n"
                            else:
                                text += " human\n"
                        else:
                            text += "player x"
                            if (agent1 != None):
                                text += " cpu\n"
                            else:
                                text += " human\n"
                        

                    
                    if (self.isCompleted() != None):
                        if (self.verbose):
                            color.printColor(self.isCompleted().value + " player is victorious!", "0;30;42")
                        if (log):
                            if (self.isCompleted() != square.square.draw):
                                text += "GAME OVER, player "+self.isCompleted().value+" wins\n"
                            else:
                                text += "GAME OVER, draw\n"
                            f = open("games/"+str(datetime.datetime.now())+".txt", 'w+')
                            f.write(text)
                            f.close()
                        return self.isCompleted()
                
                break 

        except KeyboardInterrupt:
            if (self.verbose):
                print("Exiting game")
            if (log):
                text += "Game interrupted"
                f = open("games/"+str(datetime.datetime.now())+".txt", 'w+')
                f.write(text)
                f.close()










