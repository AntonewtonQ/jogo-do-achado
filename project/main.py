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

# Configuração do relógio para controle de FPS
clock = pygame.time.Clock()

# Carregar imagem do objeto para ser encontrado
try:
    object_img = pygame.image.load('object.png')
    object_img = pygame.transform.scale(object_img, (50, 50))
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    quit()

object_rect = object_img.get_rect()
object_rect.topleft = (random.randint(0, screen_width - object_rect.width),
                       random.randint(0, screen_height - object_rect.height))

# Configuração do personagem
player_size = 40
player_speed = 5
player_color = blue
player_rect = pygame.Rect(100, screen_height - player_size - 100, player_size, player_size)

# Configuração dos obstáculos
num_obstacles = 5
obstacle_size = 50
obstacles = []

def generate_obstacles():
    global obstacles
    obstacles = []
    for _ in range(num_obstacles):
        obstacle_rect = pygame.Rect(
            random.randint(0, screen_width - obstacle_size),
            random.randint(0, screen_height - obstacle_size),
            obstacle_size, obstacle_size
        )
        # Garantir que os obstáculos não fiquem em cima do objeto ou do jogador
        while obstacle_rect.colliderect(object_rect) or obstacle_rect.colliderect(player_rect):
            obstacle_rect.topleft = (
                random.randint(0, screen_width - obstacle_size),
                random.randint(0, screen_height - obstacle_size)
            )
        obstacles.append(obstacle_rect)

# Fontes
font = pygame.font.SysFont(None, 55)



def message_display(text, color, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Função para desenhar o cenário
def draw_scene():
    # Fundo do cenário
    screen.fill(white)
    
    # Desenhando um "chão"
    pygame.draw.rect(screen, green, (0, screen_height - 100, screen_width, 100))
    
    # Desenhando uma mesa
    pygame.draw.rect(screen, brown, (300, 400, 200, 50))
    
    # Desenhando uma caixa em cima da mesa
    pygame.draw.rect(screen, gray, (350, 370, 100, 30))

def menu_screen():
    running = True
    while running:
        draw_scene()
        message_display("Pressione ENTER para começar", black, 30, 250, 300)  # Adicionamos o tamanho e as coordenadas aqui
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_screen()

        pygame.display.update()
        clock.tick(60)


def game_over_screen(score):
    running = True
    while running:
        draw_scene()
        message_display(f"Game Over!", red, 40, 250, 200)  # Ajuste as coordenadas conforme necessário
        message_display(f"Pontuação: {score}", red, 30, 250, 250)
        message_display("Pressione ENTER para voltar ao menu", red, 30, 250, 300)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_screen()

        pygame.display.update()
        clock.tick(60)


# Função para exibir pontuação na tela
def show_score(score):
    score_surface = font.render(f"Pontuação: {score}", True, black)
    screen.blit(score_surface, (10, 10))

# Função para tela do jogo
def game_screen():
    global object_rect, player_rect
    object_rect.topleft = (random.randint(0, screen_width - object_rect.width),
                           random.randint(0, screen_height - object_rect.height))
    generate_obstacles()
    score = 0
    running = True
    while running:
        draw_scene()
        screen.blit(object_img, object_rect.topleft)
        pygame.draw.rect(screen, player_color, player_rect)

        # Desenhar obstáculos
        for obstacle in obstacles:
            pygame.draw.rect(screen, red, obstacle)

        # Exibir pontuação
        show_score(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Movimentação do personagem
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
            score += 10  # Incrementar pontuação
            object_rect.topleft = (random.randint(0, screen_width - object_rect.width),
                                   random.randint(0, screen_height - object_rect.height))
            generate_obstacles()  # Recriar obstáculos

        # Verificação de colisão com obstáculos
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                game_over_screen(score)

        pygame.display.update()
        clock.tick(60)

# Função principal para alternar entre telas
def main():
    menu_screen()

# Executa o jogo
if __name__ == "__main__":
    main()
