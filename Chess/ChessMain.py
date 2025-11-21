import pygame as p
import ChessEngine
from Menu import showMainMenu,showEndGameMenu # ← ADICIONE ESTA LINHA

WIDTH = 640
HEIGHT = 512  # 400 is another option
BOARD_WIDTH = HEIGHT  # board is square
DIMENSION = 8  # dimensions of a chess board
SQ_SIZE = HEIGHT // DIMENSION
SIDE_PANEL = WIDTH - BOARD_WIDTH
MAX_FPS = 15  # for animations later on
IMAGES = {}
clock = p.time.Clock()

def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: We can access an image by saying 'IMAGES['wp']'

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Xadrez")
    loadImages()
    # Loop principal do programa
    while True:
        # Menu principal
        menu_choice = showMainMenu()
        
        if menu_choice == 'quit':
            break
            
        # Inicia um novo jogo
        clock = p.time.Clock()
        gs = ChessEngine.GameState()
        validMoves = gs.getValidMoves()
        moveMade = False
        sqSelected = ()
        playerClicks = []
        game_running = True
        
        # Loop do jogo
        while game_running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    game_running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    
                    if col >= DIMENSION:  # Clicou no painel lateral
                        continue
                        
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                        
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            gs.makeMove(move)
                            if move.isPromotion:
                                promotedPiece = choosePromotionPiece(screen, gs.whiteToMove)
                                gs.board[move.endRow][move.endCol] = ('b' if gs.whiteToMove else 'w') + promotedPiece
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
                            
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        gs.undoMove()
                        moveMade = True

            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False

            drawGameState(screen, gs, validMoves, sqSelected)
            clock.tick(MAX_FPS)
            p.display.flip()
            
            # Verifica fim de jogo
            if gs.checkMate or gs.staleMate or gs.draw:
                if gs.checkMate:
                    result = 'checkmate_black' if gs.whiteToMove else 'checkmate_white'
                elif gs.staleMate:
                    result = 'stalemate'
                else:
                    result = 'draw'
                
                end_choice = showEndGameMenu(screen, result)
                
                if end_choice == 'play_again':
                    # Reinicia o jogo
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    sqSelected = ()
                    playerClicks = []
                else:  # main_menu
                    game_running = False
    
    p.quit()

def drawGameState(screen, gs, validMoves, sqSelected,checkMate=False,staleMate=False,draw=False):



    drawBoard(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares
    drawSidePanel(screen, gs)  # draw the side panel with captured pieces


    if gs.checkMate:
        winner = "Pretas" if gs.whiteToMove else "Brancas"
        drawEndGameText(screen, f"Checkmate! {winner} vencem!")
    elif gs.staleMate:
        drawEndGameText(screen, "Empate por afogamento (Stalemate)!")
    elif gs.draw:
        drawEndGameText(screen, "Empate por material insuficiente!")

    clock.tick(MAX_FPS)
    p.display.flip()


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # sqSelected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawSidePanel(screen, gs):
    """
    Mostra as peças capturadas no painel lateral.
    """
    panel_x = BOARD_WIDTH
    p.draw.rect(screen, p.Color("lightgray"), p.Rect(panel_x, 0, SIDE_PANEL, HEIGHT))

    font = p.font.SysFont("Arial", 20, True)
    title_white = font.render("Pretas capturadas:", True, p.Color("black"))
    title_black = font.render("Brancas capturadas:", True, p.Color("black"))

    screen.blit(title_white, (panel_x + 5, 10))
    screen.blit(title_black, (panel_x + 5, HEIGHT // 2 + 10))

    # desenha as peças capturadas
    for i, piece in enumerate(gs.capturedWhitePieces):
        img = IMAGES[piece]
        screen.blit(img, (panel_x + 10 + (i % 2) * 40, 40 + (i // 2) * 40))

    for i, piece in enumerate(gs.capturedBlackPieces):
        img = IMAGES[piece]
        screen.blit(img, (panel_x + 10 + (i % 2) * 40, HEIGHT // 2 + 40 + (i // 2) * 40))





def choosePromotionPiece(screen, whiteToMove):
    """
    Exibe um menu simples para o jogador escolher a peça da promoção.
    Retorna 'Q', 'R', 'B' ou 'N'.
    """
    p.font.init()
    font = p.font.SysFont("Arial", 30, True)
    color = "white" if whiteToMove else "black"
    bg = p.Color("gray20")

    options = ["Q", "R", "B", "N"]
    running = True
    while running:
        screen.fill(bg)
        for i, piece in enumerate(options):
            label = font.render(f"Promover para: {piece}", True, p.Color("gold"))
            rect = label.get_rect(center=(WIDTH // 2, 150 + i * 60))
            screen.blit(label, rect)
        p.display.flip()

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                exit()
            elif e.type == p.KEYDOWN:
                if e.key == p.K_q:
                    return "Q"
                elif e.key == p.K_r:
                    return "R"
                elif e.key == p.K_b:
                    return "B"
                elif e.key == p.K_n:
                    return "N"
            elif e.type == p.MOUSEBUTTONDOWN:
                x, y = p.mouse.get_pos()
                for i, piece in enumerate(options):
                    if 130 + i * 60 <= y <= 170 + i * 60:
                        return piece

def drawEndGameText(screen, text):
    """
    Mostra uma mensagem centralizada no tabuleiro.
    """
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, True, p.Color("red"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - textObject.get_width() // 2,
                                                    HEIGHT // 2 - textObject.get_height() // 2)
    screen.blit(textObject, textLocation)
    # Adiciona uma sombra leve
    screen.blit(font.render(text, True, p.Color("black")),
                (textLocation.x + 2, textLocation.y + 2))







if __name__ == "__main__":
    main()