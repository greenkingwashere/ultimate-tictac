import math, copy, square, random, time, sys, misc, board, datetime, threading, game
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





    def choose(self, game, depth=5, verbose=True, debug=False, useHistory=True):
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
            score = self.tree(tempGame, depth, useHistory=useHistory)
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





    def tree(self, game, depth=5, alpha=-99, beta=99, useHistory=True, debug=False):
        """Builds game tree to search for the best move"""
        if (depth > 0 and useHistory):
            ghost = history.get(game, depth)
            if (ghost != None):
                return ghost
        if (depth <= 0 or game.isFinished() != square.square.none):
            return self.eval(game)
        if (game.player == square.square.x): #maximizing player
            current = -99
            for move in game.getAllPossibleMoves():
                tempGame = copy.deepcopy(game)
                tempGame.place(move[0], move[1])
                score = self.tree(tempGame, depth - 1, alpha=alpha, beta=beta, debug=debug)
                current = max(score, current)
                alpha = max(alpha, current)
                if (alpha >= beta):
                    break
            if (useHistory and history.get(game, depth) == None):
                history(game, depth, current)
            return current
        if (game.player == square.square.o): #minimizing player
            current = 99
            for move in game.getAllPossibleMoves():
                tempGame = copy.deepcopy(game)
                tempGame.place(move[0], move[1])
                score = self.tree(tempGame, depth - 1, alpha=alpha, beta=beta, debug=debug)
                current = min(score, current)
                beta = min(beta, current)
                if (alpha >= beta):
                    break
            if (useHistory and history.get(game, depth) == None):
                history(game, depth, current)
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






    def train(self, change=.01, max=None, verbose=True):
        """Trains the weights. Opens a certain number of threads that all play games with the original weights versus a slight change."""
        if (max == None):
            max = len(self.weights)
        threads = []
        for i in range(0,max):
            threads.append(None)

        try:
            
            while True:
                for i in threads:
                    if (i == None or not i.isAlive()):
                        if (verbose):
                            print("Detected terminated thread. Opening...")
                        
                        i = threading.Thread(target=traditional.trainThread, args=(self, threads.index(i),change, self.depth, 1, verbose,))
                        i.start()
                    time.sleep(.1)

                        

        except KeyboardInterrupt:
            #kill all threads
            misc.printColor("\nStopping training", 33)
            return


    def trainThread(self, weightIndex, weightChange, depth, trial=1, verbose=True):
        """This function is called when new threads are opened."""
        oldIntel = traditional(depth=depth)
        newIntel = traditional(depth=depth)
        newIntel.weights[weightIndex] += weightChange #adjust weight


        if (verbose):
            misc.printColor("[weight#"+str(weightIndex)+"] Starting game 1 of trial #"+str(trial)+"", 32)
            


        tempGame = game.game()
        victor1 = tempGame.start(agent1=oldIntel, agent2=newIntel, useHistory=False, verbose=False)

        if (verbose):
            print("[weight#"+str(weightIndex)+"] Game 2 of trial #"+str(trial))

        tempGame = game.game()
        victor2 = tempGame.start(agent1=newIntel, agent2=oldIntel, useHistory=False, verbose=False)

        if (victor1 == square.square.o and victor2 == square.square.x):
            if (verbose):
                misc.printColor("[weight#"+str(weightIndex)+"] New AI won both", 32)
                print("Updating weights")
            return
        if (victor1 == square.square.x and victor2 == square.square.o):
            if (verbose):
                misc.printColor("[weight#"+str(weightIndex)+"] New AI lost both", 31)
            return
        else:
            if (verbose):
                misc.printColor("[weight#"+str(weightIndex)+"] Winner game 1: "+{square.square.x:"oldAI", square.square.o:"newAI", square.square.draw:"draw"}[victor1]+", winner game 2: "+{square.square.x:"newAI", square.square.o:"oldAI", square.square.draw:"draw"}[victor2]+"", 33)
            trainThread(self, weightIndex, weightChange, depth, trial + 1, verbose=verbose)
            return



class history:
    """Contains a list of previously evaluated positions, to be accessed and used later."""

    all = [] #list of all objects
    MAX = 10000 #max amount in storage

    def __init__(self, game, depth, value):
        self.game = copy.deepcopy(game)
        self.depth = depth
        self.value = value
        history.all.append(self)
        if (len(history.all) > history.MAX):
            history.all.pop(0)

    def get(game, depth):
        """Tries to find a game that was evaluated at the provided depth or greater, returns the eval or none"""
        for i in history.all:
            if (i.game == game and i.depth >= depth):
                return i.value
        return None
