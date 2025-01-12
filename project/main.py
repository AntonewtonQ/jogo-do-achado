import pygame
import random
import os

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
green = (34, 139, 34)
gray = (169, 169, 169)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Relógio para controle de FPS
clock = pygame.time.Clock()

# Carregar imagem do objeto
try:
    object_img = pygame.image.load('object.png')
    object_img = pygame.transform.scale(object_img, (50, 50))
except pygame.error:
    object_img = pygame.Surface((50, 50))
    object_img.fill(yellow)

object_rect = object_img.get_rect()

# Configuração do jogador
player_size = 40
player_speed = 5
player_rect = pygame.Rect(100, screen_height - player_size - 100, player_size, player_size)

# Configuração dos obstáculos
num_obstacles = 5
obstacle_size = 50
obstacles = []
obstacle_speeds = []

# Carregar sons
pygame.mixer.init()
try:
    collect_sound = pygame.mixer.Sound("collect.wav")
    collide_sound = pygame.mixer.Sound("collide.wav")
except pygame.error:
    collect_sound = collide_sound = None

# Pontuação máxima persistente
def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

high_score = load_high_score()

# Fontes
font = pygame.font.SysFont(None, 55)

# Função para exibir mensagem
def message_display(text, color, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Botão interativo
def button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    text_surface = pygame.font.Font(None, 35).render(text, True, black)
    text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surface, text_rect)

# Gerar obstáculos
def generate_obstacles(num):
    global obstacles, obstacle_speeds
    obstacles = []
    obstacle_speeds = []
    for _ in range(num):
        obstacle_rect = pygame.Rect(
            random.randint(0, screen_width - obstacle_size),
            random.randint(0, screen_height - obstacle_size),
            obstacle_size, obstacle_size
        )
        while obstacle_rect.colliderect(object_rect) or obstacle_rect.colliderect(player_rect):
            obstacle_rect.topleft = (
                random.randint(0, screen_width - obstacle_size),
                random.randint(0, screen_height - obstacle_size)
            )
        obstacles.append(obstacle_rect)
        obstacle_speeds.append((random.choice([-2, 2]), random.choice([-2, 2])))

# Tela de menu
def menu_screen():
    running = True
    while running:
        screen.fill(white)
        message_display("Jogo de Achado e Perdido", black, 60, screen_width // 2, 100)

        button("Iniciar", 300, 200, 200, 50, green, yellow, game_screen)
        button("Melhor Pontuação", 300, 300, 200, 50, gray, yellow, show_high_score)
        button("Sair", 300, 400, 200, 50, red, yellow, quit_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()
        clock.tick(60)

# Tela de pontuação máxima
def show_high_score():
    running = True
    while running:
        screen.fill(white)
        message_display("Melhor Pontuação", black, 60, screen_width // 2, 100)
        message_display(f"{high_score}", black, 50, screen_width // 2, 200)
        button("Voltar", 300, 400, 200, 50, gray, yellow, menu_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()
        clock.tick(60)

# Tela de game over
def game_over_screen(score):
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    running = True
    while running:
        screen.fill(white)
        message_display("Game Over!", red, 60, screen_width // 2, 150)
        message_display(f"Pontuação: {score}", black, 50, screen_width // 2, 250)
        message_display(f"Melhor Pontuação: {high_score}", black, 50, screen_width // 2, 300)
        button("Menu", 300, 400, 200, 50, green, yellow, menu_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.update()
        clock.tick(60)

# Tela do jogo
def game_screen():
    global object_rect, player_rect
    object_rect.topleft = (random.randint(0, screen_width - object_rect.width),
                           random.randint(0, screen_height - object_rect.height))
    level = 1
    score = 0
    paused = False
    generate_obstacles(num_obstacles)

    running = True
    while running:
        if paused:
            message_display("Pausado", black, 60, screen_width // 2, screen_height // 2)
        else:
            screen.fill(white)
            screen.blit(object_img, object_rect.topleft)
            pygame.draw.rect(screen, blue, player_rect)

            for i, obstacle in enumerate(obstacles):
                pygame.draw.rect(screen, red, obstacle)
                obstacle.x += obstacle_speeds[i][0]
                obstacle.y += obstacle_speeds[i][1]

                # Rebater nas bordas
                if obstacle.left < 0 or obstacle.right > screen_width:
                    obstacle_speeds[i] = (-obstacle_speeds[i][0], obstacle_speeds[i][1])
                if obstacle.top < 0 or obstacle.bottom > screen_height:
                    obstacle_speeds[i] = (obstacle_speeds[i][0], -obstacle_speeds[i][1])

            if player_rect.colliderect(object_rect):
                score += 10
                level += 1
                if collect_sound:
                    collect_sound.play()
                object_rect.topleft = (random.randint(0, screen_width - object_rect.width),
                                       random.randint(0, screen_height - object_rect.height))
                generate_obstacles(num_obstacles + level)

            for obstacle in obstacles:
                if player_rect.colliderect(obstacle):
                    if collide_sound:
                        collide_sound.play()
                    game_over_screen(score)

            # Controles do jogador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player_rect.top > 0:
                player_rect.y -= player_speed
            if keys[pygame.K_DOWN] and player_rect.bottom < screen_height:
                player_rect.y += player_speed
            if keys[pygame.K_LEFT] and player_rect.left > 0:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
                player_rect.x += player_speed

            message_display(f"Pontuação: {score}", black, 40, 100, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused

        pygame.display.update()
        clock.tick(60)

# Sair do jogo
def quit_game():
    pygame.quit()
    quit()

# Iniciar o jogo
if __name__ == "__main__":
    menu_screen()
