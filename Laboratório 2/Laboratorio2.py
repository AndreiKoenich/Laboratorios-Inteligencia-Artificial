# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 2 - Poda alfa-beta ou MCTS em Othello/Reversi

# Andrei Pochmann Koenich - Cartão 00308680
# Jean Smaniotto Argoud   - Cartão 00275602
# Willian Nunes Reichert  - Cartão 00134090

import time
import math
import random

POSICAOINICIAL = [
'........',
'........',
'........',
'...WB...',
'...BW...',
'........',
'........',
'........',
]

POSICAOTESTE = [
'....W...',
'....W...',
'.WWWWWW.',
'..WWWWWW',
'.W.WWW..',
'W.WWWWWW',
'...WWW..',
'..B.WW..'
]
POSICAOVAZIA = '.'
BRANCO = 'W'
PRETO = 'B'
DIMENSAOTABULEIRO = 8
SEMJOGADAS = (-1,-1)
CONSTANTEUCB = math.sqrt(2)

ESQUERDA = 0
SUPERIORESQUERDA = 1
CIMA = 2
SUPERIORDIREITA = 3
DIREITA = 4
INFERIORDIREITA = 5
BAIXO = 6
INFERIORESQUERDA = 7
DIRECOES = [ESQUERDA,SUPERIORESQUERDA,CIMA,SUPERIORDIREITA,DIREITA,INFERIORDIREITA,BAIXO,INFERIORESQUERDA]

class Nodo:  # Classe para armazenar todas as informações de cada nodo da árvore.
    def __init__(self, tabuleiro_, vitorias_,jogadas_, pai_, filhos_):
        self.tabuleiro = tabuleiro_
        self.vitorias = vitorias_
        self.jogadas = jogadas_
        self.pai = pai_
        self.filhos = filhos_

def testa_final (tabuleiro): # Verifica se o jogo acabou.
    if (testa_valida(tabuleiro, BRANCO) == SEMJOGADAS and testa_valida(tabuleiro, PRETO) == SEMJOGADAS):
        return True

    return False

def calcula_ucb (nodo): # Calcula o valor do critério UCB (Upper Confidence Bound), para um nodo da árvore.
    criterio_ucb = (nodo.vitorias/nodo.jogadas) + CONSTANTEUCB*math.sqrt((2*math.log(nodo.pai.jogadas))/nodo.jogadas)
    return criterio_ucb

def posiciona_peca(tabuleiro, x, y, jogador): #
    novo_tabuleiro = tabuleiro
    lista_aux = list(novo_tabuleiro[y])
    lista_aux[x] = jogador
    novo_tabuleiro[y] = ''.join(lista_aux)
    return novo_tabuleiro

def atualiza_tabuleiro (tabuleiro, x, y, jogador): # Atualiza o tabuleiro, após a colocação das peças nas coordenadas x e y indicadas.
    novo_tabuleiro = posiciona_peca(tabuleiro, x, y, jogador)

    # Atualiza as cores das peças capturadas, pela ESQUERDA.
    i = 2
    if x-1 >= 0:
        while x-i >= 0:
            if novo_tabuleiro[y][x - i] == jogador:
                j = 1
                if novo_tabuleiro[y][x - j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x-j, y, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pela DIREITA.
    i = 2
    if x+1 < DIMENSAOTABULEIRO:
        while x+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y][x + j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x+j, y, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, por CIMA.
    i = 2
    if y-1 >= 0:
        while y-i >= 0:
            if novo_tabuleiro[y - i][x] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x, y-j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, por BAIXO.
    i = 2
    if y+1 < DIMENSAOTABULEIRO:
        while y+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y + i][x] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x, y+j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pelo CANTO SUPERIOR ESQUERDO.
    i = 2
    if x-1 >= 0 and y-1 >= 0:
        while x-i >= 0 and y-i >= 0:
            if novo_tabuleiro[y - i][x - i] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x - j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x-j, y-j, jogador)
                    j = j+1
            i = i+1
    # Atualiza as cores das peças capturadas, pelo CANTO SUPERIOR DIREITO.
    i = 2
    if x+1 < DIMENSAOTABULEIRO and y-1 >= 0:
        while x+i < DIMENSAOTABULEIRO and y-i >= 0:
            if novo_tabuleiro[y - i][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x + j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x+j, y-j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pela CANTO INFERIOR ESQUERDO.
    i = 2
    if x-1 >= 0 and y+1 < DIMENSAOTABULEIRO:
        while x-i >= 0 and y+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y + i][x - i] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x - j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x-j, y+j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pela CANTO INFERIOR DIREITO.
    i = 2
    if x+1 < DIMENSAOTABULEIRO and y+1 < DIMENSAOTABULEIRO:
        while x+i < DIMENSAOTABULEIRO and y+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y + i][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x + j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x+j, y+j, jogador)
                    j = j+1
            i = i+1

    return novo_tabuleiro

def calcula_posicao(tabuleiro, x, y, jogador):
    if jogador == PRETO: # Verifica quem é o adversário.
        adversario = BRANCO
    else:
        adversario = PRETO

    random.shuffle(DIRECOES) # Escolhe a direção do teste para colocação de peça de forma aleatória, até encontrar alguma válida.

    for direcao in DIRECOES:
        # Abaixo, serão testadas as oito possíveis direções, para verificar se existe ao menos um lance válido.

        if direcao == ESQUERDA:
            i = 2 # Variável auxiliar, para percorrer as posições do tabuleiro (matriz 8x8) incrementando os índices.
            if x-1 >= 0 and tabuleiro[y][x-1] == adversario: # Busca uma posição válida para colocar a peça, pela ESQUERDA.
                while x-i >= 0:
                    if tabuleiro[y][x-i] == POSICAOVAZIA:
                        return (x-i,y)
                    elif tabuleiro[y][x-i] == jogador:
                        break # Encerra a busca nessa direção, pois não há lances válidos.
                    i = i+1

        elif direcao == DIREITA:
            i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
            if x+1 < DIMENSAOTABULEIRO and tabuleiro[y][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIREITA.
                while x+i < DIMENSAOTABULEIRO:
                    if tabuleiro[y][x+i] == POSICAOVAZIA:
                        return (x+i,y)
                    elif tabuleiro[y][x+i] == jogador:
                        break # Encerra a busca nessa direção, pois não há lances válidos.
                    i = i+1

        elif direcao == CIMA:
            i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
            if y-1 >= 0 and tabuleiro[y-1][x] == adversario: # Busca uma posição válida para colocar a peça, por CIMA.
                while y-i >= 0:
                    if tabuleiro[y-i][x] == POSICAOVAZIA:
                        return (x,y-i)
                    elif tabuleiro[y-i][x] == jogador:
                        break # Encerra a busca nessa direção, pois não há lances válidos.
                    i = i+1

        elif direcao == BAIXO:
            i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
            if y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x] == adversario: # Busca uma posição válida para colocar a peça, por BAIXO.
                while y+i < DIMENSAOTABULEIRO:
                    if tabuleiro[y+i][x] == POSICAOVAZIA:
                        return (x,y+i)
                    elif tabuleiro[y+i][x] == jogador:
                        break # Encerra a busca nessa direção, pois não há lances válidos.
                    i = i+1

        elif direcao == SUPERIORESQUERDA:
            i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
            if x-1 >= 0 and y-1 >= 0 and tabuleiro[y-1][x-1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR ESQUERDA.
                while x-i >= 0 and y-i >= 0:
                    if tabuleiro[y-i][x-i] == POSICAOVAZIA:
                        return (x-i,y-i)
                    elif tabuleiro[y-i][x-i] == jogador:
                        break # Encerra a busca nessa direção, pois não há lances válidos.
                    i = i+1

        elif direcao == SUPERIORDIREITA:
            i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
            if x+1 < DIMENSAOTABULEIRO and y-1 >= 0 and tabuleiro[y-1][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR DIREITA.
                while x+i < DIMENSAOTABULEIRO and y-i >= 0:
                    if tabuleiro[y-i][x+i] == POSICAOVAZIA:
                        return (x+i,y-i)
                    elif tabuleiro[y-i][x+i] == jogador:
                        break # Encerra a busca nessa direção, pois não há lances válidos.
                    i = i+1

        elif direcao == INFERIORESQUERDA:
            i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
            if x-i >= 0 and y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x-1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR ESQUERDA.
                while x-i >= 0 and y+i < DIMENSAOTABULEIRO:
                    if tabuleiro[y+i][x-i] == POSICAOVAZIA:
                        return (x-i,y+1)
                    elif tabuleiro[y+i][x-i] == jogador:
                        break # Encerra a busca nessa direção, pois não há lances válidos.
                    i = i+1

        elif direcao == INFERIORDIREITA:
            i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
            if x+1 < DIMENSAOTABULEIRO and y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR DIREITA.
                while x+i < DIMENSAOTABULEIRO and y+i < DIMENSAOTABULEIRO:
                    if tabuleiro[y+i][x+i] == POSICAOVAZIA:
                        return (x+i,y+i)
                    elif tabuleiro[y+i][x+i] == jogador:
                        break # Encerra a busca nessa direção, pois não há lances válidos.
                    i = i+1

def testa_valida(tabuleiro,jogador):
    for y in range(DIMENSAOTABULEIRO): # Percorre todas as posições do tabuleiro, para verificar se existe algum lance válido.
        for x in range(DIMENSAOTABULEIRO):
            if tabuleiro[y][x] == jogador:
                jogada = calcula_posicao(tabuleiro, x, y, jogador)
                if jogada != SEMJOGADAS:
                    return jogada

    return SEMJOGADAS

def main():
    print(testa_valida(POSICAOTESTE, PRETO))

start_time = time.time()
main()
print("\n--- TEMPO DE EXECUÇÃO: %s segundos ---\n" % (time.time() - start_time))
