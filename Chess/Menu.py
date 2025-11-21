import pygame as p
import sys

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BROWN = (139, 69, 19)
LIGHT_BROWN = (222, 184, 135)
GOLD = (255, 215, 0)

class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_BROWN, hover_color=GOLD):
        self.rect = p.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = p.font.SysFont("Arial", 32, True)
        
    def draw(self, screen):
        # Cor do botão (normal ou hover)
        color = self.hover_color if self.is_hovered else self.color
        
        # Desenha o botão
        p.draw.rect(screen, color, self.rect, border_radius=10)
        p.draw.rect(screen, DARK_BROWN, self.rect, 3, border_radius=10)
        
        # Texto do botão
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        """Verifica se o mouse está sobre o botão"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        """Verifica se o botão foi clicado"""
        return self.rect.collidepoint(mouse_pos) and mouse_click

def showMainMenu():
    """
    Exibe o menu principal
    Retorna: 'play' ou 'quit'
    """
    # Inicializa o Pygame se ainda não estiver inicializado
    if not p.get_init():
        p.init()
    
    # Configurações da tela (use as mesmas do seu jogo)
    WIDTH = 640
    HEIGHT = 512
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Xadrez - Menu Principal")
    
    # Fonte para o título
    title_font = p.font.SysFont("Arial", 64, True)
    subtitle_font = p.font.SysFont("Arial", 24, True)
    
    # Textos do título
    title_text = title_font.render("XADREZ", True, GOLD)
    subtitle_text = subtitle_font.render("Clássico Jogo de Estratégia", True, WHITE)
    
    # Cria os botões
    button_width = 200
    button_height = 60
    center_x = WIDTH // 2
    
    play_button = Button(
        center_x - button_width // 2, 
        HEIGHT // 2 - 30, 
        button_width, 
        button_height, 
        "JOGAR"
    )
    
    quit_button = Button(
        center_x - button_width // 2, 
        HEIGHT // 2 + 60, 
        button_width, 
        button_height, 
        "SAIR"
    )
    
    clock = p.time.Clock()
    
    # Loop principal do menu
    while True:
        mouse_pos = p.mouse.get_pos()
        mouse_clicked = False
        
        # Processa eventos
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    mouse_clicked = True
        
        # Verifica se o mouse está sobre os botões
        play_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        # Verifica cliques nos botões
        if play_button.is_clicked(mouse_pos, mouse_clicked):
            return 'play'
            
        if quit_button.is_clicked(mouse_pos, mouse_clicked):
            p.quit()
            sys.exit()
        
        # DESENHA TUDO NA TELA
        
        # Fundo
        screen.fill(DARK_BROWN)
        
        # Título
        screen.blit(title_text, (center_x - title_text.get_width() // 2, 120))
        screen.blit(subtitle_text, (center_x - subtitle_text.get_width() // 2, 200))
        
        # Botões
        play_button.draw(screen)
        quit_button.draw(screen)
        
        # Atualiza a tela
        p.display.flip()
        clock.tick(60)  # 60 FPS

def showEndGameMenu(screen, game_result):
    """
    Exibe o menu de fim de jogo
    game_result: string com o resultado - 'checkmate_white', 'checkmate_black', 'stalemate', 'draw'
    Retorna: 'play_again' ou 'main_menu'
    """
    WIDTH, HEIGHT = screen.get_size()
    
    # Fundo semi-transparente
    overlay = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Preto semi-transparente
    screen.blit(overlay, (0, 0))
    
    # Define os textos baseado no resultado
    title_font = p.font.SysFont("Arial", 48, True)
    message_font = p.font.SysFont("Arial", 24, True)
    
    if game_result == 'checkmate_white':
        title_text = title_font.render("CHECKMATE!", True, (255, 215, 0))  # Dourado
        message_text = message_font.render("Brancas vencem!", True, WHITE)
    elif game_result == 'checkmate_black':
        title_text = title_font.render("CHECKMATE!", True, (255, 215, 0))
        message_text = message_font.render("Pretas vencem!", True, WHITE)
    elif game_result == 'stalemate':
        title_text = title_font.render("AFOGAMENTO", True, (255, 215, 0))
        message_text = message_font.render("Empate!", True, WHITE)
    else:  # draw
        title_text = title_font.render("EMPATE", True, (255, 215, 0))
        message_text = message_font.render("Material insuficiente", True, WHITE)
    
    # Cria os botões
    button_width = 220
    button_height = 50
    center_x = WIDTH // 2
    
    play_again_button = Button(
        center_x - button_width // 2,
        HEIGHT // 2 + 20,
        button_width,
        button_height,
        "JOGAR NOVAMENTE"
    )
    
    main_menu_button = Button(
        center_x - button_width // 2,
        HEIGHT // 2 + 90,
        button_width,
        button_height,
        "MENU PRINCIPAL"
    )
    
    clock = p.time.Clock()
    
    # Loop do menu de fim de jogo
    while True:
        mouse_pos = p.mouse.get_pos()
        mouse_clicked = False
        
        # Processa eventos
        for event in p.event.get():
            if event.type == p.QUIT:
                return 'main_menu'
            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    mouse_clicked = True
            elif event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    return 'main_menu'
        
        # Verifica hover nos botões
        play_again_button.check_hover(mouse_pos)
        main_menu_button.check_hover(mouse_pos)
        
        # Verifica cliques
        if play_again_button.is_clicked(mouse_pos, mouse_clicked):
            return 'play_again'
        if main_menu_button.is_clicked(mouse_pos, mouse_clicked):
            return 'main_menu'
        
        # Desenha o menu de fim de jogo
        menu_bg = p.Rect(center_x - 200, HEIGHT // 2 - 120, 400, 300)
        p.draw.rect(screen, DARK_BROWN, menu_bg, border_radius=15)
        p.draw.rect(screen, GOLD, menu_bg, 3, border_radius=15)
        
        # Textos
        screen.blit(title_text, (center_x - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(message_text, (center_x - message_text.get_width() // 2, HEIGHT // 2 - 40))
        
        # Botões
        play_again_button.draw(screen)
        main_menu_button.draw(screen)
        
        p.display.flip()
        clock.tick(60)