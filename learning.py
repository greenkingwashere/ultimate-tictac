import math, copy, square, random, time, sys, misc, board, datetime
from progress.bar import ChargingBar





class traditional:
    """AI object. Uses a mimimax algorithem"""
    

    def __init__(self, weights=None, depth=5):
        if (weights==None):
            self.weights = traditional.loadWeights()
        else:
            self.weights = weights
        self.depth = depth

    def loadWeights():
        """Grabs weights from the file and returns them as a list of floats"""
        final = []
        f = open("data/weight.txt", 'r')
        for line in f:
            final.append(float(line))
        f.close()
        return final
    
    def updateWeights(values):
        """Merges new weights into the master file"""
        raise NotImplementedError





    def choose(self, game, depth=5, verbose=True, debug=False):
        """Chooses the best move by building a list of trees from each move."""
        starttime = datetime.datetime.now()
        currentBest = [-1,-1,-2.0]
        if (game.player == square.square.o):
            currentBest[2] = 2.0
        if (debug):
            print("---Start time: "+str(starttime)+"---")
        if (verbose):
            print("Choosing move from "+str(len(game.getAllPossibleMoves()))+" options")
            bar = ChargingBar("Thinking", suffix='%(percent)d%%', max=len(game.getAllPossibleMoves()))
            bar.next()
        for move in game.getAllPossibleMoves():
            tempGame = copy.deepcopy(game)
            tempGame.place(move[0], move[1])
            score = self.tree(tempGame, depth)
            if (game.player == square.square.x and score > currentBest[2]):
                currentBest = [move[0], move[1], score]
                if (score == 1.0):
                    break
            if (game.player == square.square.o and score < currentBest[2]):
                currentBest = [move[0], move[1], score]
                if (score == -1.0):
                    break
            if (verbose):
                bar.next()
        if (verbose):
            bar.finish()
            print("Selected the move "+str(currentBest[0])+" "+str(currentBest[1])+", ", end="")
            misc.printEval(currentBest[2])
        return [currentBest[0], currentBest[1]]





    def tree(self, game, depth=5, alpha=-99, beta=99):
        """Builds game tree to search for the best move"""

        if (depth <= 0 or game.isFinished() != square.square.none):
            return self.eval(game)
        if (game.player == square.square.x):
            current = -99
            for move in game.getAllPossibleMoves():
                tempGame = copy.deepcopy(game)
                tempGame.place(move[0], move[1])
                score = self.tree(tempGame, depth - 1, alpha=alpha, beta=beta)
                current = max(score, current)
                alpha = max(alpha, current)
                if (alpha >= beta):
                    break
            return current
        if (game.player == square.square.o):
            current = 99
            for move in game.getAllPossibleMoves():
                tempGame = copy.deepcopy(game)
                tempGame.place(move[0], move[1])
                score = self.tree(tempGame, depth - 1, alpha=alpha, beta=beta)
                current = min(score, current)
                beta = min(beta, current)
                if (alpha >= beta):
                    break
            return current





    def eval(self, game, debug=False):
        """Examine a board, return a number on who is winning

        """
        if (debug):
            starttime = datetime.datetime.now()
            print("---Eval start time: "+str(starttime)+"---")

        if (debug):
            temptime = datetime.datetime.now()
        if (game.isFinished() == square.square.x):
            return 1.0
        if (game.isFinished() == square.square.o):
            return -1.0
        if (game.isFinished() == square.square.draw):
            return 0.0
        if (debug):
            print("Section 1 (3x game.isFinished): "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms")

        finalX = [0,0,0,0,0,0,0,0,0,0,0]
        finalO = [0,0,0,0,0,0,0,0,0,0,0]

        totalX = 0
        totalO = 0

        # 1: Number of tiles in center board ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[0] = game.boards[4].numOfTile(square.square.x)
        finalO[0] = game.boards[4].numOfTile(square.square.o)
        if (debug):
            print("Weight 1: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[0])+", o: "+str(finalO[0]))
        # 2: Number of tiles in side boards ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[1] = game.boards[1].numOfTile(square.square.x) + game.boards[3].numOfTile(square.square.x) + game.boards[5].numOfTile(square.square.x) + game.boards[7].numOfTile(square.square.x)
        finalO[1] = game.boards[1].numOfTile(square.square.o) + game.boards[3].numOfTile(square.square.o) + game.boards[5].numOfTile(square.square.o) + game.boards[7].numOfTile(square.square.o)
        if (debug):
            print("Weight 2: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[1])+", o: "+str(finalO[1]))
        # 3: Number of tiles in the corner boards ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[2] = game.boards[0].numOfTile(square.square.x) + game.boards[2].numOfTile(square.square.x) + game.boards[6].numOfTile(square.square.x) + game.boards[8].numOfTile(square.square.x)
        finalO[2] = game.boards[0].numOfTile(square.square.o) + game.boards[2].numOfTile(square.square.o) + game.boards[6].numOfTile(square.square.o) + game.boards[8].numOfTile(square.square.o)
        if (debug):
            print("Weight 3: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[2])+", o: "+str(finalO[2]))
        # 4: Number of completed center boards ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[3] = game.numCenterCompleted(square.square.x)
        finalO[3] = game.numCenterCompleted(square.square.o)
        if (debug):
            print("Weight 4: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[3])+", o: "+str(finalO[3]))
        # 5: Number of completed corner boards ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[4] = game.numCornerCompleted(square.square.x)
        finalO[4] = game.numCornerCompleted(square.square.o)
        if (debug):
            print("Weight 5: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[4])+", o: "+str(finalO[4]))
        # 6: Number of completed side boards ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[5] = game.numSideCompleted(square.square.x)
        finalO[5] = game.numSideCompleted(square.square.o)
        if (debug):
            print("Weight 6: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[5])+", o: "+str(finalO[5]))
        # 7: Number of almost completed boards ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[6] = game.numAlmostCompleted(square.square.x)
        finalO[6] = game.numAlmostCompleted(square.square.o)
        if (debug):
            print("Weight 7: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[6])+", o: "+str(finalO[6]))
        # 8: Number of adjacent completed boards ---
        if (debug):
            temptime = datetime.datetime.now()
        if (game.almostCompleted(square.square.x)):
            finalX[7] = 1
        if (game.almostCompleted(square.square.o)):
            finalO[7] = 1
        if (debug):
            print("Weight 8: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[7])+", o: "+str(finalO[7]))
        # 9: Number of tiles in center ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[8] = game.squaresOnCenter(square.square.x)
        finalO[8] = game.squaresOnCenter(square.square.o)
        if (debug):
            print("Weight 9: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[8])+", o: "+str(finalO[8]))
        # 10: Number of tiles in sides ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[9] = game.squaresOnSides(square.square.x)
        finalO[9] = game.squaresOnSides(square.square.o)
        if (debug):
            print("Weight 10: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[9])+", o: "+str(finalO[9]))
        # 11: Number of tiles in corners ---
        if (debug):
            temptime = datetime.datetime.now()
        finalX[10] = game.squaresOnCorners(square.square.x)
        finalO[10] = game.squaresOnCorners(square.square.o)
        if (debug):
            print("Weight 11: "+str((datetime.datetime.now() - temptime).microseconds / 1000)+"ms, x: "+str(finalX[10])+", o: "+str(finalO[10]))




        for i in range(0,len(finalX)):
            totalX += finalX[i] * self.weights[i]
            totalO += finalO[i] * self.weights[i]


        return math.tanh(totalX-totalO)
    

