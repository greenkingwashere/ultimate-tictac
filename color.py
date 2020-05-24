import sys, os

def printColor(text, code=31, end="\n"):
    print("\033["+str(code)+"m"+text+"\033[00m", end=end)



def printException(e):
    """Print details about an exception object"""
    printColor(""+str(sys.exc_info()[0].__name__)+" in "+str(os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1])+" at line "+str(sys.exc_info()[2].tb_lineno)+"\n"+str(e), "1;37;41")