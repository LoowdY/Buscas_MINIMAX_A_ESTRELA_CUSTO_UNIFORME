import sys
import pygame
import heapq

# Initialize Pygame
pygame.init()

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

# Cell size
TAMANHO_CELULA = 50

# Define the maps for each level
mapa1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]





mapa2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]




mapa3 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
        conjunto_fechado.add(atual)

        # Generate the frontier (nodes in open set)
        borda = [item[1] for item in conjunto_aberto]

        # Print visited nodes and frontier with costs and evaluation function
        print(f"\nVisitado: {atual}, g={pontuacao_g[atual]}, f={pontuacao_f[atual]}")
        print("Borda:")
        for no in borda:
            print(f"  {no}, g={pontuacao_g[no]}, f={pontuacao_f[no]}")

        yield atual, conjunto_fechado, veio_de, pontuacao_g.copy(), pontuacao_f.copy()

        if atual == fim:
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            caminho.append(inicio)
            caminho.reverse()
            return caminho

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
        if atual in visitados:
            continue

        visitados.add(atual)

        # Generate the frontier (nodes in queue)
        borda = [item[1] for item in fila]

        # Print visited nodes and frontier with costs
        print(f"\nVisitado: {atual}, custo={custos[atual]}")
        print("Borda:")
        for no in borda:
            print(f"  {no}, custo={custos[no]}")

        yield atual, visitados.copy(), dict(zip(caminho, caminho[1:] + [atual])), custos.copy()

        if atual == fim:
            return caminho + [atual]

        for i, j in vizinhos:
            proximo_no = atual[0] + i, atual[1] + j
            if 0 <= proximo_no[0] < len(grade) and 0 <= proximo_no[1] < len(grade[0]):
                if grade[proximo_no[0]][proximo_no[1]] == 1:
                    novo_custo = custo + 1
                    if proximo_no not in custos or novo_custo < custos[proximo_no]:
                        custos[proximo_no] = novo_custo
                        heapq.heappush(fila, (novo_custo, proximo_no, caminho + [atual]))

    return None

# Function to draw the grid and show node details
def desenhar_grade(tela, grade, inicio, fim, caminho, atual, visitados, borda, tamanho_celula, pontuacao_g=None, pontuacao_f=None, custos=None):
    fonte = pygame.font.Font(None, 24)
    for i in range(len(grade)):
        for j in range(len(grade[0])):
            cor = BRANCO if grade[i][j] == 1 else PRETO
            pygame.draw.rect(tela, cor, (j*tamanho_celula, i*tamanho_celula, tamanho_celula, tamanho_celula))
            pygame.draw.rect(tela, PRETO, (j*tamanho_celula, i*tamanho_celula, tamanho_celula, tamanho_celula), 1)

    if inicio:
        pygame.draw.rect(tela, VERDE, (inicio[1]*tamanho_celula, inicio[0]*tamanho_celula, tamanho_celula, tamanho_celula))
    if fim:
        pygame.draw.rect(tela, VERMELHO, (fim[1]*tamanho_celula, fim[0]*tamanho_celula, tamanho_celula, tamanho_celula))

    for no in visitados:
        if no != inicio and no != fim and grade[no[0]][no[1]] == 1:
            pygame.draw.rect(tela, LARANJA, (no[1]*tamanho_celula, no[0]*tamanho_celula, tamanho_celula, tamanho_celula))

    for no in borda:
        if no != inicio and no != fim and grade[no[0]][no[1]] == 1:
            pygame.draw.rect(tela, ROXO, (no[1]*tamanho_celula, no[0]*tamanho_celula, tamanho_celula, tamanho_celula))

        # Draw cost and evaluation function
        if pontuacao_g and pontuacao_f and no in pontuacao_g:
            texto = f"g={pontuacao_g[no]}, f={pontuacao_f[no]}"
            texto_renderizado = fonte.render(texto, True, PRETO)
            tela.blit(texto_renderizado, (no[1]*tamanho_celula + 5, no[0]*tamanho_celula + 5))

        elif custos and no in custos:
            texto = f"custo={custos[no]}"
            texto_renderizado = fonte.render(texto, True, PRETO)
            tela.blit(texto_renderizado, (no[1]*tamanho_celula + 5, no[0]*tamanho_celula + 5))

    if atual and grade[atual[0]][atual[1]] == 1:
        pygame.draw.rect(tela, AZUL, (atual[1]*tamanho_celula, atual[0]*tamanho_celula, tamanho_celula, tamanho_celula))

    if caminho:
        for no in caminho:
            if grade[no[0]][no[1]] == 1:
                pygame.draw.rect(tela, AMARELO, (no[1]*tamanho_celula, no[0]*tamanho_celula, tamanho_celula, tamanho_celula))

# Function to draw the sidebar with instructions and buttons
def desenhar_barra_lateral(tela, fonte, algoritmo, nivel, reiniciar, proximo, mudar_algoritmo, largura_tela):
    # Sidebar background
    pygame.draw.rect(tela, CINZA_CLARO, (largura_tela - 200, 0, 200, largura_tela))

    # Instructions
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
        tela.blit(texto_renderizado, (largura_tela - 190, 20 + i*25))

    # Restart search button
    pygame.draw.rect(tela, CINZA_ESCURO, reiniciar)
    texto_reiniciar = fonte.render("Reiniciar Busca", True, BRANCO)
    tela.blit(texto_reiniciar, (largura_tela - 180, reiniciar.y + 10))

    # Next level button
    pygame.draw.rect(tela, CINZA_ESCURO, proximo)
    texto_proximo = fonte.render("Próximo Nível", True, BRANCO)
    tela.blit(texto_proximo, (largura_tela - 180, proximo.y + 10))

    # Change algorithm button
    pygame.draw.rect(tela, CINZA_ESCURO, mudar_algoritmo)
    texto_mudar = fonte.render("Mudar Algoritmo", True, BRANCO)
    tela.blit(texto_mudar, (largura_tela - 180, mudar_algoritmo.y + 10))

# Function to select algorithm
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
        tela.blit(titulo, (tela.get_width() // 2 - titulo.get_width() // 2, tela.get_height() // 3))
        tela.blit(opcao1, (tela.get_width() // 2 - opcao1.get_width() // 2, tela.get_height() // 2))
        tela.blit(opcao2, (tela.get_width() // 2 - opcao2.get_width() // 2, tela.get_height() // 2 + 50))
        pygame.display.flip()
    return selecionado

def main():
    mapas = [mapa1, mapa2, mapa3]
    fonte = pygame.font.Font(None, 24)

    # Initialize search history list
    search_history = []

    for nivel, grade in enumerate(mapas, start=1):
        # Adjust grid size based on the map
        TAMANHO_GRADE_X = len(grade[0])
        TAMANHO_GRADE_Y = len(grade)
        largura_grade = TAMANHO_GRADE_X * TAMANHO_CELULA
        altura_grade = TAMANHO_GRADE_Y * TAMANHO_CELULA

        # Adjust screen size
        LARGURA = largura_grade + 200  # 200 pixels for sidebar
        ALTURA = max(altura_grade, 600)  # Ensure a minimum height

        # Create the screen
        global tela
        tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Jogo de Busca de Caminhos Interativo")

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

        # Initialize variables
        pontuacao_g = {}
        pontuacao_f = {}
        custos = {}

        # Define button positions
        reiniciar_rect = pygame.Rect(LARGURA - 180, 400, 160, 40)
        proximo_rect = pygame.Rect(LARGURA - 180, 460, 160, 40)
        mudar_algoritmo_rect = pygame.Rect(LARGURA - 180, 520, 160, 40)

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    grade_x, grade_y = y // TAMANHO_CELULA, x // TAMANHO_CELULA

                    # Check if click was on any button
                    if reiniciar_rect.collidepoint(x, y):
                        gerador_busca = None  # Restart search
                        caminho = None
                        atual = None
                        visitados = set()
                        borda = []
                        pontuacao_g = {}
                        pontuacao_f = {}
                        custos = {}
                    elif proximo_rect.collidepoint(x, y):
                        rodando = False  # Move to next level
                    elif mudar_algoritmo_rect.collidepoint(x, y):
                        algoritmo = selecionar_algoritmo()  # Change algorithm during the level

                    # If click was inside the grid
                    if 0 <= grade_x < TAMANHO_GRADE_Y and 0 <= grade_y < TAMANHO_GRADE_X and not reiniciar_rect.collidepoint(x, y):
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
                        pontuacao_g = {}
                        pontuacao_f = {}
                        custos = {}

            tela.fill(BRANCO)

            if gerador_busca:
                try:
                    if algoritmo == "A*":
                        atual, visitados, veio_de, pontuacao_g, pontuacao_f = next(gerador_busca)
                        borda = [no for no in pontuacao_f if no not in visitados and no != atual]
                    else:
                        atual, visitados, veio_de, custos = next(gerador_busca)
                        borda = [no for no in custos if no not in visitados and no != atual]
                except StopIteration as e:
                    caminho = e.value if e.value else []
                    gerador_busca = None

                    # Compute cost and record search
                    if caminho:
                        cost = len(caminho) - 1
                        print(f"Algoritmo: {algoritmo}, Custo da busca: {cost}")
                        search_history.append((algoritmo, cost))
                    else:
                        print(f"Algoritmo: {algoritmo}, Não foi encontrado caminho.")
                        search_history.append((algoritmo, None))

            desenhar_grade(tela, grade, inicio, fim, caminho, atual if gerador_busca else None,
                           visitados if gerador_busca else set(), borda if gerador_busca else [],
                           TAMANHO_CELULA,
                           pontuacao_g=pontuacao_g if algoritmo == "A*" else None,
                           pontuacao_f=pontuacao_f if algoritmo == "A*" else None,
                           custos=custos if algoritmo == "Custo Uniforme" else None)

            # Draw the sidebar
            desenhar_barra_lateral(tela, fonte, algoritmo, nivel, reiniciar_rect, proximo_rect, mudar_algoritmo_rect, LARGURA)

            pygame.display.flip()
            relogio.tick(10)

    # After game loop, print search history
    print("\nHistórico de Buscas:")
    for idx, (alg, cost) in enumerate(search_history, 1):
        if cost is not None:
            print(f"{idx}. Algoritmo: {alg}, Custo: {cost}")
        else:
            print(f"{idx}. Algoritmo: {alg}, Caminho não encontrado.")

    pygame.quit()

if __name__ == "__main__":
    main()
