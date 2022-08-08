import sys
import matplotlib.pyplot as plt

MAX_STATIC_VALUE = 10000
MIN_STATIC_VALUE = -10000

def neighbors(location):
    switcher = {
        0:[1,2,15],#a0 : [g0,b1,a6]
        1:[0,3,8],#g0 : [a0,f1,g3]
        2:[0,3,4,12],#b1 : [a0,f1,c2,b5]
        3:[1,2,5,7],#f1 : [g0,b1,e2,f3]
        4:[2,5,9],#c2 : [b1,e2,c4]
        5:[3,4,6],#e2 : [f1,c2,e3]
        6:[5,7,11],#e3 : [e2,f3,e4]
        7:[3,6,8,14],#f3 : [f1,e3,g3,f5]
        8:[1,7,17],#g3 : [g0,f3,g6]
        9:[4,10,12],#c4 : [c2,d4,b5]
        10:[9,11,13],#d4 : [c4,e4,d5] 
        11:[6,10,14],#e4 : [e3,d4,f5]
        12:[2,9,13,15],#b5 : [b1,c4,d5,a6]
        13:[10,12,14,16],#d5 : [d4,b5,f5,]
        14:[7,11,13,17],#f5 : [f3,e4,d5,g6]
        15:[0,12,16],#a6 : [a0,b5,d6]
        16:[13,15,17],#d6 : [d5,a6,g6]
        17:[8,14,16]#g6 : [g3,f5,d6]
    }

    return switcher.get(location,[])

# close mill checker
def closeMill(location,board):
    C = board[location] # get color of current board location
    switcher = {
       #a0 
       0: True if board[2] == C and board[4] == C else False,
       #g0
       1: True if (board[3] == C and board[5] == C) or (board[8] == C and board[17] == C) else False,
       #b1
       2: True if board[0] == C and board[4] == C else False,
       #f1
       3: True if (board[1] == C and board[5] == C) or (board[7] == C and board[14] == C) else False,
       #c2
       4: True if board[0] == C and board[2] == C else False,
       #e2
       5: True if (board[1] == C and board[3] == C) or (board[6] == C and board[11] == C) else False,
       #e3
       6: True if (board[5] == C and board[11] == C) or (board[7] == C and board[8] == C) else False,
       #f3
       7: True if (board[6] == C and board[8] == C) or (board[3] == C and board[14] == C) else False ,
       #g3
       8: True if (board[1] == C and board[17] == C) or (board[6] == C and board[7] == C) else False,
       #c4
       9: True if (board[10] == C and board[11] == C) or (board[12] == C and board[15] == C) else False,
       #d4
       10: True if (board[9] == C and board[11] == C) or (board[13] == C and board[16] == C) else False,
       #e4
       11: True if (board[9] == C and board[10] == C) or (board[5] == C and board[6] == C) or (board[14] == C and board[17] == C) else False,
       #b5
       12: True if (board[9] == C and board[15] == C) or (board[13] == C and board[14] == C) else False,
       #d5
       13: True if (board[12] == C and board[14] == C) or (board[10] == C and board[16] == C) else False,
       #f5
       14: True if (board[12] == C and board[13] == C) or (board[3] == C and board[7] == C) or (board[11] == C and board[17] == C) else False,
       #a6
       15: True if (board[16] == C and board[17] == C) or(board[9] == C and board[12] == C) else False,
       #d6
       16: True if (board[15] == C and board[17] == C) or (board[10] == C and board[13] == C) else False,
       #g5
       17: True if (board[15] == C and board[16] == C) or (board[1] == C and board[8] == C) or (board[11] == C and board[14] == C) else False
    }

    return switcher.get(location,False)

def generateRemove(board,curList):
    allBlackInMill = True
    for i in range(len(board)):
        if board[i] == 'B':
            if not closeMill(i,board):
                copyBoard = board.copy()
                copyBoard[i] = 'x'
                curList.append(copyBoard)
                allBlackInMill = False
    if allBlackInMill == True:
        curList.append(board)
        
def generateHopping(board):
    outputList = []
    for i in range(len(board)):
        if board[i] == 'W':
            for j in range(len(board)):
                if board[j] == 'x':
                    copyBoard = board.copy()
                    copyBoard[i] = 'x'
                    copyBoard[j] = 'W'
                    if closeMill(j,copyBoard):
                        generateRemove(copyBoard,outputList)
                    else:
                        outputList.append(copyBoard)
    return outputList

def generateMove(board):
    outputList = []
    for i in range(len(board)):
        if board[i] == 'W':
            nbs = neighbors(i)
            for j in nbs:
                if board[j] == 'x':
                    copyBoard = board.copy()
                    copyBoard[i] = 'x'
                    copyBoard[j] = 'W'
                    if closeMill(j,copyBoard):
                        generateRemove(copyBoard,outputList)
                    else:
                        outputList.append(copyBoard)
    return outputList

def getPieceCount(board,piece):
    count = 0
    for i in range(len(board)):
        if board[i] == piece:
            count = count + 1
    return count

#swap pieces on board
def swapPieces(board):
    copyBoard = board.copy()
    for i in range(len(copyBoard)):
        if copyBoard[i] == 'W':
            copyBoard[i] = 'B'
        elif copyBoard[i] == 'B':
            copyBoard[i] = 'W'
    return copyBoard       

def generateMovesMidgameEndgame(board):
    count = getPieceCount(board,'W')
    if count == 3:
        return generateHopping(board)
    else:
        return generateMove(board)

def getStaticEstForMidgameEndgame(board):
    blackCount = getPieceCount(board,'B')
    if blackCount <= 2:
        return MAX_STATIC_VALUE
    whiteCount = getPieceCount(board,'W')
    if whiteCount <= 2:
        return MIN_STATIC_VALUE  
    swapedBoard = swapPieces(board)
    blackMoves = len(generateMovesMidgameEndgame(swapedBoard))
    if blackMoves == 0:
        return MAX_STATIC_VALUE
    return 1000*(whiteCount - blackCount) - blackMoves

#Solution helper class
class Solution:
  def __init__(self, val, state):
    self.val = val
    self.state = state
    
def maxMin(board,height,staticEst,generateMoves,staticEstCounter)->Solution:
    solution = []
    if height == 0:
        staticEstCounter[0] = staticEstCounter[0] + 1
        return Solution(staticEst(board),board)
    else:
        v = -float('inf')
        openingMoves = generateMoves(board)
        for i in range(len(openingMoves)):
            minMaxVal=minMax(openingMoves[i],height-1,staticEst,generateMoves,staticEstCounter)
            if minMaxVal.val > v:
                v = minMaxVal.val
                solution = openingMoves[i]
        return Solution(v,solution)

def minMax(board,height,staticEst,generateMoves,staticEstCounter)->Solution:
    solution = []
    if height == 0:
        staticEstCounter[0] = staticEstCounter[0] + 1
        return Solution(staticEst(board),board)
    else:
        v = float('inf')
        swapedBoard = swapPieces(board)
        openingMoves = generateMoves(swapedBoard)
        for i in range(len(openingMoves)):
            reSwapBoard = swapPieces(openingMoves[i])
            maxMinVal=maxMin(reSwapBoard,height-1,staticEst,generateMoves,staticEstCounter)
            if maxMinVal.val < v:
                v = maxMinVal.val
                solution = reSwapBoard
        return Solution(v,solution)   

def plotBoard(board,ax):
    origpoints = [[-15,-15],[15,-15],[-10,-10],[10,-10],[-5,-5],[5,-5],[5,0],[10,0],[15,0],[-5,5],[0,5],[5,5],[-10,10],[0,10],[10,10],[-15,15],[0,15],[15,15]]
    lines = [[[-15,15],[15,15]],[[-10,10],[10,10]],[[-5,5],[5,5]],[[5,0],[15,0]],[[-5,-5],[5,-5]],[[-10,-10],[10,-10]],[[-15,-15],[15,-15]],
    [[-15,-15],[-15,15]],[[-10,-10],[-10,10]],[[-5,-5],[-5,5]],[[0,5],[0,15]],[[5,5],[5,-5]],[[10,10],[10,-10]],[[15,15],[15,-15]],
    [[5,5],[15,15]],[[-5,-5],[-15,-15]],[[-5,5],[-15,15]],[[5,-5],[15,-15]]]
    points = []
    pValues = [] 
    for i in range(len(board)):
        if board[i] == 'W' or board[i] == 'B':
            points.append(origpoints[i])  
            pValues.append(board[i])  
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    colors = ['white' if c=='W' else 'black' for c in pValues]
    ax.set_facecolor("lightgray")
    for line in lines:
        ax.plot([line[0][0],line[1][0]],[line[0][1],line[1][1]],color='grey',linewidth=1)
    ax.scatter(xs, ys,color = colors,marker="8",s=200) 

if __name__ == "__main__":
    args = sys.argv
    height = int(args[3])
    inpFileName = args[1]
    outputFileName = args[2]
    inpFile = open(inpFileName,"r")
    inpLine = inpFile.readline()
    inpFile.close()
    inpBoard = []
    for i in range(len(inpLine)):
        inpBoard.append(inpLine[i])
    fig, ax = plt.subplots(1,2, figsize=(10, 5))         
    plotBoard(inpBoard,ax[0])
    staticEstCounter = [0]    
    res = maxMin(inpBoard,height,getStaticEstForMidgameEndgame,generateMovesMidgameEndgame,staticEstCounter)
    plotBoard(res.state,ax[1])   
    finalBoard = ''.join(res.state)
    print("Board Position: " + finalBoard)  
    print("Positions evaluated by static estimation: " + str(staticEstCounter[0]) + ".") 
    print("MINIMAX estimate: " + str(res.val) + ".")
    plt.savefig('moveMade.png')
    outfile = open(outputFileName, "w")
    outfile.write(finalBoard)
    outfile.close()
