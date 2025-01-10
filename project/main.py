import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo de Achado e Perdido")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
brown = (139, 69, 19)
green = (34, 139, 34)
gray = (169, 169, 169)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Configuração do relógio para controle de FPS
clock = pygame.time.Clock()

# Fontes
font_large = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

# Configuração do jogador
player_size = 40
player_speed = 5
player_color = blue
player_rect = pygame.Rect(100, screen_height - player_size - 100, player_size, player_size)

# Configuração do objeto a ser encontrado
object_size = 50
object_color = yellow
object_rect = pygame.Rect(
    random.randint(0, screen_width - object_size),
    random.randint(0, screen_height - object_size),
    object_size, object_size
)

# Configuração dos obstáculos
obstacle_size = 50
initial_obstacles = 5
obstacles = []

# Gerar obstáculos

def generate_obstacles(num_obstacles):
    global obstacles
    obstacles = []
    for _ in range(num_obstacles):
        obstacle_rect = pygame.Rect(
            random.randint(0, screen_width - obstacle_size),
            random.randint(0, screen_height - obstacle_size),
            obstacle_size, obstacle_size
        )
        # Garantir que os obstáculos não fiquem sobre o jogador ou o objeto
        while obstacle_rect.colliderect(player_rect) or obstacle_rect.colliderect(object_rect):
            obstacle_rect.topleft = (
                random.randint(0, screen_width - obstacle_size),
                random.randint(0, screen_height - obstacle_size)
            )
        obstacles.append(obstacle_rect)

# Função para exibir texto

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Função para o menu principal

def menu_screen():
    running = True
    while running:
        screen.fill(white)
        draw_text("Achado e Perdido", font_large, black, screen_width // 2, screen_height // 4)
        draw_text("1. Jogar", font_small, black, screen_width // 2, screen_height // 2 - 40)
        draw_text("2. Sair", font_small, black, screen_width // 2, screen_height // 2 + 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Jogar
                    game_screen()
                elif event.key == pygame.K_2:  # Sair
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(60)

# Função para o jogo

def game_screen():
    global object_rect, player_rect
    num_obstacles = initial_obstacles
    score = 0
    level = 1
    running = True
    generate_obstacles(num_obstacles)

    while running:
        screen.fill(white)

        # Desenhar elementos
        pygame.draw.rect(screen, green, (0, screen_height - 100, screen_width, 100))
        pygame.draw.rect(screen, object_color, object_rect)
        pygame.draw.rect(screen, player_color, player_rect)
        for obstacle in obstacles:
            pygame.draw.rect(screen, red, obstacle)

        # Exibir pontuação e nível
        draw_text(f"Pontuação: {score}", font_small, black, 100, 20)
        draw_text(f"Nível: {level}", font_small, black, 700, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
            player_rect.y += player_speed
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
            player_rect.x += player_speed

        # Verificação de colisão com o objeto
        if player_rect.colliderect(object_rect):
            score += 10
            level += 1
            object_rect.topleft = (
                random.randint(0, screen_width - object_size),
                random.randint(0, screen_height - object_size)
            )
            num_obstacles += 1
            generate_obstacles(num_obstacles)

        # Verificação de colisão com obstáculos
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                game_over_screen(score, level)

        pygame.display.update()
        clock.tick(60)

# Função para tela de game over

def game_over_screen(score, level):
    running = True
    while running:
        screen.fill(white)
        draw_text("Game Over", font_large, red, screen_width // 2, screen_height // 4)
        draw_text(f"Pontuação: {score}", font_small, black, screen_width // 2, screen_height // 2 - 40)
        draw_text(f"Nível: {level}", font_small, black, screen_width // 2, screen_height // 2)
        draw_text("Pressione ENTER para voltar ao menu", font_small, black, screen_width // 2, screen_height // 2 + 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_screen()

        pygame.display.update()
        clock.tick(60)

# Executar o jogo
if __name__ == "__main__":
    menu_screen()
