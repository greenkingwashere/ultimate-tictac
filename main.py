import pygame, sys, random, time
import learning as ai
import misc




pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((650,650))
clock = pygame.time.Clock()
pygame.display.set_caption("Ultimate Tic Tac Toe")









class table:
    boards = []
    key = {0:[0,0],1:[50,0],2:[100,0],3:[0,50],4:[50,50],5:[100,50],6:[0,100],7:[50,100],8:[100,100]}
    lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    globalWinner = misc.square.none
    def __init__(self, x=0, y=0, color=[0, 0, 0]):
        self.x = x
        self.y = y
        self.color=color
        self.values = [misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none]
        self.winner = misc.square.none
        self.active = True


    def empty(self):
        self.values = [misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none, misc.square.none]
    def fill(self, dummy):
        self.values = [dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy]
    def isFull(self):
        for i in self.values:
            if (i == misc.square.none):
                return False
        return True
    def blit(self):
        global smallfont
        global debug
        if (self.active):
            pygame.draw.rect(screen, [255, 102, 102], [self.x, self.y, 150, 150])
        for i in range(0, len(self.values)):
            if (self.values[i] == misc.square.x):
                pygame.draw.line(screen, self.color, [table.key[i][0]+self.x+10, table.key[i][1]+self.y+10], [table.key[i][0]+self.x+40, table.key[i][1]+self.y+40], 2)
                pygame.draw.line(screen, self.color, [table.key[i][0]+self.x+10, table.key[i][1]+self.y+40], [table.key[i][0]+self.x+40, table.key[i][1]+self.y+10], 2)
            elif (self.values[i] == misc.square.o):
                pygame.draw.circle(screen, self.color, [table.key[i][0]+self.x+25, table.key[i][1]+self.y+25], 15, 1)
            else:
                if (collides(table.key[i][0]+self.x, table.key[i][1]+self.y, 50, 50) and self.winner == misc.square.none and table.globalWinner == misc.square.none and self.active):
                    pygame.draw.rect(screen, [255, 140, 140], [table.key[i][0]+self.x, table.key[i][1]+self.y, 50, 50])
        pygame.draw.line(screen, self.color, [self.x+50, self.y], [self.x+50, self.y+150])
        pygame.draw.line(screen, self.color, [self.x+100, self.y], [self.x+100, self.y+150])
        pygame.draw.line(screen, self.color, [self.x, self.y+50], [self.x+150, self.y+50])
        pygame.draw.line(screen, self.color, [self.x, self.y+100], [self.x+150, self.y+100])
        if (self.winner == misc.square.draw):
            #screen.blit(smallfont.render("Draw", True, (0,0,0)), [self.x+55, self.y+155])
            pass
        if (self.winner == misc.square.x):
            #screen.blit(smallfont.render("X's win!", True, (0,0,0)), [self.x+50, self.y+155])
            pygame.draw.line(screen, self.color, [self.x,self.y], [self.x+150,self.y+150], 5)
            pygame.draw.line(screen, self.color, [self.x+150,self.y], [self.x,self.y+150], 5)

        if (self.winner == misc.square.o):
            #screen.blit(smallfont.render("O's win!", True, (0,0,0)), [self.x+50, self.y+155])
            pygame.draw.circle(screen, self.color, [self.x+75,self.y+75], 65, 4)
    def blitAll():
        for i in table.boards:
            i.blit()
    def almostDone(self, dummy):
        """Returns true if almost finished board"""
        for i in table.lines:
            if (((self.values[i[0]] == self.values[i[1]] and self.values[i[0]] == dummy and self.values[i[1]] == dummy) or (self.values[i[0]] == self.values[i[2]] and self.values[i[0]] == dummy and self.values[i[2]] == dummy) or (self.values[i[1]] == self.values[i[2]] and self.values[i[1]] == dummy and self.values[i[2]] == dummy)) and self.winner == misc.square.none):
                return True
        return False
    


    def check():
        """using mouse coords, check if the click was on a suitable square"""
        global active
        for i in table.boards:
            for j in range(0,len(i.values)):
                if (collides(table.key[j][0]+i.x, table.key[j][1]+i.y) and i.values[j] == misc.square.none and i.winner == misc.square.none and table.globalWinner == misc.square.none and i.active):
                    i.values[j] = active
                    
                    switch()
                    table.boards[j].update()
                    if (table.boards[j].winner == misc.square.none):
                        table.setAllInactive()
                        table.boards[j].active = True
                    else:
                        table.setAllActive()
                    
        table.updateBoards()
    
    def update(self):
        for i in table.lines:
            
            if (self.values[i[0]] == self.values[i[1]] and self.values[i[1]] == self.values[i[2]] and self.values[i[0]] != misc.square.none): #tic tac detected
                self.winner = self.values[i[0]]
                self.active = False
                return
        if self.isFull():
            self.winner = misc.square.draw
            self.color=[150,150,150]
            self.active = False
    def setAllInactive():
        for i in table.boards:
            i.active = False
    def setAllActive():
        for i in table.boards:
            if (i.winner == misc.square.none):
                i.active = True
            else:
                i.active = False
    def checkForWinner():
        for i in table.lines:
            if (table.boards[i[0]].winner == table.boards[i[1]].winner and table.boards[i[1]].winner == table.boards[i[2]].winner and table.boards[i[0]].winner != misc.square.none and table.boards[i[0]].winner != misc.square.draw):
                table.globalWinner = table.boards[i[0]].winner
    def updateBoards():
        for i in table.boards:
            i.update()
        table.checkForWinner()

def collides(x, y, width=50, height=50):
    """Check for mouse collision"""
    if (pygame.mouse.get_pos()[0] > x and pygame.mouse.get_pos()[0] < x + width and pygame.mouse.get_pos()[1] > y and pygame.mouse.get_pos()[1] < y + height):
        return True
    return False



smallfont = pygame.font.SysFont("Arial", 16)
bigfont = pygame.font.SysFont("Arial", 36)
hugefont = pygame.font.SysFont("Arial", 50)

debug = False
active = misc.square.x
def switch():
    global active
    if (active == misc.square.x):
        active=misc.square.o
    else:
        active = misc.square.x


table.boards = [table(50, 50),table(250, 50),table(450, 50),table(50, 250),table(250, 250),table(450, 250),table(50, 450),table(250, 450),table(450, 450)]
mode = 0







ai.eval.loadWeights()
ai.eval.saveWeights()
print(str(ai.eval.weight))









while True:
    clock.tick(60)

    screen.fill([255, 255, 255])
    screen.blit(hugefont.render("Ultimate Tic Tac Toe", True, [0,0,0]),[55,10])

    if (collides(300,200,120,40)):
        screen.blit(bigfont.render("P v P", True, [250,0,0]),[300,200])
    else:
        screen.blit(bigfont.render("P v P", True, [0,0,0]),[300,200])
    if (collides(300,300,120,40)):
        screen.blit(bigfont.render("P v Cpu", True, [250,0,0]),[300,300])
    else:
        screen.blit(bigfont.render("P v Cpu", True, [0,0,0]),[300,300])
    if (collides(300,400,120,40)):
        screen.blit(bigfont.render("Cpu v Cpu", True, [250,0,0]),[300,400])
    else:
        screen.blit(bigfont.render("Cpu v Cpu", True, [0,0,0]),[300,400])
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (collides(300,200,120,40)):#pvp
                mode = 1
            if (collides(300,300,120,40)):
                mode = 2
            if (collides(300,400,120,40)):
                mode = 3

    if (mode != 0):
        while True:
            clock.tick(60)

            screen.fill([255,255,255])

            screen.blit(smallfont.render("Player "+str(active.value)+"'s turn", True, (0,0,0)),[5,0])
            screen.blit(smallfont.render("Eval: "+str(ai.eval.evaluate(table.boards)), True, (0,0,0)),[475,0])

            table.blitAll()
            if (table.globalWinner == misc.square.x or table.globalWinner == misc.square.o):
                screen.blit(smallfont.render("Player "+str(table.globalWinner.value)+" wins!", True, [0,0,0]),[5,630])
            
            pygame.display.flip()





            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    table.check()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        debug = not debug
                    if event.key == pygame.K_F2:
                        print(str(ai.eval.evaluate(table.boards)))


