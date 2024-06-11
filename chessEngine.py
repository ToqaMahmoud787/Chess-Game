class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunction ={'p': self.getPawnMoves, 'R':self.getRookMoves,'N':self.getKnightMoves,
                            'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}

        self.WhiteToMove = True
        self.MoveLog = []
        self.blackKingLocation=(7,4)
        self.whiteKingLocation=(0,4)
        self.checkMate=False
        self.staleMate=False
        self.currentCastlingRight= castleRight(True, True,True,True)
        self.castleRightLog=[castleRight(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                         self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]
   
   
    def makeMove (self, move):
        self.board[move.startRow][move.startcol] = "--"
        self.board[move.endRow][move.endcol]=move.pieceMoved
        self.MoveLog.append(move)# Log the move so we can undo it later 
        self.WhiteToMove =not self.WhiteToMove #Aswap players
        #update the king's location
        if move.pieceMoved=='wK':
            self.whiteKingLocation=(move.endRow,move.endcol)
        elif move.pieceMoved=='bK':
            self.blackKingLocation=(move.endRow,move.endcol)   
        
        
        #pawn promot
        if move.isPawnPromotion:
            self.board[move.endRow][move.endcol]=move.pieceMoved[0] + 'Q'
       
       #castle move
        if move.isCastleMove:
            if move.endcol - move.startcol == 2:
                self.board[move.endRow][move.endcol-1] = self.board[move.endRow][move.endcol+1]  #moves the rock
                self.board[move.endRow][move.endcol+1]='--'
            else:
                self.board[move.endRow][move.endcol+1] = self.board[move.endRow][move.endcol-2] #moves the rock
                self.board[move.endRow][move.endcol-2]='--'
       
       
       
       
      # update castle right
        self.updateCastleRight(move)
        self.castleRightLog=[castleRight(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                         self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]
        
        
    def undoMove(self):
        if len(self.MoveLog) != 0:
            move = self.MoveLog.pop()
        self.board[move.startRow][move.startcol] = move.pieceMoved  
        self.board[move.endRow][move.endcol] = move.pieceCaptured
        self.WhiteToMove = not self.WhiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.startRow, move.startcol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.startRow, move.startcol)
        
        # Undo Right Castle move
        if len(self.castleRightLog) > 0:
            self.castleRightLog.pop()
            if len(self.castleRightLog) > 0:
                self.currentCastlingRight = self.castleRightLog[-1]
            else:
                # If the list is empty, create a new castleRight instance
                self.currentCastlingRight = castleRight(True, True, True, True)
                
        if move.isCastleMove:
            if move.endcol - move.startcol == 2:
                self.board[move.endRow][move.endcol+1] = self.board[move.endRow][move.endcol-1] 
                self.board[move.endRow][move.endcol-1] = '--'
            else:  
                self.board[move.endRow][move.endcol-2] = self.board[move.endRow][move.endcol+1] 
                self.board[move.endRow][move.endcol+1] = '--'

        self.checkMate=False
        self.staleMate=False     
                       
                
               
               
               
    def updateCastleRight(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
      
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startcol == 0:# left rook
                    self.currentCastlingRight.wqs = False
                
            
        elif move.startcol == 7:# right rook
            self.currentCastlingRight.wks = False
                
            
        
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startcol == 0:
                    self.currentCastlingRight.bqs = False
        
             
                
                elif move.startcol == 7:
                    self.currentCastlingRight.bks = False
                

                    
            
            

    def getValidMoves(self):
        tempCastleRights = castleRight(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                         self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)
        
        
        #1)generate all possible moves
        moves=self.getAllPossibleMoves()
        if self.WhiteToMove:
            self.getCastleMove(self.whiteKingLocation[0],self.whiteKingLocation[1],moves)
        else:
            self.getCastleMove(self.blackKingLocation[0],self.blackKingLocation[1],moves)
        #2)for each move make a move
        for i in range(len(moves)-1, -1, -1):#when removing from a list go backwa though that list
            self.makeMove(moves[i])
        #3)generate all openents moves
        #4)for each of the openents moves see if the they attack your king
            self.WhiteToMove=not self.WhiteToMove #switch turn back 
            if self.inCheck():
               moves.remove(moves[i])
         
        #5)if they do attack on your king its not a valid move
            self.WhiteToMove=not self.WhiteToMove #switch turn back 
            self.undoMove()  
        
        if len(moves)==0:
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate=True    
        else:
            self.checkMate=False
            self.staleMate=False  
        
        self.currentCastlingRight = tempCastleRights
        return moves
    
    
   #determine if the current playes is in check  
      
    def inCheck(self):
        if self.WhiteToMove:
             return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
             return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
                  
    
    
    #determine if the enemy can attack this square
    def squareUnderAttack(self,r,c):
        self.WhiteToMove=not self.WhiteToMove #switch to ur oppenents turn 
        oppMoves=self.getAllPossibleMoves()
        self.WhiteToMove=not self.WhiteToMove #switch turn back     
        for move in oppMoves:
            if move.endRow==r and move.endcol==c: #square is under attack 
                return True               
        return False         
     
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if(turn=='w' and self.WhiteToMove)or(turn=='b'and not self.WhiteToMove):
                    piece=self.board[r][c][1]
                    self.moveFunction[piece](r,c,moves) 
        return moves
     
    def getPawnMoves(self,r,c,moves):
         if self.WhiteToMove: #white pawn moves
             if self.board[r-1][c]=="--": #1 square pawn advance
                 moves.append(Move((r,c),(r-1,c),self.board))
                 if r==6 and self.board[r-2][c]=="--":  #2 square pawn advance
                     moves.append(Move((r,c),(r-2,c),self.board))
             if c-1>=0: #capture to the left
                 if self.board[r-1][c-1][0]=='b': #enemy piece to capture
                     moves.append(Move((r,c),(r-1,c-1),self.board))
              
 
             if c+1 <= 7: #capture to the right
                 if self.board[r-1][c+1][0]=='b':
                     moves.append(Move((r,c),(r-1,c+1),self.board))
                   

         else: #black pawn moves
             if self.board[r+1][c]=="--": #1 square pawn advance
                 moves.append(Move((r,c),(r+1,c),self.board))
                 if r==1 and self.board[r+2][c]=="--":  #2 square pawn advance
                     moves.append(Move((r,c),(r+2,c),self.board))
             if c-1>=0: #capture to the left
                 if self.board[r+1][c-1][0]=='w': #enemy piece to capture
                     moves.append(Move((r,c),(r+1,c-1),self.board))
                 
             if c+1 <= 7: #capture to the right
                 if self.board[r+1][c+1][0]=='w':
                     moves.append(Move((r,c),(r+1,c+1),self.board))
                     

             
                     
                 
    def getRookMoves(self,r,c,moves):
         directions=((-1,0),(0,-1),(1,0),(0,1)) #up,left,right,down
         enemyColor="b" if self.WhiteToMove else "w"
         for d in directions:
             for i in range(1,8):
                 endRow = r + d[0] * i
                 endCol = c + d[1] * i
                 if 0 <= endRow <8 and 0 <= endCol <8 :
                     endpiece = self.board[endRow][endCol]
                     if endpiece =="--":
                         moves.append(Move((r,c),(endRow,endCol),self.board))
                     elif endpiece[0]== enemyColor: #enemy piece invalid
                         moves.append(Move((r,c),(endRow,endCol),self.board))
                         break
                     else: #friendly piece invalid
                         break
                 else: #off board
                     break
               
    
    def getKnightMoves(self,r,c,moves):
         KnightMoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
         allyColor = "w" if self.WhiteToMove else "b"
         for m in KnightMoves:
             endRow= r + m[0]
             endCol= c + m[1]
             if 0 <= endRow <8 and 0 <= endCol <8 :
                 endpiece = self.board[endRow][endCol]
                 if endpiece[0]!= allyColor:
                     moves.append(Move((r,c),(endRow,endCol),self.board))


    
    def getBishopMoves(self,r,c,moves):
         directions=((-1,-1),(-1,1),(1,-1),(1,1)) #4 diagnols
         enemyColor="b" if self.WhiteToMove else "w"
         for d in directions:
             for i in range(1,8):
                 endRow = r + d[0] * i
                 endCol = c + d[1] * i
                 if 0 <= endRow <8 and 0 <= endCol <8 :
                     endpiece = self.board[endRow][endCol]
                     if endpiece =="--":
                         moves.append(Move((r,c),(endRow,endCol),self.board))
                     elif endpiece[0]== enemyColor: #enemy piece invalid
                         moves.append(Move((r,c),(endRow,endCol),self.board))
                         break
                     else: #friendly piece invalid
                         break
                 else: #off board
                     break
                              
    
    def getQueenMoves(self,r,c,moves):
         self.getRookMoves(r,c,moves)
         self.getBishopMoves(r,c,moves)    
    
    def getKingMoves(self,r,c,moves):
         kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
         allyColor= "w" if self.WhiteToMove else "b"
         for i in range(8):
             endRow = r + kingMoves[i][0]
             endCol = c + kingMoves[i][1]
             if 0 <= endRow <8 and 0 <= endCol <8 :
                 endpiece = self.board[endRow][endCol]
                 if endpiece[0]!= allyColor:
                     moves.append(Move((r,c),(endRow,endCol),self.board))
        
                  
                     

    def getCastleMove(self, r , c , moves )  :
        
        if self.squareUnderAttack(r,c):
            return
        if (self.WhiteToMove and self.currentCastlingRight.wks) or (not self.WhiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMove(r, c, moves)

        if (self.WhiteToMove and self.currentCastlingRight.wqs) or (not self.WhiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMove( r , c , moves)
        
              
      
    def getKingSideCastleMove(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))
            


    def getQueenSideCastleMove(self, r, c, moves):
     if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
        if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
            moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))



    
      
      
class castleRight():
    def __init__(self,wks, bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs



class Move():
    
    rankToRows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in rankToRows.items()}
    filesToCols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFils={v:k for k ,v in filesToCols.items()}
    
    def __init__(self,startSq,endSq,board, isCastleMove= False) :
        self.startRow=startSq[0]
        self.startcol=startSq[1]
        self.endRow=endSq[0]    
        self.endcol=endSq[1]
        self.pieceMoved=board[self.startRow][self.startcol]
        self.pieceCaptured=board[self.endRow][self.endcol]
        self.isCastleMove=isCastleMove
        
        #pawn poromtion
        self.isPawnPromotion=False
        if(self.pieceMoved=='wp' and self.endRow==0) or (self.pieceMoved=='bp' and self.endRow==7):
            self.isPawnPromotion=True
        

         #enpassant 
        #self.isEnpassantMove=False
        #if self.pieceMoved[1]=='p'and (self.endRow,self.endcol)==enpassantPossible:
       
            
            
        self.moveID=self.startRow*1000 + self.startcol*100 + self.endRow*10 + self.endcol
        print(self.moveID)
    
    def __eq__(self,other):
        if isinstance(other,Move):
           return self.moveID==other.moveID 
        return False 
        
    def getChessNotation(self):
       return self.getRankFile(self.startRow, self.startcol) + self.getRankFile(self.endRow, self.endcol)
    
     
    def getRankFile(self, r, c):
      return self. colsToFils[c] + self.rowsToRanks[r]    
        