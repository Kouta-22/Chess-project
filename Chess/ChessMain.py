import pygame as p
import ChessEngine

WIDTH = 640
HEIGHT = 512  # 400 is another option
BOARD_WIDTH = HEIGHT  # board is square
DIMENSION = 8  # dimensions of a chess board
SQ_SIZE = HEIGHT // DIMENSION
SIDE_PANEL = WIDTH - BOARD_WIDTH
MAX_FPS = 15  # for animations later on
IMAGES = {}

def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: We can access an image by saying 'IMAGES['wp']'

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag para quando o movimento for feito
    loadImages()  # carrega imagens uma vez
    running = True
    sqSelected = ()  # guarda a ultima casa selecionada (tupla: (linha, coluna))
    playerClicks = []  # guarda os cliques do jogador (duas tuplas: [(6,4), (4,4)])
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): # O jogador clicou na mesma casa duas vezes
                    sqSelected = () # deseleciona
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        if move.isPromotion:
                            promotedPiece = choosePromotionPiece(screen, gs.whiteToMove)

                            gs.board[move.endRow][move.endCol] = ('b' if gs.whiteToMove else 'w') + promotedPiece

                        moveMade = True
                        sqSelected = () # resetar selecao
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected] 
                # 
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # desfazer quando 'z' for pressionado
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()





def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares
    drawSidePanel(screen, gs)  # draw the side panel with captured pieces


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


if __name__ == "__main__":
    main()