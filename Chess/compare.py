def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    loadImages()  # carrega imagens uma vez

    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        drawGameState(screen, gs)  # desenha tabuleiro e peças
        clock.tick(MAX_FPS)
        p.display.flip()