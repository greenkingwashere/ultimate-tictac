import  math, copy, square, random, time, sys, color, datetime
from progress.bar import ChargingBar












class traditional:


    def __init__(self, weights=None, verbose=False):
        if (weights==None):
            self.weights = traditional.loadWeights()
        else:
            self.weights = weights
        self.verbose = verbose

    def loadWeights():
        final = []
        f = open("data/weight.txt", 'r')
        for line in f:
            final.append(float(line))
        f.close()
        return final
    def updateWeights(values):
        """Save new weights and archive old ones"""
        f = open("data/old/"+str(datetime.datetime.now())+".txt", 'w+')
        for line in traditional.loadWeights():
            f.write(str(line)+"\n")
        f.close()
        f = open("data/weight.txt", 'w')
        for line in values:
            f.write(str(line)+"\n")
        f.close()
    def choose(self, game, depth=5, turbo=False):
        """Chooses the best move"""
        startTime = datetime.datetime.now()


        currentBest = [-1,-1,-1,-1,-2.0]
        if (game.player == square.square.o):
            currentBest[4] = 2.0

        if (self.verbose):
            print("Choosing move from ", end="")
            numOfMoves = len(game.getAllPossibleMoves())
            if (numOfMoves < 5):
                color.printColor(str(numOfMoves), 32, end="")
            elif (numOfMoves < 10):
                color.printColor(str(numOfMoves), 33, end="")
            else:
                color.printColor(str(numOfMoves), 31, end="")
            print(" possible options, depth of "+str(depth))
            bar = ChargingBar("Thinking", suffix='%(percent)d%%', max=len(game.getAllPossibleMoves()))
            bar.next()

        for move in game.getAllPossibleMoves():
            
            tempGame = copy.deepcopy(game)
            tempGame.place(move[0],move[1],move[2],move[3])
            score = self.tree(tempGame, 0, depth)
            if (game.player == square.square.x and score > currentBest[4]):
                currentBest = [move[0], move[1], move[2], move[3], score]
                if (score == 1.0):
                    break
            if (game.player == square.square.o and score < currentBest[4]):
                currentBest = [move[0], move[1], move[2], move[3], score]
                if (score == -1.0):
                    break
            if (self.verbose):
                bar.next()
                #print("Score for "+str(move)+" is "+str(score)+" ---------")
                

        if (self.verbose):
            bar.finish()
            print("Selected the move "+str(currentBest[0:4])+" which had a score of ", end="")
            dummy = (currentBest[4])
            if (dummy == 1.0):
                color.printColor(str(dummy), "0;37;42")
            elif (dummy > 0):
                color.printColor(str(dummy), 32)
            elif (dummy == 0):
                print(str(dummy))
            elif (dummy > -1.0):
                color.printColor(str(dummy), 31)
            else:
                color.printColor(str(dummy), "0;37;41")
            color.printColor("Total time: ", "1;37;40", end="")
            print(str((datetime.datetime.now()-startTime).seconds)+" seconds ", end="")
            color.printColor("Average time per move: ", "1;37;40", end="")
            print(str((datetime.datetime.now()-startTime).seconds/float(len(game.getAllPossibleMoves())))+" seconds ", end="\n")

        #time.sleep(1)               
        return currentBest
                    
    def tree(self, game, curDepth, depth, alpha=-99, beta=99):
        """Builds a game tree to search for the optimal move. 
        curDepth gets incremented with each level of the tree
        alpha and beta should start at their defualt values but get updated with recursed
        """
        
        tempEval = history.getGame(game, curDepth)
        if (tempEval != None):
            print("Check: "+str(tempEval))
            return tempEval

        if (curDepth >= depth or game.isCompleted() != None):
            score = self.eval(game)
            history(game, curDepth, score) #log the completed eval in history
            return score

        if (game.player == square.square.x): #(looking for maximum score value)
            current = -99
            for move in game.getAllPossibleMoves():
                tempGame = copy.deepcopy(game)
                tempGame.place(move[0],move[1],move[2],move[3]) #WORKING ON THIS
                score = self.tree(tempGame, curDepth + 1, depth, alpha=alpha, beta=beta)
                current = max(score, current)
                alpha = max(alpha, current)
                if (alpha >= beta):
                    break
            
            history(game, curDepth, current) #log the completed eval in history
            return current
        elif (game.player == square.square.o): #looking for minimum value
            current = 99
            for move in game.getAllPossibleMoves():
                tempGame = copy.deepcopy(game)
                tempGame.place(move[0],move[1],move[2],move[3]) #WORKING ON THIS
                score = self.tree(tempGame, curDepth + 1, depth, alpha=alpha, beta=beta)
                current = min(score, current)
                beta = min(beta, current)
                if (alpha >= beta):
                    break
            
            history(game, curDepth, current) #log the completed eval in history
            return current
        return 0.0
        



    def eval(self, game):
        """Examine a board, return a number on who is winning
        
        Criteria:
        1) number of squares in centered board
        2) number of squares in the outside boards
        3) number of squares in corner boards
        4) number of completed boards in center
        5) completed boards in corners
        6) completed boards in sides
        7) number of almost completed boards
        8) adjacent completed boards
        9) number of squares in center
        10) number of squares on sides
        11) number of squares on corners
        """

        if (game.isCompleted() == square.square.x):
            return 1.0
        if (game.isCompleted() == square.square.o):
            return -1.0
        if (game.isCompleted() == square.square.draw):
            return 0.0

        finalX = [0,0,0,0,0,0,0,0,0,0,0]
        finalO = [0,0,0,0,0,0,0,0,0,0,0]

        totalX = 0
        totalO = 0

        finalX[0] = game.boards[1][1].num(square.square.x)
        finalO[0] = game.boards[1][1].num(square.square.o)

        finalX[1] = game.boards[0][1].num(square.square.x) + game.boards[1][0].num(square.square.x) + game.boards[2][1].num(square.square.x) + game.boards[1][2].num(square.square.x)
        finalO[1] = game.boards[0][1].num(square.square.o) + game.boards[1][0].num(square.square.o) + game.boards[2][1].num(square.square.o) + game.boards[1][2].num(square.square.o)

        finalX[2] = game.boards[0][0].num(square.square.x) + game.boards[2][2].num(square.square.x) + game.boards[2][0].num(square.square.x) + game.boards[0][2].num(square.square.x)
        finalO[2] = game.boards[0][0].num(square.square.o) + game.boards[2][2].num(square.square.o) + game.boards[2][0].num(square.square.o) + game.boards[0][2].num(square.square.o)
        
        finalX[3] = game.numCenterCompleted(square.square.x)
        finalO[3] = game.numCenterCompleted(square.square.o)

        finalX[4] = game.numCornerCompleted(square.square.x)
        finalO[4] = game.numCornerCompleted(square.square.o)

        finalX[5] = game.numSideCompleted(square.square.x)
        finalO[5] = game.numSideCompleted(square.square.o)


        finalX[6] = game.numAlmostCompleted(square.square.x)
        finalO[6] = game.numAlmostCompleted(square.square.o)

        if (game.almostCompleted(square.square.x)):
            finalX[7] = 1
        if (game.almostCompleted(square.square.o)):
            finalO[7] = 1

        finalX[8] = game.squaresOnCenter(square.square.x)
        finalO[8] = game.squaresOnCenter(square.square.o)

        finalX[9] = game.squaresOnSide(square.square.x)
        finalO[9] = game.squaresOnSide(square.square.o)

        finalX[10] = game.squaresOnCorner(square.square.x)
        finalO[10] = game.squaresOnCorner(square.square.o)


        for i in range(0,len(finalX)):
            totalX += finalX[i] * self.weights[i]
            totalO += finalO[i] * self.weights[i]

        return math.tanh(totalX-totalO)
        







class history:
    """Tracks previous made node evaluations, so that if an identical node comes up it can reuse the found values."""

    all = []
    MAX = 10000 #max size of all

    def __init__(self, game, depth, value):
        #print("Creating history object. Values: "+str(depth)+", "+str(value))
        self.game = game #the evaluated position
        self.depth = depth #the depth it was evaluated at
        self.value = value #the result float, -1 to 1
        if (self.depth > 1):
            history.all.append(self)
            if (len(history.all) > history.MAX):
                history.all.pop(0)

    def getGame(game, depth):
        """If all contains a matching game with depth greater then or equal to the provided depth, return the value. Otherwise, return None.
        Refer to the __eq__ of the game class for equality tests"""
        
        for i in history.all:
            if (game == i.game):
                #print("Using found history: "+str(i.value))
                return i.value
        return None