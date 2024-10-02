import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import time
import tkinter as tk
from tkinter import messagebox

# Configurações do jogo
TAMANHO_TABULEIRO = 3
TAMANHO_CELULA = 1.0
RAIO_ESFERA = 0.3

# Cores
BRANCO = (1, 1, 1)
VERMELHO = (1, 0, 0)
AZUL = (0, 0, 1)
VERDE = (0, 1, 0)
AMARELO = (1, 1, 0)
ROXO = (0.5, 0, 0.5)
CIANO = (0, 1, 1)
LARANJA = (1, 0.5, 0)
CIANO_BRILHANTE = (0, 1, 1)

# Elementos decorativos
NUM_ESTRELAS = 500
NUM_ASTEROIDES = 20

class JogoDaVelha3D:
    def __init__(self, profundidade_maxima=4):
        self.tabuleiro = [[[0 for _ in range(TAMANHO_TABULEIRO)] for _ in range(TAMANHO_TABULEIRO)] for _ in
                          range(TAMANHO_TABULEIRO)]
        self.jogador_atual = 1
        self.jogo_terminado = False
        self.vencedor = None
        self.profundidade_maxima = profundidade_maxima
        self.linha_vitoria = None
        self.placar_jogador = 0
        self.placar_ia = 0

    def fazer_jogada(self, x, y, z, jogador):
        if 0 <= x < TAMANHO_TABULEIRO and 0 <= y < TAMANHO_TABULEIRO and 0 <= z < TAMANHO_TABULEIRO and \
                self.tabuleiro[x][y][z] == 0:
            self.tabuleiro[x][y][z] = jogador
            return True
        return False

    def desfazer_jogada(self, x, y, z):
        self.tabuleiro[x][y][z] = 0

    def verificar_vencedor(self, jogador):
        for i in range(TAMANHO_TABULEIRO):
            for j in range(TAMANHO_TABULEIRO):
                if all(self.tabuleiro[i][j][k] == jogador for k in range(TAMANHO_TABULEIRO)):
                    self.linha_vitoria = [(i, j, 0), (i, j, TAMANHO_TABULEIRO - 1)]
                    return True
                if all(self.tabuleiro[i][k][j] == jogador for k in range(TAMANHO_TABULEIRO)):
                    self.linha_vitoria = [(i, 0, j), (i, TAMANHO_TABULEIRO - 1, j)]
                    return True
                if all(self.tabuleiro[k][i][j] == jogador for k in range(TAMANHO_TABULEIRO)):
                    self.linha_vitoria = [(0, i, j), (TAMANHO_TABULEIRO - 1, i, j)]
                    return True

        if all(self.tabuleiro[i][i][i] == jogador for i in range(TAMANHO_TABULEIRO)):
            self.linha_vitoria = [(0, 0, 0), (TAMANHO_TABULEIRO - 1, TAMANHO_TABULEIRO - 1, TAMANHO_TABULEIRO - 1)]
            return True
        if all(self.tabuleiro[i][i][TAMANHO_TABULEIRO - 1 - i] == jogador for i in range(TAMANHO_TABULEIRO)):
            self.linha_vitoria = [(0, 0, TAMANHO_TABULEIRO - 1), (TAMANHO_TABULEIRO - 1, TAMANHO_TABULEIRO - 1, 0)]
            return True
        if all(self.tabuleiro[i][TAMANHO_TABULEIRO - 1 - i][i] == jogador for i in range(TAMANHO_TABULEIRO)):
            self.linha_vitoria = [(0, TAMANHO_TABULEIRO - 1, 0), (TAMANHO_TABULEIRO - 1, 0, TAMANHO_TABULEIRO - 1)]
            return True
        if all(self.tabuleiro[TAMANHO_TABULEIRO - 1 - i][i][i] == jogador for i in range(TAMANHO_TABULEIRO)):
            self.linha_vitoria = [(TAMANHO_TABULEIRO - 1, 0, 0), (0, TAMANHO_TABULEIRO - 1, TAMANHO_TABULEIRO - 1)]
            return True

        return False

    def tabuleiro_cheio(self):
        return all(self.tabuleiro[x][y][z] != 0
                   for x in range(TAMANHO_TABULEIRO)
                   for y in range(TAMANHO_TABULEIRO)
                   for z in range(TAMANHO_TABULEIRO))

    def avaliar_tabuleiro(self):
        if self.verificar_vencedor(1):
            return -1000
        elif self.verificar_vencedor(-1):
            return 1000
        else:
            return 0

    def minimax(self, profundidade, alfa, beta, e_maximizando):
        if profundidade == 0 or self.jogo_terminado:
            return self.avaliar_tabuleiro()

        if e_maximizando:
            melhor_valor = -math.inf
            for x in range(TAMANHO_TABULEIRO):
                for y in range(TAMANHO_TABULEIRO):
                    for z in range(TAMANHO_TABULEIRO):
                        if self.tabuleiro[x][y][z] == 0:
                            self.fazer_jogada(x, y, z, -1)
                            valor = self.minimax(profundidade - 1, alfa, beta, False)
                            self.desfazer_jogada(x, y, z)
                            melhor_valor = max(melhor_valor, valor)
                            alfa = max(alfa, melhor_valor)
                            if beta <= alfa:
                                break
            return melhor_valor
        else:
            melhor_valor = math.inf
            for x in range(TAMANHO_TABULEIRO):
                for y in range(TAMANHO_TABULEIRO):
                    for z in range(TAMANHO_TABULEIRO):
                        if self.tabuleiro[x][y][z] == 0:
                            self.fazer_jogada(x, y, z, 1)
                            valor = self.minimax(profundidade - 1, alfa, beta, True)
                            self.desfazer_jogada(x, y, z)
                            melhor_valor = min(melhor_valor, valor)
                            beta = min(beta, melhor_valor)
                            if beta <= alfa:
                                break
            return melhor_valor

    def obter_melhor_jogada(self):
        melhor_valor = -math.inf
        melhor_jogada = None
        alfa = -math.inf
        beta = math.inf

        for x in range(TAMANHO_TABULEIRO):
            for y in range(TAMANHO_TABULEIRO):
                for z in range(TAMANHO_TABULEIRO):
                    if self.tabuleiro[x][y][z] == 0:
                        self.fazer_jogada(x, y, z, -1)
                        valor = self.minimax(self.profundidade_maxima - 1, alfa, beta, False)
                        self.desfazer_jogada(x, y, z)
                        if valor > melhor_valor:
                            melhor_valor = valor
                            melhor_jogada = (x, y, z)
                        alfa = max(alfa, melhor_valor)
                        if beta <= alfa:
                            break

        return melhor_jogada

    def jogar_ia(self):
        print("IA está pensando...")
        start_time = time.time()
        melhor_jogada = self.obter_melhor_jogada()
        end_time = time.time()
        print(f"IA decidiu em {end_time - start_time:.2f} segundos")
        if melhor_jogada:
            x, y, z = melhor_jogada
            self.fazer_jogada(x, y, z, -1)
            print(f"IA jogou na posição: ({x}, {y}, {z})")
            if self.verificar_vencedor(-1):
                self.jogo_terminado = True
                self.vencedor = -1
                self.placar_ia += 1
                mostrar_popup_ia_ganhou()
            elif self.tabuleiro_cheio():
                self.jogo_terminado = True
            else:
                self.jogador_atual = 1


def mostrar_popup_jogador_ganhou():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    messagebox.showinfo("Fim de Jogo", "Parabéns, você ganhou!")
    root.destroy()

class Camera:
    def __init__(self):
        self.posicao = Vector3(0, 5, 10)
        self.yaw = 0
        self.pitch = -30

    def mover(self, dx, dy, dz):
        frente = Vector3(math.sin(math.radians(self.yaw)), 0, math.cos(math.radians(self.yaw)))
        direita = Vector3(frente.z, 0, -frente.x)
        self.posicao += frente * dz + direita * dx + Vector3(0, 1, 0) * dy

    def rotacionar(self, dyaw, dpitch):
        self.yaw -= dyaw
        self.pitch -= dpitch
        self.pitch = max(-89, min(89, self.pitch))

    def aplicar(self):
        glRotatef(-self.pitch, 1, 0, 0)
        glRotatef(-self.yaw, 0, 1, 0)
        glTranslatef(-self.posicao.x, -self.posicao.y, -self.posicao.z)

class Estrela:
    def __init__(self):
        self.posicao = Vector3(random.uniform(-20, 20), random.uniform(-20, 20), random.uniform(-20, -10))
        self.cor = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
        self.tamanho = random.uniform(0.01, 0.03)

    def desenhar(self):
        glPushMatrix()
        glTranslatef(self.posicao.x, self.posicao.y, self.posicao.z)
        glColor3f(*self.cor)

        glPointSize(self.tamanho * 100)
        glBegin(GL_POINTS)
        glVertex3f(0, 0, 0)
        glEnd()

        glPopMatrix()

class Asteroide:
    def __init__(self):
        self.posicao = Vector3(random.uniform(-15, 15), random.uniform(-15, 15), random.uniform(-30, -20))
        self.velocidade = Vector3(random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01))
        self.tamanho = random.uniform(0.1, 0.3)
        self.rotacao = Vector3(random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360))
        self.velocidade_rotacao = Vector3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))

    def atualizar(self):
        self.posicao += self.velocidade
        self.rotacao += self.velocidade_rotacao
        if abs(self.posicao.x) > 15 or abs(self.posicao.y) > 15 or self.posicao.z < -30 or self.posicao.z > -20:
            self.posicao = Vector3(random.uniform(-15, 15), random.uniform(-15, 15), -30)

    def desenhar(self):
        glPushMatrix()
        glTranslatef(self.posicao.x, self.posicao.y, self.posicao.z)
        glRotatef(self.rotacao.x, 1, 0, 0)
        glRotatef(self.rotacao.y, 0, 1, 0)
        glRotatef(self.rotacao.z, 0, 0, 1)
        glColor3f(0.5, 0.5, 0.5)

        glBegin(GL_TRIANGLES)
        vertices = [
            (0, 1, 0), (1, 0, 0), (0, 0, 1),
            (0, 1, 0), (0, 0, 1), (-1, 0, 0),
            (0, 1, 0), (-1, 0, 0), (0, 0, -1),
            (0, 1, 0), (0, 0, -1), (1, 0, 0),
            (0, -1, 0), (1, 0, 0), (0, 0, 1),
            (0, -1, 0), (0, 0, 1), (-1, 0, 0),
            (0, -1, 0), (-1, 0, 0), (0, 0, -1),
            (0, -1, 0), (0, 0, -1), (1, 0, 0)
        ]
        for v in vertices:
            glVertex3f(v[0] * self.tamanho, v[1] * self.tamanho, v[2] * self.tamanho)
        glEnd()

        glPopMatrix()

def inicializar_gl(largura, altura):
    glViewport(0, 0, largura, altura)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (largura / altura), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def desenhar_tabuleiro():
    glColor3f(*CIANO)
    glLineWidth(2.0)
    for i in range(TAMANHO_TABULEIRO + 1):
        for j in range(TAMANHO_TABULEIRO + 1):
            glBegin(GL_LINES)
            glVertex3f(i * TAMANHO_CELULA - TAMANHO_CELULA * 1.5, -TAMANHO_CELULA * 1.5,
                       j * TAMANHO_CELULA - TAMANHO_CELULA * 1.5)
            glVertex3f(i * TAMANHO_CELULA - TAMANHO_CELULA * 1.5, TAMANHO_CELULA * 1.5,
                       j * TAMANHO_CELULA - TAMANHO_CELULA * 1.5)
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(-TAMANHO_CELULA * 1.5, i * TAMANHO_CELULA - TAMANHO_CELULA * 1.5,
                       j * TAMANHO_CELULA - TAMANHO_CELULA * 1.5)
            glVertex3f(TAMANHO_CELULA * 1.5, i * TAMANHO_CELULA - TAMANHO_CELULA * 1.5,
                       j * TAMANHO_CELULA - TAMANHO_CELULA * 1.5)
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(i * TAMANHO_CELULA - TAMANHO_CELULA * 1.5, j * TAMANHO_CELULA - TAMANHO_CELULA * 1.5,
                       -TAMANHO_CELULA * 1.5)
            glVertex3f(i * TAMANHO_CELULA - TAMANHO_CELULA * 1.5, j * TAMANHO_CELULA - TAMANHO_CELULA * 1.5,
                       TAMANHO_CELULA * 1.5)
            glEnd()

def desenhar_base_tabuleiro():
    glColor3f(*ROXO)
    glPushMatrix()
    glTranslatef(0, -TAMANHO_CELULA * 1.6, 0)
    glScalef(TAMANHO_CELULA * 3.2, 0.1, TAMANHO_CELULA * 3.2)

    glBegin(GL_QUADS)
    glVertex3f(-1, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, 0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()

    glPopMatrix()

def desenhar_esfera(x, y, z, cor):
    glPushMatrix()
    glTranslatef(x * TAMANHO_CELULA - TAMANHO_CELULA, y * TAMANHO_CELULA - TAMANHO_CELULA,
                 z * TAMANHO_CELULA - TAMANHO_CELULA)
    glColor3f(*cor)

    slices, stacks = 16, 16
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + float(i) / stacks)
        z0 = math.sin(lat0)
        zr0 = math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * float(j) / slices
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0 * RAIO_ESFERA, y * zr0 * RAIO_ESFERA, z0 * RAIO_ESFERA)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1 * RAIO_ESFERA, y * zr1 * RAIO_ESFERA, z1 * RAIO_ESFERA)
        glEnd()

    glPopMatrix()

def mostrar_popup_ia_ganhou():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    messagebox.showinfo("Fim de Jogo", "A IA ganhou!")
    root.destroy()
def desenhar_x(x, y, z):
    tamanho = RAIO_ESFERA * 1.5
    glPushMatrix()
    glTranslatef(x * TAMANHO_CELULA - TAMANHO_CELULA, y * TAMANHO_CELULA - TAMANHO_CELULA,
                 z * TAMANHO_CELULA - TAMANHO_CELULA)
    glColor3f(*VERMELHO)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex3f(-tamanho, -tamanho, -tamanho)
    glVertex3f(tamanho, tamanho, tamanho)
    glVertex3f(-tamanho, -tamanho, tamanho)
    glVertex3f(tamanho, tamanho, -tamanho)
    glVertex3f(-tamanho, tamanho, -tamanho)
    glVertex3f(tamanho, -tamanho, tamanho)
    glVertex3f(-tamanho, tamanho, tamanho)
    glVertex3f(tamanho, -tamanho, -tamanho)
    glEnd()
    glPopMatrix()

def desenhar_jogo(jogo, celula_selecionada, estrelas, asteroides, camera):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Desenhar elementos de fundo
    for estrela in estrelas:
        estrela.desenhar()
    for asteroide in asteroides:
        try:
            asteroide.desenhar()
        except OpenGL.error.GLError:
            pass  # Ignorar erros de renderização de asteroides

    # Aplicar transformações da câmera
    camera.aplicar()

    desenhar_base_tabuleiro()
    desenhar_tabuleiro()

    for x in range(TAMANHO_TABULEIRO):
        for y in range(TAMANHO_TABULEIRO):
            for z in range(TAMANHO_TABULEIRO):
                if jogo.tabuleiro[x][y][z] == 1:
                    desenhar_esfera(x, y, z, VERMELHO)
                elif jogo.tabuleiro[x][y][z] == -1:
                    desenhar_x(x, y, z)
                elif (x, y, z) == celula_selecionada:
                    desenhar_esfera(x, y, z, AMARELO)  # Célula selecionada

    if jogo.jogo_terminado and jogo.linha_vitoria:
        inicio, fim = jogo.linha_vitoria
        glColor3f(*VERDE)
        glLineWidth(5.0)
        glBegin(GL_LINES)
        glVertex3f(inicio[0] * TAMANHO_CELULA - TAMANHO_CELULA,
                   inicio[1] * TAMANHO_CELULA - TAMANHO_CELULA,
                   inicio[2] * TAMANHO_CELULA - TAMANHO_CELULA)
        glVertex3f(fim[0] * TAMANHO_CELULA - TAMANHO_CELULA,
                   fim[1] * TAMANHO_CELULA - TAMANHO_CELULA,
                   fim[2] * TAMANHO_CELULA - TAMANHO_CELULA)
        glEnd()

def desenhar_mira(superficie):
    centro_x, centro_y = superficie.get_width() // 2, superficie.get_height() // 2
    comprimento = 20
    pygame.draw.line(superficie, BRANCO, (centro_x - comprimento, centro_y), (centro_x + comprimento, centro_y), 2)
    pygame.draw.line(superficie, BRANCO, (centro_x, centro_y - comprimento), (centro_x, centro_y + comprimento), 2)

def desenhar_placar(superficie, jogo):
    fonte = pygame.font.Font(None, 36)
    texto_placar = f"Jogador: {jogo.placar_jogador}  IA: {jogo.placar_ia}"
    superficie_texto = fonte.render(texto_placar, True, BRANCO)
    superficie.blit(superficie_texto, (10, 10))

def raio_intersecta_esfera(origem_raio, direcao_raio, centro_esfera, raio_esfera):
    oc = origem_raio - centro_esfera
    a = direcao_raio.dot(direcao_raio)
    b = 2.0 * oc.dot(direcao_raio)
    c = oc.dot(oc) - raio_esfera * raio_esfera
    discriminante = b * b - 4 * a * c
    return discriminante > 0

def obter_celula_selecionada(camera):
    origem_raio = camera.posicao
    direcao_raio = Vector3(
        math.cos(math.radians(camera.pitch)) * math.sin(math.radians(camera.yaw)),
        -math.sin(math.radians(camera.pitch)),
        math.cos(math.radians(camera.pitch)) * math.cos(math.radians(camera.yaw))
    )

    for x in range(TAMANHO_TABULEIRO):
        for y in range(TAMANHO_TABULEIRO):
            for z in range(TAMANHO_TABULEIRO):
                centro_esfera = Vector3(
                    x * TAMANHO_CELULA - TAMANHO_CELULA,
                    y * TAMANHO_CELULA - TAMANHO_CELULA,
                    z * TAMANHO_CELULA - TAMANHO_CELULA
                )
                if raio_intersecta_esfera(origem_raio, direcao_raio, centro_esfera, RAIO_ESFERA):
                    return (x, y, z)
    return None

def main():
    pygame.init()
    tela = (800, 600)
    superficie = pygame.display.set_mode(tela, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Jogo da Velha 3D Espacial")

    inicializar_gl(*tela)

    jogo = JogoDaVelha3D(profundidade_maxima=3)
    camera = Camera()
    relogio = pygame.time.Clock()

    estrelas = [Estrela() for _ in range(NUM_ESTRELAS)]
    asteroides = [Asteroide() for _ in range(NUM_ASTEROIDES)]

    # Perguntar ao jogador se quer começar
    jogador_comeca = input("Você quer começar? (s/n): ").lower() == 's'
    if not jogador_comeca:
        jogo.jogador_atual = -1
        jogo.jogar_ia()

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    celula_selecionada = None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif evento.key == pygame.K_v and jogo.jogador_atual == 1:
                    if celula_selecionada and jogo.tabuleiro[celula_selecionada[0]][celula_selecionada[1]][
                        celula_selecionada[2]] == 0:
                        jogo.fazer_jogada(celula_selecionada[0], celula_selecionada[1], celula_selecionada[2], 1)
                        print(
                            f"Jogador jogou na posição: ({celula_selecionada[0]}, {celula_selecionada[1]}, {celula_selecionada[2]})")
                        if jogo.verificar_vencedor(1):
                            jogo.jogo_terminado = True
                            jogo.vencedor = 1
                            jogo.placar_jogador += 1
                            mostrar_popup_jogador_ganhou()  # Adicionando o pop-up para o jogador aqui
                        elif jogo.tabuleiro_cheio():
                            jogo.jogo_terminado = True
                        else:
                            jogo.jogador_atual = -1
                            jogo.jogar_ia()

        # Movimento da câmera
        teclas = pygame.key.get_pressed()
        camera.mover(
            (teclas[pygame.K_d] - teclas[pygame.K_a]) * 0.1,
            (teclas[pygame.K_e] - teclas[pygame.K_q]) * 0.1,
            (teclas[pygame.K_s] - teclas[pygame.K_w]) * 0.1
        )

        # Rotação da câmera
        movimento_mouse = pygame.mouse.get_rel()
        camera.rotacionar(movimento_mouse[0] * 0.1, movimento_mouse[1] * 0.1)

        # Atualizar asteroides
        for asteroide in asteroides:
            asteroide.atualizar()

        celula_selecionada = obter_celula_selecionada(camera)
        desenhar_jogo(jogo, celula_selecionada, estrelas, asteroides, camera)

        # Desenhar a mira e o placar
        superficie_2d = pygame.Surface(tela, pygame.SRCALPHA)
        desenhar_mira(superficie_2d)
        desenhar_placar(superficie_2d, jogo)
        superficie.blit(superficie_2d, (0, 0))

        pygame.display.flip()
        relogio.tick(60)

        if jogo.jogo_terminado:
            if jogo.vencedor == 1:
                print("Você venceu!")
            elif jogo.vencedor == -1:
                print("A IA venceu!")
            else:
                print("Empate!")
            pygame.time.wait(3000)
            jogo = JogoDaVelha3D(profundidade_maxima=3)
            jogo.placar_jogador = jogo.placar_jogador
            jogo.placar_ia = jogo.placar_ia
            if not jogador_comeca:
                jogo.jogador_atual = -1
                jogo.jogar_ia()

if __name__ == "__main__":
    main()
