# Jogo da Velha 3D Espacial com IA (Minimax)

Este é um projeto de um jogo da velha 3D, onde o jogador pode competir contra uma IA. O jogo é renderizado em 3D utilizando a biblioteca OpenGL e decorado com elementos espaciais, como estrelas e asteroides. A IA utiliza o algoritmo Minimax com poda alfa-beta para decidir suas jogadas.

## Descrição do Projeto

### Algoritmo Minimax
A IA do jogo é baseada no algoritmo Minimax com poda alfa-beta, que é utilizado para determinar a melhor jogada possível em um jogo de dois jogadores. O algoritmo simula todos os movimentos possíveis do jogador e do oponente até uma determinada profundidade, calculando uma pontuação para cada jogada. A poda alfa-beta é usada para otimizar o Minimax, ignorando ramos da árvore de decisão que não precisam ser avaliados, tornando o processo mais eficiente.

- **Maximização**: A IA tenta maximizar seu ganho.
- **Minimização**: O jogador adversário (humano) tenta minimizar o ganho da IA.
- **Poda Alfa-Beta**: Melhora o desempenho do algoritmo, ignorando jogadas que não afetariam a decisão final.

### Estrutura do Tabuleiro
O jogo é jogado em um tabuleiro 3D de 3x3x3, onde cada célula pode conter uma peça do jogador, da IA, ou estar vazia. A cada turno, o jogador ou a IA pode fazer uma jogada em uma célula vazia.

### Elementos Visuais
O jogo é decorado com elementos do espaço, como estrelas e asteroides que se movem ao fundo. Esses elementos são puramente decorativos e não interferem na jogabilidade.

## Bibliotecas Utilizadas

- **Pygame**: Utilizada para gerenciamento de janelas, captura de eventos do teclado e mouse, e controle do loop principal do jogo.
- **PyOpenGL**: Usada para renderizar gráficos 3D no jogo, como o tabuleiro e as esferas.
- **Math**: Funções matemáticas padrão, como seno, cosseno, etc.
- **Random**: Para gerar posições aleatórias dos elementos decorativos (estrelas e asteroides).
- **Time**: Para medir o tempo que a IA leva para tomar decisões.

## Instalação

### Pré-requisitos
Certifique-se de que você tem Python 3.6 ou superior instalado em seu sistema. Além disso, você precisará das bibliotecas Pygame e PyOpenGL.

### Instalando as Dependências
Você pode instalar as dependências necessárias executando:

```bash
pip install -r requirements.txt
```

## Executando o Jogo

Após instalar as dependências, você pode executar o jogo rodando o seguinte comando:

```bash
python main.py
```


## Estrutura do Código

### Funções e Classes

- **Classe `JogoDaVelha3D`**: Esta classe controla a lógica do jogo da velha 3D, incluindo as jogadas, a verificação de vencedores, o algoritmo Minimax e o estado geral do jogo.
  
  - `__init__(self, profundidade_maxima=4)`: Inicializa o tabuleiro e define o jogador atual.
  - `fazer_jogada(x, y, z, jogador)`: Faz uma jogada no tabuleiro 3D.
  - `desfazer_jogada(x, y, z)`: Desfaz uma jogada no tabuleiro.
  - `verificar_vencedor(jogador)`: Verifica se o jogador atual venceu o jogo.
  - `tabuleiro_cheio()`: Verifica se o tabuleiro está cheio, indicando empate.
  - `avaliar_tabuleiro()`: Avalia o estado atual do tabuleiro.
  - `minimax(profundidade, alfa, beta, e_maximizando)`: Implementa o algoritmo Minimax com poda alfa-beta para encontrar a melhor jogada.
  - `obter_melhor_jogada()`: Obtém a melhor jogada possível para a IA.
  - `jogar_ia()`: Faz a jogada da IA usando o Minimax.

- **Classe `Camera`**: Implementa a câmera 3D do jogo, permitindo movimento e rotação ao redor do tabuleiro.
  
  - `__init__()`: Define a posição e a rotação inicial da câmera.
  - `mover(dx, dy, dz)`: Move a câmera na direção desejada.
  - `rotacionar(dyaw, dpitch)`: Rotaciona a câmera com base no movimento do mouse.
  - `aplicar()`: Aplica as transformações da câmera.

- **Classe `Estrela`**: Define estrelas que são renderizadas no fundo do cenário.
  
  - `__init__()`: Inicializa a posição e cor de uma estrela.
  - `desenhar()`: Renderiza a estrela no cenário.

- **Classe `Asteroide`**: Define asteroides que são renderizados no fundo do cenário.
  
  - `__init__()`: Inicializa a posição, tamanho e rotação do asteroide.
  - `atualizar()`: Atualiza a posição e rotação do asteroide.
  - `desenhar()`: Renderiza o asteroide no cenário.

- **Função `inicializar_gl(largura, altura)`**: Inicializa os parâmetros da renderização OpenGL.

- **Função `desenhar_tabuleiro()`**: Desenha o tabuleiro 3D do jogo.

- **Função `desenhar_base_tabuleiro()`**: Desenha a base sob o tabuleiro.

- **Função `desenhar_esfera(x, y, z, cor)`**: Renderiza uma esfera 3D no tabuleiro.

- **Função `desenhar_x(x, y, z)`**: Renderiza um "X" tridimensional para representar a jogada da IA.

- **Função `desenhar_jogo(jogo, celula_selecionada, estrelas, asteroides, camera)`**: Desenha todos os elementos do jogo, incluindo o tabuleiro, as esferas, o "X" e os elementos de fundo (estrelas e asteroides).

- **Função `desenhar_mira(superficie)`**: Desenha uma mira no centro da tela para auxiliar na seleção de células.

- **Função `raio_intersecta_esfera(origem_raio, direcao_raio, centro_esfera, raio_esfera)`**: Verifica se um raio da câmera intersecta uma célula do tabuleiro.

- **Função `obter_celula_selecionada(camera)`**: Calcula qual célula do tabuleiro está sendo selecionada pela mira da câmera.

## Controles

- **Teclas W, A, S, D**: Movem a câmera para frente, esquerda, trás e direita, respectivamente.
- **Teclas Q, E**: Movem a câmera para cima e para baixo.
- **Mouse**: Controla a rotação da câmera.
- **Tecla V**: Faz a jogada do jogador humano na célula selecionada.
- **Esc**: Sai do jogo.

# Autor  
João Renan S. Lopes   


# Agradecimentos   
Agradeço à professora Polyana pelo incentivo ao desenvolvimento do projeto e pelo conhecimento passado.  

