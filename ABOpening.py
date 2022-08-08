import sys

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
        

def generateAdd(board):
    outputList = []
    for i in range(len(board)):
        if board[i] == 'x':
            copyBoard = board.copy()
            copyBoard[i] = 'W'
            if closeMill(i,copyBoard):
                generateRemove(copyBoard,outputList)
            else:
                outputList.append(copyBoard)
    return outputList
    
def generateMovesOpening(board):
    return generateAdd(board)

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

def getStaticEstForOpening(board):
    blackCount = getPieceCount(board,'B')
    whiteCount = getPieceCount(board,'W')
    return whiteCount - blackCount

#Solution helper class
class Solution:
  def __init__(self, val, state):
    self.val = val
    self.state = state

def abMaxMin(board,alpha,beta,height,staticEst,generateMoves,staticEstCounter)->Solution:
    solution = []
    if height == 0:
        staticEstCounter[0] = staticEstCounter[0] + 1
        return Solution(staticEst(board),board)
    else:
        v = -float('inf')
        openingMoves = generateMoves(board)
        for i in range(len(openingMoves)):
            minMaxVal=abMinMax(openingMoves[i],alpha,beta,height-1,staticEst,generateMoves,staticEstCounter)
            if minMaxVal.val > v:
                v = minMaxVal.val
                solution = openingMoves[i]
            if v >= beta:
                return Solution(v,solution)
            else:
                alpha = max(v,alpha) 
        return Solution(v,solution)

def abMinMax(board,alpha,beta,height,staticEst,generateMoves,staticEstCounter)->Solution:
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
            maxMinVal=abMaxMin(reSwapBoard,alpha,beta,height-1,staticEst,generateMoves,staticEstCounter)
            if maxMinVal.val < v:
                v = maxMinVal.val
                solution = reSwapBoard
            if v <= alpha:
                return Solution(v,solution)
            else:
                beta = min(v,beta)        
        return Solution(v,solution)

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
    staticEstCounter = [0]   
    res = abMaxMin(inpBoard,-float('inf'),float('inf'),height,getStaticEstForOpening,generateMovesOpening,staticEstCounter)  
    finalBoard = ''.join(res.state)
    print("Board Position: " + finalBoard)  
    print("Positions evaluated by static estimation: " + str(staticEstCounter[0]) + ".") 
    print("MINIMAX estimate: " + str(res.val) + ".")
    outfile = open(outputFileName, "w")
    outfile.write(finalBoard)
    outfile.close() 
