import sys, random, time, misc, learning, game, board, square







if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] == "gui"):
        pass
    else:
        misc.printFile('logo.txt')
        
        try:
            while True:
                print("> ", end="", flush=True)
                ghost = input()
                if (ghost == "pvp"):
                    tempGame = game.game()
                    tempGame.start()
                elif (ghost == "pvc" or ghost == "cvp" or ghost == "cvc"):
                    print("Depth: ", end="", flush=True)
                    try:
                        depth = int(input())
                    except ValueError:
                        misc.printColor("Input Error")
                        continue
                    print("History (y/n): ", end="", flush=True)
                    try:
                        history = {"y":True, "n":False}[input().lower()]
                    except KeyError:
                        misc.printColor("Input Error")
                        continue

                    tempGame = game.game()
                    ai = learning.traditional(depth = depth)
                    if (ghost == "pvc"):
                        tempGame.start(agent2 = ai, useHistory=history)
                    elif (ghost == "cvp"):
                        tempGame.start(agent1 = ai, useHistory=history)
                    elif (ghost == "cvc"):
                        tempGame.start(agent1 = ai, agent2=ai, useHistory=history)
                
                elif (ghost == "debug"):
                    tempGame = game.game()
                    tempGame.start(debug=True)
        except KeyboardInterrupt:
            print("\nExiting")
        