import pygame
from pygame import *
import random

# Configurações gerais
WINDONS_SIZE = (600, 600)
PIXEL_SIZE = 10
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)

# Função para criar comida em posição aleatória
def randon_on_grid():
    x = random.randint(0, WINDONS_SIZE[0] // PIXEL_SIZE - 1) * PIXEL_SIZE
    y = random.randint(0, WINDONS_SIZE[1] // PIXEL_SIZE - 1) * PIXEL_SIZE
    return (x, y)

# Função para detectar colisão
def colisao(pos1, pos2):
    return pos1 == pos2

# Função para detectar colisão com os limites da tela
def offlimits(pos):
    return not (0 <= pos[0] < WINDONS_SIZE[0] and 0 <= pos[1] < WINDONS_SIZE[1])

# Função para mostrar a tela inicial
def tela_inicial(screen):
    fonte = pygame.font.Font(None, 74)
    texto_titulo = fonte.render("Snake Game", True, VERDE)
    texto_instrucao = pygame.font.Font(None, 36).render("Pressione qualquer tecla para começar", True, BRANCO)

    while True:
        screen.fill(PRETO)
        screen.blit(texto_titulo, ((WINDONS_SIZE[0] - texto_titulo.get_width()) // 2, WINDONS_SIZE[1] // 3))
        screen.blit(texto_instrucao, ((WINDONS_SIZE[0] - texto_instrucao.get_width()) // 2, WINDONS_SIZE[1] // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                return  # Sai da função e começa o jogo

# Classe da Cobra
class Cobra:
    def __init__(self):
        self.snake_pos = [(250, 50), (260, 50), (270, 50)]
        self.snake_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        self.snake_surface.fill(BRANCO)
        self.direction = K_LEFT
        self.new_direction = self.direction

    def move(self):
        # Previne mudanças bruscas de direção
        if (self.new_direction == K_UP and self.direction != K_DOWN) or \
           (self.new_direction == K_DOWN and self.direction != K_UP) or \
           (self.new_direction == K_LEFT and self.direction != K_RIGHT) or \
           (self.new_direction == K_RIGHT and self.direction != K_LEFT):
            self.direction = self.new_direction

        for i in range(len(self.snake_pos) - 1, 0, -1):
            self.snake_pos[i] = self.snake_pos[i - 1]

        if self.direction == K_UP:
            self.snake_pos[0] = (self.snake_pos[0][0], self.snake_pos[0][1] - PIXEL_SIZE)
        elif self.direction == K_DOWN:
            self.snake_pos[0] = (self.snake_pos[0][0], self.snake_pos[0][1] + PIXEL_SIZE)
        elif self.direction == K_LEFT:
            self.snake_pos[0] = (self.snake_pos[0][0] - PIXEL_SIZE, self.snake_pos[0][1]) 
        elif self.direction == K_RIGHT:
            self.snake_pos[0] = (self.snake_pos[0][0] + PIXEL_SIZE, self.snake_pos[0][1])

        # Implementando o teletransporte da cobra
        self.snake_pos[0] = (
            self.snake_pos[0][0] % WINDONS_SIZE[0],  # Teleporta horizontalmente
            self.snake_pos[0][1] % WINDONS_SIZE[1]   # Teleporta verticalmente
        )
    
    def grow(self):
        # Adiciona um novo segmento à cobra
        self.snake_pos.append((-10, 0))

    def draw(self, screen):
        for pos in self.snake_pos:
            screen.blit(self.snake_surface, pos)

# Classe da Maçã
class Maca:
    def __init__(self):
        self.apple_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        self.apple_surface.fill(VERMELHO)
        self.apple_pos = randon_on_grid()
    
    def draw(self, screen):
        screen.blit(self.apple_surface, self.apple_pos)
    
    def reposition(self):
        self.apple_pos = randon_on_grid()

# Função para reiniciar o jogo
def restart_game(cobra, maca):
    cobra.snake_pos = [(250, 50), (260, 50), (270, 50)]
    cobra.direction = K_LEFT
    maca.reposition()

# Configuração inicial
pygame.init()
pygame.mixer.init()
som_comer = pygame.mixer.Sound('mordida.mp3')

screen = pygame.display.set_mode(WINDONS_SIZE)
pygame.display.set_caption("Snake")

cobra = Cobra()
maca = Maca()

# Mostrar a tela inicial
tela_inicial(screen)

# Loop principal do jogo
while True:
    screen.fill(PRETO)
    pygame.time.Clock().tick(15)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                cobra.new_direction = event.key

    cobra.move()

    if offlimits(cobra.snake_pos[0]) or any(colisao(cobra.snake_pos[0], pos) for pos in cobra.snake_pos[1:]):
        restart_game(cobra, maca)
        tela_inicial(screen)

    if colisao(maca.apple_pos, cobra.snake_pos[0]):
        cobra.grow()
        maca.reposition()
        som_comer.play()

    maca.draw(screen)
    cobra.draw(screen)
    
    pygame.display.update()
