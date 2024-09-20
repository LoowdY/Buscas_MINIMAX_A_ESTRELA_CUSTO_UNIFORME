import sys
import pygame
import heapq

# Initialize Pygame
pygame.init()

# Screen settings
LARGURA, ALTURA = 1000, 600  # Ajustado para incluir a barra lateral direita
TAMANHO_GRADE = 12
TAMANHO_CELULA = 50

# Colors
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
CINZA_CLARO = (200, 200, 200)
CINZA_ESCURO = (100, 100, 100)

# Create the screen
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Busca de Caminhos Interativo")

# Definir os 3 níveis do mapa
mapa_nivel_1 = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

mapa_nivel_2 = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

mapa_nivel_3 = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Heuristic function for A* (Manhattan distance)
def heuristica(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

# A* Search Algorithm
def busca_a_estrela(inicio, fim, grade):
    vizinhos = [(0,1), (0,-1), (1,0), (-1,0)]
    conjunto_fechado = set()
    veio_de = {}
    pontuacao_g = {inicio: 0}
    pontuacao_f = {inicio: heuristica(inicio, fim)}
    conjunto_aberto = []
    heapq.heappush(conjunto_aberto, (pontuacao_f[inicio], inicio))

    while conjunto_aberto:
        atual = heapq.heappop(conjunto_aberto)[1]

        yield atual, conjunto_fechado, veio_de, pontuacao_g, pontuacao_f

        if atual == fim:
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            caminho.append(inicio)
            caminho.reverse()
            return caminho

        conjunto_fechado.add(atual)

        for i, j in vizinhos:
            vizinho = atual[0] + i, atual[1] + j
            if 0 <= vizinho[0] < len(grade) and 0 <= vizinho[1] < len(grade[0]):
                if grade[vizinho[0]][vizinho[1]] == 0:
                    continue
            else:
                continue

            tentativa_g = pontuacao_g[atual] + 1

            if vizinho in conjunto_fechado and tentativa_g >= pontuacao_g.get(vizinho, 0):
                continue

            if tentativa_g < pontuacao_g.get(vizinho, float('inf')) or vizinho not in [i[1] for i in conjunto_aberto]:
                veio_de[vizinho] = atual
                pontuacao_g[vizinho] = tentativa_g
                pontuacao_f[vizinho] = pontuacao_g[vizinho] + heuristica(vizinho, fim)
                heapq.heappush(conjunto_aberto, (pontuacao_f[vizinho], vizinho))

    return None

# Uniform Cost Search Algorithm
def busca_custo_uniforme(inicio, fim, grade):
    vizinhos = [(0,1), (0,-1), (1,0), (-1,0)]
    visitados = set()
    fila = [(0, inicio, [])]
    custos = {inicio: 0}

    while fila:
        (custo, atual, caminho) = heapq.heappop(fila)

        yield atual, visitados, dict(zip(caminho, caminho[1:] + [atual])), custos

        if atual == fim:
            return caminho + [atual]

        if atual in visitados:
            continue

        visitados.add(atual)

        for i, j in vizinhos:
            proximo_no = atual[0] + i, atual[1] + j
            if 0 <= proximo_no[0] < len(grade) and 0 <= proximo_no[1] < len(grade[0]):
                if grade[proximo_no[0]][proximo_no[1]] == 1:
                    novo_custo = custo + 1
                    if proximo_no not in custos or novo_custo < custos[proximo_no]:
                        custos[proximo_no] = novo_custo
                        heapq.heappush(fila, (novo_custo, proximo_no, caminho + [atual]))

    return None

# Function to draw the grid
def desenhar_grade(tela, grade, inicio, fim, caminho, atual, visitados, borda):
    for i in range(TAMANHO_GRADE):
        for j in range(TAMANHO_GRADE):
            cor = BRANCO if grade[i][j] == 1 else PRETO
            pygame.draw.rect(tela, cor, (j*TAMANHO_CELULA, i*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
            pygame.draw.rect(tela, PRETO, (j*TAMANHO_CELULA, i*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA), 1)

    if inicio:
        pygame.draw.rect(tela, VERDE, (inicio[1]*TAMANHO_CELULA, inicio[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
    if fim:
        pygame.draw.rect(tela, VERMELHO, (fim[1]*TAMANHO_CELULA, fim[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    for no in visitados:
        if no != inicio and no != fim and grade[no[0]][no[1]] == 1:
            pygame.draw.rect(tela, LARANJA, (no[1]*TAMANHO_CELULA, no[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    for no in borda:
        if no != inicio and no != fim and grade[no[0]][no[1]] == 1:
            pygame.draw.rect(tela, ROXO, (no[1]*TAMANHO_CELULA, no[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    if atual and grade[atual[0]][atual[1]] == 1:
        pygame.draw.rect(tela, AZUL, (atual[1]*TAMANHO_CELULA, atual[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    if caminho:
        for no in caminho:
            if grade[no[0]][no[1]] == 1:
                pygame.draw.rect(tela, AMARELO, (no[1]*TAMANHO_CELULA, no[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

# Function to draw the sidebar with instructions and buttons
def desenhar_barra_lateral(tela, fonte, algoritmo, nivel, reiniciar, proximo, mudar_algoritmo):
    # Fundo da barra lateral
    pygame.draw.rect(tela, CINZA_CLARO, (LARGURA - 200, 0, 200, ALTURA))

    # Instruções
    instrucoes = [
        "Instruções:",
        "1. Clique esquerdo:",
        "   Definir início e fim.",
        "2. Clique direito:",
        "   Adicionar/remover paredes.",
        "3. Espaço: Iniciar busca.",
        f"Algoritmo: {algoritmo}",
        f"Nível: {nivel}",
    ]
    for i, instrucao in enumerate(instrucoes):
        texto_renderizado = fonte.render(instrucao, True, PRETO)
        tela.blit(texto_renderizado, (LARGURA - 190, 20 + i*25))

    # Botão de reiniciar busca
    pygame.draw.rect(tela, CINZA_ESCURO, reiniciar)
    texto_reiniciar = fonte.render("Reiniciar Busca", True, BRANCO)
    tela.blit(texto_reiniciar, (LARGURA - 180, reiniciar.y + 10))

    # Botão de próximo nível
    pygame.draw.rect(tela, CINZA_ESCURO, proximo)
    texto_proximo = fonte.render("Próximo Nível", True, BRANCO)
    tela.blit(texto_proximo, (LARGURA - 180, proximo.y + 10))

    # Botão de mudar algoritmo
    pygame.draw.rect(tela, CINZA_ESCURO, mudar_algoritmo)
    texto_mudar = fonte.render("Mudar Algoritmo", True, BRANCO)
    tela.blit(texto_mudar, (LARGURA - 180, mudar_algoritmo.y + 10))

# Main game function
def selecionar_algoritmo():
    fonte_titulo = pygame.font.Font(None, 48)
    fonte_opcao = pygame.font.Font(None, 36)
    titulo = fonte_titulo.render("Selecione o Algoritmo", True, PRETO)
    opcao1 = fonte_opcao.render("1 - A*", True, PRETO)
    opcao2 = fonte_opcao.render("2 - Busca de Custo Uniforme", True, PRETO)

    selecionado = None
    while selecionado not in ["A*", "Custo Uniforme"]:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    selecionado = "A*"
                elif evento.key == pygame.K_2:
                    selecionado = "Custo Uniforme"

        tela.fill(CINZA_CLARO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 3))
        tela.blit(opcao1, (LARGURA // 2 - opcao1.get_width() // 2, ALTURA // 2))
        tela.blit(opcao2, (LARGURA // 2 - opcao2.get_width() // 2, ALTURA // 2 + 50))
        pygame.display.flip()
    return selecionado

# Main game function
def main():
    mapas = [mapa_nivel_1, mapa_nivel_2, mapa_nivel_3]
    fonte = pygame.font.Font(None, 24)

    for nivel, grade in enumerate(mapas, start=1):
        algoritmo = selecionar_algoritmo()
        inicio = None
        fim = None
        caminho = None
        gerador_busca = None
        relogio = pygame.time.Clock()

        rodando = True
        atual = None
        visitados = set()
        borda = []

        # Definir posições dos botões
        reiniciar_rect = pygame.Rect(LARGURA - 180, 400, 160, 40)
        proximo_rect = pygame.Rect(LARGURA - 180, 460, 160, 40)
        mudar_algoritmo_rect = pygame.Rect(LARGURA - 180, 520, 160, 40)

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    grade_x, grade_y = y // TAMANHO_CELULA, x // TAMANHO_CELULA

                    # Verifica se o clique foi em algum dos botões
                    if reiniciar_rect.collidepoint(x, y):
                        gerador_busca = None  # Reiniciar a busca
                        caminho = None
                        atual = None
                        visitados = set()
                        borda = []
                    elif proximo_rect.collidepoint(x, y):
                        rodando = False  # Passar para o próximo nível
                    elif mudar_algoritmo_rect.collidepoint(x, y):
                        algoritmo = selecionar_algoritmo()  # Mudar o algoritmo no meio do nível

                    # Se o clique foi dentro da grade
                    if 0 <= grade_x < TAMANHO_GRADE and 0 <= grade_y < TAMANHO_GRADE and not reiniciar_rect.collidepoint(x, y):
                        if evento.button == 1:  # Left mouse button
                            if not inicio:
                                inicio = (grade_x, grade_y)
                            elif not fim and (grade_x, grade_y) != inicio:
                                fim = (grade_x, grade_y)
                        elif evento.button == 3:  # Right mouse button
                            if (grade_x, grade_y) != inicio and (grade_x, grade_y) != fim:
                                grade[grade_x][grade_y] = 1 - grade[grade_x][grade_y]  # Toggle cell state
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and inicio and fim:
                        if algoritmo == "A*":
                            gerador_busca = busca_a_estrela(inicio, fim, grade)
                        else:
                            gerador_busca = busca_custo_uniforme(inicio, fim, grade)
                        caminho = None
                        atual = None
                        visitados = set()
                        borda = []

            tela.fill(BRANCO)

            if gerador_busca:
                try:
                    if algoritmo == "A*":
                        atual, visitados, veio_de, pontuacao_g, pontuacao_f = next(gerador_busca)
                        borda = [no for no in pontuacao_f if no not in visitados]
                    else:
                        atual, visitados, veio_de, custos = next(gerador_busca)
                        borda = [no for no in custos if no not in visitados]
                except StopIteration as e:
                    caminho = e.value if e.value else []
                    gerador_busca = None

            desenhar_grade(tela, grade, inicio, fim, caminho, atual if gerador_busca else None,
                           visitados if gerador_busca else set(), borda if gerador_busca else [])

            # Desenha a barra lateral
            desenhar_barra_lateral(tela, fonte, algoritmo, nivel, reiniciar_rect, proximo_rect, mudar_algoritmo_rect)

            pygame.display.flip()
            relogio.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
