import sys, math, enum, misc




#inputs: all square contents
#outputs: board number, square number
#activation function: 
#
#fitness function: 







class eval:
    """Evaluation Function."""
    
    weight = [.1,.1,.1,.1,.1,.1]

    def saveWeights():
        f = open("data/eval.txt", 'w')
        for i in eval.weight:
            f.write(str(i)+"\n")
        f.close()
    def loadWeights():
        f = open("data/eval.txt", 'r')
        dummy = 0
        for line in f:
            eval.weight[dummy] = float(line)
            dummy += 1
        f.close()









    def evaluate(boards):
        """ Eval a position, return a number from -1 to 1, negative are good for o, positive for x """
        #parameters: number of completed boards, center control, almost completed boards, squares on x, squares on +, connected super boards
        sumX = [0,0,0,0,0,0]
        sumO = [0,0,0,0,0,0]

        lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for i in boards:
            #print(str(i.values))
            if (i.winner == misc.square.x):
                sumX[0] += 1
            elif (i.winner == misc.square.o):
                sumO[0] += 1



            
            if (i.almostDone(misc.square.x)):
                sumX[2] += 1
            if (i.almostDone(misc.square.o)):
                sumO[2] += 1
        if (boards[4].winner == misc.square.none):
            for j in boards[4].values:
                if (j == misc.square.x):
                    sumX[1] += 1
                elif (j == misc.square.o):
                    sumO[1] += 1
        for i in [boards[0], boards[2], boards[6], boards[8]]:
            for j in i.values:
                if (j == misc.square.x):
                    sumX[3] += 1
                elif (j == misc.square.o):
                    sumO[3] += 1
        for i in [boards[1], boards[3], boards[5], boards[7]]:
            for j in i.values:
                if (j == misc.square.x):
                    sumX[4] += 1
                elif (j == misc.square.o):
                    sumO[4] += 1

        for i in lines:
            if (((boards[i[0]] == boards[i[1]] and boards[i[0]].winner == misc.square.x and board[i[1]].winner == misc.square.x) or (boards[i[0]] == boards[i[2]] and boards[i[0]].winner == misc.square.x and boards[i[2]].winner == misc.square.x) or (boards[i[1]] == boards[i[2]] and boards[i[1]].winner == misc.square.x and boards[i[2]].winner == misc.square.x))):
                sumX[5] += 1
            if (((boards[i[0]] == boards[i[1]] and boards[i[0]].winner == misc.square.o and board[i[1]].winner == misc.square.o) or (boards[i[0]] == boards[i[2]] and boards[i[0]].winner == misc.square.o and boards[i[2]].winner == misc.square.o) or (boards[i[1]] == boards[i[2]] and boards[i[1]].winner == misc.square.o and boards[i[2]].winner == misc.square.o))):
                sumO[5] += 1



        print(str(sumX)+", "+str(sumO))
        totalX = (eval.weight[0]*sumX[0]) + (eval.weight[1]*sumX[1]) + (eval.weight[2]*sumX[2]) + (eval.weight[3]*sumX[3]) + (eval.weight[4]*sumX[4]) + (eval.weight[5]*sumX[5])
        totalO = (eval.weight[0]*sumO[0]) + (eval.weight[1]*sumO[1]) + (eval.weight[2]*sumO[2]) + (eval.weight[3]*sumO[3]) + (eval.weight[4]*sumO[4]) + (eval.weight[5]*sumX[5])

        return math.tanh((totalX)-(totalO))











