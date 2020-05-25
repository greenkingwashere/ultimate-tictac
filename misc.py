import sys, os




def printColor(text, code=31, end="\n"):
    """Prints text in color using ascii color codes, which can either be a string or an int
    31: red, 32: green, 33: yellow, 34: blue, 35: purple
    """
    print("\033["+str(code)+"m"+str(text)+"\033[00m", end=end)



def printException(e):
    """Print details about an exception object"""
    printColor(""+str(sys.exc_info()[0].__name__)+" in "+str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1])+" at line "+str(sys.exc_info()[2].tb_lineno)+"\n"+str(e), "1;37;41")

def printEval(num):
    text = "{0:.4f}".format(num)
    if (num == 1.0):
        printColor(text, "0;37;42")
    elif (num > 0):
        printColor(text, 32)
    elif (num == 0):
        print(str(text))
    elif (num > -1.0):
        printColor(text, 31)
    else:
        printColor(text, "0;37;41")

def printFile(filename):
    try:
        f = open(filename, 'r')
        for line in f:
            print(str(line))
        f.close()

    except FileNotFoundError:
        color.printColor(filename+" not found")