# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 2 - Poda alfa-beta ou MCTS em Othello/Reversi

# Andrei Pochmann Koenich - Cartão 00308680
# Jean Smaniotto Argoud   - Cartão 00275602
# Willian Nunes Reichert  - Cartão 00134090

import time

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
SEMJOGADAS = -1

class Nodo:  # Classe para armazenar todas as informações de cada nodo da árvore.
    def __init__(self, vitorias_,jogadas_, pai_, filhos_):
        self.vitorias = vitorias_
        self.jogadas = jogadas_
        self.pai = pai_
        self.filhos = filhos_

def testa_posicao(tabuleiro,x,y,jogador):
    if jogador == PRETO: # Verifica quem é o adversário.
        adversario = BRANCO
    else:
        adversario = PRETO

    # Abaixo, serão testadas as oito possíveis direçõs, para verificar se existe ao menos um lance válido.

    i = 2 # Variável auxiliar, para percorrer as posições do tabuleiro (matriz 8x8) incrementando os índices.
    if x-1 >= 0 and tabuleiro[x-1][y] == adversario: # Busca uma posição válida para colocar a peça, pela ESQUERDA.
        while x-i >= 0:
            if tabuleiro[x-i][y] == POSICAOVAZIA:
                return True # Retorna verdadeiro, indicando que achou um lance válido nessa direção.
            elif tabuleiro[x-i][y] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and tabuleiro[x+1][y] == adversario: # Busca uma posição válida para colocar a peça, pela DIREITA.
        while x+i < DIMENSAOTABULEIRO:
            if tabuleiro[x+i][y] == POSICAOVAZIA:
                return True # Retorna verdadeiro, indicando que achou um lance válido nessa direção.
            elif tabuleiro[x+i][y] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y-1 >= 0 and tabuleiro[x][y-1] == adversario: # Busca uma posição válida para colocar a peça, por CIMA.
        while y-i >= 0:
            if tabuleiro[x][y-i] == POSICAOVAZIA:
                return True # Retorna verdadeiro, indicando que achou um lance válido nessa direção.
            elif tabuleiro[x][y-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y+1 < DIMENSAOTABULEIRO and tabuleiro[x][y+1] == adversario: # Busca uma posição válida para colocar a peça, por BAIXO.
        while y+i < DIMENSAOTABULEIRO:
            if tabuleiro[x][y+i] == POSICAOVAZIA:
                return True # Retorna verdadeiro, indicando que achou um lance válido nessa direção.
            elif tabuleiro[x][y+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-1 >= 0 and y-1 >= 0 and tabuleiro[x-1][y-1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR ESQUERDA.
        while x-i >= 0 and y-i >= 0:
            if tabuleiro[x-i][y-i] == POSICAOVAZIA:
                return True # Retorna verdadeiro, indicando que achou um lance válido nessa direção.
            elif tabuleiro[x-i][y-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and y-1 >= 0 and tabuleiro[x+1][y-1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR DIREITA.
        while x+i < DIMENSAOTABULEIRO and y-i >= 0:
            if tabuleiro[x+i][y-i] == POSICAOVAZIA:
                return True # Retorna verdadeiro, indicando que achou um lance válido nessa direção.
            elif tabuleiro[x+i][y-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-i >= 0 and y+1 < DIMENSAOTABULEIRO and tabuleiro[x-1][y+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR ESQUERDA.
        while x-i >= 0 and y+i < DIMENSAOTABULEIRO:
            if tabuleiro[x-i][y+i] == POSICAOVAZIA:
                return True # Retorna verdadeiro, indicando que achou um lance válido nessa direção.
            elif tabuleiro[x-i][y+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and y+1 < DIMENSAOTABULEIRO and tabuleiro[x+1][y+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR DIREITA.
        while x+i < DIMENSAOTABULEIRO and y+i < DIMENSAOTABULEIRO:
            if tabuleiro[x+i][y+i] == POSICAOVAZIA:
                return True # Retorna verdadeiro, indicando que achou um lance válido nessa direção.
            elif tabuleiro[x+i][y+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    return False # Retorna falso, indicando que não há nenhum lance válido para o jogador.

def testa_valida(tabuleiro,jogador):
    for x in range(DIMENSAOTABULEIRO): # Percorre todas as posições do tabuleiro, para verificar se existe algum lance válido.
        for y in range(DIMENSAOTABULEIRO):
            if tabuleiro[x][y] == jogador and testa_posicao(tabuleiro,x,y,jogador) == True:
                return True

    return False

def main():
    print(testa_valida(POSICAOTESTE, BRANCO))
    print(testa_valida(POSICAOTESTE, PRETO))

start_time = time.time()
main()
print("\n--- TEMPO DE EXECUÇÃO: %s segundos ---\n" % (time.time() - start_time))
