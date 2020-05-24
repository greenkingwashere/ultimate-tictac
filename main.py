import game, learning, color, _thread, random, time, square









def trainGame(depth=5, change=.01):
    tempGame = game.game(verbose=False)
    color.printColor(tempGame.start(learning.traditional(verbose=True), learning.traditional(verbose=True), depth=depth).value+" player wins after "+str(tempGame.turn)+" turns!",33)








if __name__ == "__main__":

    

    try:

        print("Welcome to Ultimate Tic Tac Toe. Options: pvp, pvc, or cvc\nTraining option is also available for testing")
        while True:
            print("> ", end="")
            dummy = input()
            if (dummy == "pvp"):
                startingGame = game.game(verbose=True)
                startingGame.start()
            elif (dummy == "pvc" or dummy == "cvp"):
                print("Depth: ", end="")
                dummy = input()
                try:
                    assert int(dummy) > 1
                    startingGame = game.game(verbose=True)
                    startingGame.start(agent1=None, agent2=learning.traditional(verbose=True), depth=int(dummy), log=True)
                except (ValueError, AssertionError) as e:
                    color.printException(e)
            elif (dummy == "cvc"):
                print("Depth: ", end="")
                dummy = input()
                try:
                    assert int(dummy) > 1
                    startingGame = game.game(verbose=True)
                    startingGame.start(learning.traditional(verbose=True), learning.traditional(verbose=True), depth=int(dummy), log=True)
                except (ValueError, AssertionError) as e:
                    color.printException(e)
            
            elif (dummy == "train"):
                print("Depth: ", end="")
                try:
                    dummy1 = int(input())
                    assert dummy1 > 1
                    print("Change value (default .01): ", end="")
                    dummy2 = (input())
                    if (dummy2 == ""):
                        dummy2 = .01
                    dummy2 = float(dummy2)
                    assert dummy2 > 0
                    

                except (ValueError, AssertionError) as e:
                    color.printException(e)

                color.printColor("Starting training. Ctrl+c to cancel", "0;30;42")

                try:
                    while True:
                        print("Current weights: "+str(learning.traditional.loadWeights())+"\nSelecting a weight at random... ", end="")
                        current = random.randint(0,len(learning.traditional.loadWeights())-1)
                        direction = {0:-1, 1:1}[random.randint(0,1)]
                        color.printColor("Selected "+str(current)+", which is currently "+str(learning.traditional.loadWeights()[current])+", direction: "+str(direction), 32)
                        

                        times = 1
                        while True:
                            color.printColor("Starting trial #"+str(times)+" for weight #"+str(current), "0;37;44")


                            tempGame = game.game(verbose = False)

                            oldAI = learning.traditional(verbose=True)
                            newAI = learning.traditional(verbose=True)

                            newAI.weights[current] += (times * dummy2 * direction)
                            print("Adjusted weight for "+str(current)+": "+str(newAI.weights[current]))


                            color.printColor("Starting game with newAI as X", "0;30;43")
                            winner1 = tempGame.start(newAI, oldAI, dummy1, log=True)
                            color.printColor("Finished first game with a winner of "+str(winner1.value), "0;30;43")

                            tempGame = game.game(verbose = False)

                            color.printColor("Starting game with newAI as O", "0;30;43")
                            winner2 = tempGame.start(oldAI, newAI, dummy1, log=True)
                            color.printColor("Finished second game with a winner of "+str(winner2.value), "0;30;43")

                            


                            if (winner1 == square.square.x and winner2 == square.square.o):
                                color.printColor("New AI won both! Saving weights...", 32)
                                learning.traditional.updateWeights(newAI.weights)
                                break

                            elif (winner1 == square.square.x and winner2 == square.square.draw):
                                color.printColor("New AI won as X then draw as O", 33)

                            elif (winner1 == square.square.draw and winner2 == square.square.o):
                                color.printColor("New AI won as O then draw as X", 33)

                            elif (winner1 == square.square.x and winner2 == square.square.x):
                                color.printColor("New AI won as X then lost as O", 33)

                            elif (winner1 == square.square.o and winner2 == square.square.o):
                                color.printColor("New AI won as O then lost as X", 33)

                            else:
                                color.printColor("New AI lost both", 31)
                                break


                            times += 1
                        color.printColor("Concluding the round of training.\n\n\n", 36)


                except KeyboardInterrupt:
                    color.printColor("Aborting training")


    except KeyboardInterrupt:
        print("Goodbye")

  




