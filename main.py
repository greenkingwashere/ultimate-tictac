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
                elif (ghost == "pvc"):
                    print("Depth: ", end="", flush=True)
                    try:
                        depth = int(input())
                    except ValueError:
                        misc.printColor("Input Error")
                        continue
                    tempGame = game.game()
                    ai = learning.traditional(depth = depth)
                    tempGame.start(agent2 = ai)
                elif (ghost == "cvp"):
                    print("Depth: ", end="", flush=True)
                    try:
                        depth = int(input())
                    except ValueError:
                        misc.printColor("Input Error")
                        continue
                    tempGame = game.game()
                    ai = learning.traditional(depth=depth)
                    tempGame.start(agent1 = ai)
                elif (ghost == "cvc"):
                    print("Depth: ", end="", flush=True)
                    try:
                        depth = int(input())
                    except ValueError:
                        misc.printColor("Input Error")
                        continue
                    tempGame = game.game()
                    ai = learning.traditional(depth=depth)
                    tempGame.start(agent2 = ai, agent1 = ai)
                elif (ghost == "debug"):
                    tempGame = game.game()
                    tempGame.start(debug=True)
        except KeyboardInterrupt:
            print("\nExiting")
        