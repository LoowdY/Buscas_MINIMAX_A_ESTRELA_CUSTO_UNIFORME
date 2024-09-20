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
