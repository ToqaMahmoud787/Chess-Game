import random

pieceScore = {"K" : 0, "Q" : 10,"R" : 5,"B" : 3,"N" : 3,"p" :1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[ random.randint(0, len(validMoves)- 1)]


# def findBestMove(gs,validMoves):
#    turnMultiplier = 1 if gs.WhiteToMove else -1
#    opponentMinMaxScore= CHECKMATE
#    bestPlayerMove = None
#    random.shuffle(validMoves)
#    for playerMove in validMoves:
#        gs.makeMove(playerMove)
#        opponentsMoves = gs.getValidMoves()
#        if gs.staleMate :
#            opponentMaxScore = STALEMATE
#        elif gs.checkMate:
#            opponentMaxScore = -CHECKMATE
#        else:
#            opponentMaxScore = -CHECKMATE
#        for opponentsMove in opponentsMoves:
#             gs.makeMove(opponentsMove)
#             #gs.getValidMoves()
#             if gs.checkMate:
#                 score = CHECKMATE
#             elif gs.staleMate:
#                 score =STALEMATE
#             else:
#                 score = -turnMultiplier * scoreMaterial(gs.board)
#             if score > opponentMaxScore:
#                 opponentMaxScore = score
#             gs.undoMove()
#        if   opponentMinMaxScore > opponentMaxScore:
#            opponentMinMaxScore = opponentMaxScore
#            bestPlayerMove = playerMove
#        gs.undoMove()
#    return bestPlayerMove

def findBestMove(gs , validMoves):
    global nextMove , counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    #findMoveMinMax(gs , validMoves ,DEPTH, gs.WhiteToMove )
    findMoveNegaMax(gs , validMoves , DEPTH , 1 if gs.WhiteToMove else -1)
    #findMoveNegaMaxAlphaBeta(gs , validMoves ,DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.WhiteToMove else -1 )
    print(counter)
    return nextMove




def findMoveMinMax(gs , validMoves ,depth , WhiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if WhiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs ,nextMoves ,depth-1 , not WhiteToMove )
            if score > maxScore:
                maxScore=score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore


    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs ,nextMoves ,depth-1 ,  WhiteToMove )
            if score <minScore:
                minScore=score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
    


def findMoveNegaMax(gs , validMoves , depth , turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth ==0:
        return turnMultiplier * scoreBoard(gs)
    

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs , nextMoves , depth-1 , -turnMultiplier)
        if score > maxScore:
            maxScore=score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore



def findMoveNegaMaxAlphaBeta(gs , validMoves , depth ,alpha , beta, turnMultiplier):
    global nextMove , counter
    counter+=1
    if depth ==0:
        return turnMultiplier * scoreBoard(gs)
    

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs , nextMoves , depth-1 ,-beta , -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore=score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
'''
a positive score is good for white , a negative score is goog for black
'''

def scoreBoard(gs):
    if gs.checkMate:
        if gs.WhiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.staleMate:
        return STALEMATE
    

    score=0
    for row in gs.board:
        for square in row:
            if square[0]=='w':
                score += pieceScore[square[1]]
            elif square[0]=='b':
                score -= pieceScore[square[1]]

    return score   

    

       


def scoreMaterial(board):
    score=0
    for row in board:
        for square in row:
            if square[0]=='w':
                score += pieceScore[square[1]]
            elif square[0]=='b':
                score -= pieceScore[square[1]]

    return score   