import pygame as p 
from chessEngine  import GameState
from chessEngine  import Move
from SmartMoveFinder import findRandomMove
from SmartMoveFinder import findBestMove
 
 

p.init()
WIDTH=HEIGHT=512
DIMENSION=8
SQ_SIZE= HEIGHT//DIMENSION
MAX_FPS=15
IMAGES={}

def loading_images():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) 
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves=gs.getValidMoves()
    moveMade=False
    animate = False
    print(gs.board)
    loading_images()
    running = True
    sqSelected=()#no square is selected , keep track of the last click of the user
    playerClicks=[]#keep track of player clicks  
    gameOver = False
    playerOne = False #if a Human playing white, then this will be True. if an AI is playing white, then it will be false
    playerTwo = True # same as above but for black
    while running:
        humanTurn = (gs.WhiteToMove and playerOne) or (not gs.WhiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type==p.MOUSEBUTTONUP:
                if not gameOver and humanTurn:
                    location=p.mouse.get_pos()
                    col=location[0]//SQ_SIZE
                    row=location[1]//SQ_SIZE 
                    if sqSelected==(row,col):#the user click the same square twice
                        sqSelected=()#deselected
                        playerClicks=[]#clear playe clicks
                    else:
                        sqSelected=(row,col)
                        playerClicks.append(sqSelected)#append foe both first and second clicks
                    if len(playerClicks)==2: #after 2 clicks 
                        move=Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(move)
                                moveMade=True
                                animate = True
                                sqSelected=()
                                playerClicks=[]
                        if not moveMade:
                            playerClicks = [sqSelected]
                       
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undoMove()  
                    moveMade=True   
                    animate = False
                    gameOver = False
                if    e.key == p.K_r:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        
        if not gameOver and not humanTurn:
            AIMove = findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
                    
               
        if moveMade:
            if animate:
                animateMove(gs.MoveLog[-1], screen, gs.board, clock)
                
            validMoves=gs.getValidMoves()
            moveMade = False  
            animate = False         
        drawGameState(screen,gs,validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.WhiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen,'white wins by checkmate')
        elif gs.staleMate:
            gameOver= True
            drawText(screen, 'StaleMatez')
        clock.tick(MAX_FPS)
        p.display.flip()
        
def highlightSquares(screen, gs, validMoves, sqSelected):
    
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.WhiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startcol == c:
                    screen.blit(s, (move.endcol * SQ_SIZE, move.endRow * SQ_SIZE))
                    
def drawGameState(screen,gs,validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen,gs, validMoves, sqSelected)
    drawPeices(screen,gs.board)
    
    
def drawBoard(screen):
    global colors
    colors= [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
    
    
def drawPeices(screen,board):
        for r in range(DIMENSION):
         for c in range (DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            


def animateMove (move, screen, board, clock):
    global colors
    
    dR = move.endRow - move.startRow
    dC = move.endcol - move.startcol
    
    framePerSquaer = 10
    frameCount = (abs(dR)+ abs(dC)) *framePerSquaer
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startcol + dC * frame / frameCount)
        drawBoard(screen)
        drawPeices(screen, board)
        
        color = colors[(move.endRow + move.endcol) % 2]
        endSquare = p.Rect(move.endcol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen,color, endSquare)
        
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured],endSquare)
            
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(110)    
         
def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0 , p.Color('Black'))
    textLocation = p.Rect(0, 0 , WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2,HEIGHT/2 - textObject.get_height()/2 )
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2,2))

       
if __name__=="__main__":
    main()    
    
    