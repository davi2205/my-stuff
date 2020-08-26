
'''

    Blockbreaker Básico em Pygame
    Autor: Davi Villalva
     Data: 2018
     Nota: Provavelmente vou misturar inglês com português nessa bagaça por força do hábito.
           Esta implementação não está nem um pouco otimizada e nem pretendo otimizar.

'''

# Importa a biblioteca Pygame
import pygame
# Importa as constantes úteis (QUIT, KEYDOWN, etc)
from pygame.locals import *

# Outras bibliotecas
from random import random
from math import sqrt

# Inicia o módulo Pygame e o submódulo Font para renderizar (desenhar) texto
pygame.init()
pygame.font.init()

# Variáveis de configuração do Jogo
tela_largura = 480
tela_altura  = 480
fonte_padrao = pygame.font.SysFont("Comic Sans MS", 16)
cor_fundo    = (  0,   0,   0)
cor_padrao   = (255, 255, 255)

# Quanto maior o índice do tijolo na lista, maior a quantidade de vezes que é preciso
# bater nele para quebrar (é a 'vida' do tijolo)
cores_tijolo = [
    (255,   0,  0), # tijolo com vida 1
    (255,  50,  0), # tijolo com vida 2
    (255, 100,  0), # tijolo com vida 3
    (255, 150,  0), # tijolo com vida 4
    (255, 200,  0), # tijolo com vida 5
    (255, 255,  0)  # tijolo com vida 6
]

# Cada elemento desta matriz corresponde a um índice da lista 'cores_tijolo'
mapa         = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 6, 6, 6, 6, 6, 6, 6, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 4, 4, 4, 4, 4, 4, 4, 0 ],
    [ 0, 3, 3, 3, 3, 3, 3, 3, 0 ],
    [ 0, 2, 2, 2, 2, 2, 2, 2, 0 ],
    [ 0, 1, 1, 1, 1, 1, 1, 1, 0 ],
]

# Funções utilitárias

# Esta função põe 'x' entre os valores 'a' e 'b'
def limita(x, a, b):
    return max(a, min(b, x))

# Desenha texto em uma Surface do Pygame
def desenha_texto(surface, texto, pos, cor):
    surface.blit(fonte_padrao.render(texto, False, cor), pos)

# Classes do jogo

# O propósito dessa classe é puramente semântico
class Tamanho(object):
    def __init__(self, l, a):
        self.set(l, a)

    # Vou usar set pois é mais curto que 'definir'
    def set(self, l, a):
        self.largura = float(l)
        self.altura  = float(a)

# Classe pra representar vetores no espaço 2D
class Vet2(object):
    def __init__(self, x = 0.0, y = 0.0):
        self.set(x, y)

    def set(self, x, y):
        self.x = float(x)
        self.y = float(y)

    # Operações com vetores
    
    def __add__(self, o):
        return Vet2(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vet2(self.x - o.x, self.y - o.y)

    def __mul__(self, o):
        if isinstance(o, Vet2):
            return Vet2(self.x * o.x, self.y * o.y)
        else:
            return Vet2(self.x *   o, self.y *   o)

    def __div__(self, o):
        if isinstance(o, Vet2):
            return Vet2(self.x / o.x, self.y / o.y)
        else:
            return Vet2(self.x /   o, self.y /   o)

    # Compatibilidade com Python 3.x
    __truediv__  = __div__
    __floordiv__ = __div__

    def prod_escalar(self, o):
        return self.x * o.x + self.y * o.y
    
    def get_tamanho(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def set_tamanho(self, t):
        return self.get_forma_normal() * t

    def get_forma_normal(self):
        t = self.get_tamanho()
        return Vet2(self.x / t, self.y / t)

    def reflete(self, normal):
        dn = self.prod_escalar(normal)
    
        if dn >= 0.0:
            return self

        # v = d - 2 (d * n) * n
        return self - (normal * 2.0 * dn)

# Estado global do jogo
class Estado(object):
    def __init__(self):
        self.saiu                 = False
        self.esquerda_pressionada = False
        self.direita_pressionada  = False
        self.cima_pressionado     = False
        self.baixo_pressionado    = False
        self.pontos               = 0

    def recebe_evento(self, evento):
        if   evento.type == QUIT:
            self.saiu                     = True
        
        elif evento.type == KEYDOWN:
            if   evento.key == K_LEFT:
                self.esquerda_pressionada = True
            elif evento.key == K_RIGHT:
                self.direita_pressionada  = True
            elif evento.key == K_UP:
                self.cima_pressionado     = True
            elif evento.key == K_DOWN:
                self.baixo_pressionado    = True
            
        elif evento.type == KEYUP:
            if   evento.key == K_LEFT:
                self.esquerda_pressionada = False
            elif evento.key == K_RIGHT:
                self.direita_pressionada  = False
            elif evento.key == K_UP:
                self.cima_pressionado     = False
            elif evento.key == K_DOWN:
                self.baixo_pressionado    = False

class Cena2D(object):
    def __init__(self):
        self.objetos           = []
        self.objetos_a_remover = []

    def executa_logica(self, estado, delta_t):
        for obj in self.objetos:
            obj.executa_logica(estado, delta_t)

        # Enquanto houver objetos a remover, remove-os
        while len(self.objetos_a_remover) > 0:
            self.objetos.remove(self.objetos_a_remover.pop())

    def desenha(self, surface):
        for obj in self.objetos:
            obj.desenha(surface)

    def adiciona(self, obj):
        obj.cena = self
        self.objetos.append(obj)

    def remove(self, obj):
        self.objetos_a_remover.append(obj)

class Objeto2D(object):
    def __init__(self):
        self.pos        = Vet2()
        self.velocidade = Vet2()
        self.tamanho    = Tamanho(0, 0)
        self.cor        = cor_padrao
        self.solido     = True
        self.cena       = None

    def executa_logica(self, estado, delta_t):
        self.pos += self.velocidade * delta_t

    def desenha(self, surface):
        pygame.draw.rect(surface,                          \
                         self.cor,                         \
                         pygame.Rect(self.pos.x,           \
                                     self.pos.y,           \
                                     self.tamanho.largura, \
                                     self.tamanho.altura))

class Player(Objeto2D):
    def __init__(self):
        super(Player, self).__init__()

        self.tamanho.set(80, 20)
        self.pos.set((tela_largura / 2) - (self.tamanho.largura / 2),
                      tela_altura - 80)

        # Velocidade e medida em pixels/segundo
        self.velocidade_escalar = 500
    
    def executa_logica(self, estado, delta_t):
        self.velocidade.set(0, 0)
        
        if estado.esquerda_pressionada:
            self.velocidade.x -= self.velocidade_escalar

        if estado.direita_pressionada:
            self.velocidade.x += self.velocidade_escalar

        self.pos.x = limita(self.pos.x, 0, tela_largura - self.tamanho.largura)

        super(Player, self).executa_logica(estado, delta_t)

class Bola(Objeto2D):
    def __init__(self):
        super(Bola, self).__init__()

        self.pos.set(tela_largura / 2, tela_altura - 100)
        self.tamanho.set(10, 10)

        self.velocidade = Vet2(random() * 2.0 - 1.0, -1).set_tamanho(400)

    def quica(self, obj):
        # Não vamos quicar a bola em algo não-sólido
        if not obj.solido:
            return False

        # Encontra o ponto de colisão entre o objeto retangular e a bolinha
        ponto = Vet2(limita(self.pos.x, obj.pos.x, obj.pos.x + obj.tamanho.largura),
                     limita(self.pos.y, obj.pos.y, obj.pos.y + obj.tamanho.altura))
        # Encontra o "delta" entre a posição da bola e o ponto de colisão
        # A forma normal desse "delta" é a normal de colisão
        delta = self.pos - ponto

        # Se o delta for maior que o raio da bolinha, não houve colisão
        if delta.get_tamanho() > self.tamanho.largura:
            return False

        # Faz a resposta da colisão (corrige a posição e reflete o vetor velocidade)
        try:
            normal          = delta.get_forma_normal()
            self.pos        = ponto + (normal * (self.tamanho.largura))
            self.velocidade = self.velocidade.reflete(normal)
        except ZeroDivisionError:
            pass

        return True

    def executa_logica(self, estado, delta_t):
        # Reflete a bolinha nos cantos da tela
        if self.pos.y - self.tamanho.largura <= 0.0:
            self.velocidade = self.velocidade.reflete(Vet2(0, 1))

        if self.pos.x - self.tamanho.largura <= 0.0:
            self.velocidade = self.velocidade.reflete(Vet2(1, 0))
        
        if self.pos.x >= tela_largura - self.tamanho.largura:
            self.velocidade = self.velocidade.reflete(Vet2(-1, 0))

        # Reseta a bolinha se ela cair na parte mais baixa da tela
        if self.pos.y >= tela_altura - self.tamanho.altura:
            self.pos.set(tela_largura / 2, tela_altura - 100)
            self.velocidade = Vet2(random() * 2.0 - 1.0, -1).set_tamanho(400)

        # Testa colisão com objetos na cena
        for obj in self.cena.objetos:
            if obj is not self:
                if self.quica(obj) and type(obj) is Tijolo:
                    obj.reduzir_vida()
                    estado.pontos += 50

        super(Bola, self).executa_logica(estado, delta_t)

    def desenha(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.pos.x), int(self.pos.y)), int(self.tamanho.largura))

class Tijolo(Objeto2D):
    def __init__(self, x, y, l, a, vida = 1):
        super(Tijolo, self).__init__()

        self.pos.set(x, y)
        self.tamanho.set(l, a)
        self.cor      = cores_tijolo[vida - 1]
        self.vida     = vida
        self.contador = -1

    def executa_logica(self, estado, delta_t):
        if self.contador > 0.0:
            self.contador -= delta_t

    def reduzir_vida(self):
        if self.contador > 0.0:
            return
        
        self.vida -= 1

        if self.vida <= 0:
            self.cena.remove(self)
        else:
            self.cor = cores_tijolo[self.vida - 1]

        self.contador = 0.5
        
class Pontuacao(Objeto2D):
    def __init__(self):
        super(Pontuacao, self).__init__()

        self.pos.set(10, tela_altura - 30)
        self.texto  = ''
        self.solido = False

    def executa_logica(self, estado, delta_t):
        self.texto = str(estado.pontos)

    def desenha(self, tela):
        desenha_texto(tela, self.texto, (int(self.pos.x), int(self.pos.y)), self.cor)


estado  = Estado()

cena    = Cena2D()
cena.adiciona(Player())
cena.adiciona(Bola())
cena.adiciona(Pontuacao())

cursor_x       = 5
cursor_y       = 10
tijolo_altura  = 20

# Cria os tijolinhos
for linha in mapa:
    tijolo_largura = (tela_largura + 5) / len(linha)
    
    for item in linha:
        if item > 0:
            cena.adiciona(Tijolo(cursor_x, cursor_y, tijolo_largura - 5, 20, item))

        cursor_x += tijolo_largura

    cursor_x  = 5
    cursor_y += tijolo_altura + 5

tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("BlockBreaker em PyGame")

ultimo_tempo = pygame.time.get_ticks() / 1000.0

while 1:
    for evento in pygame.event.get():
        estado.recebe_evento(evento)

    if estado.saiu:
        break

    tempo_atual  = (pygame.time.get_ticks() / 1000.0)
    delta_t      = (tempo_atual - ultimo_tempo)
    ultimo_tempo =  tempo_atual

    # a variável delta_t é necessária para calcular a velocidade instantânea dos objetos
    # velocidade instantânea = delta_s / delta_t
    cena.executa_logica(estado, delta_t)

    tela.fill(cor_fundo)
    cena.desenha(tela)
    pygame.display.flip()

pygame.font.quit()
pygame.quit()

        
