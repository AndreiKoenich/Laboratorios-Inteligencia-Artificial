# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 2 - Poda alfa-beta ou MCTS em Othello/Reversi

# Andrei Pochmann Koenich - Cartão 00308680
# Jean Smaniotto Argoud   - Cartão 00275602
# Willian Nunes Reichert  - Cartão 00134090

import math
import random
import time
from collections import OrderedDict

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

POSICAOTESTE2 = ['BBBBBBBB', 'BBBBBBBB', 'BBBBWBWB', '..WWBBBB', '...WWBBB', '...WWBWB', '...WWWWB', '...WWWWB']
POSICAOTESTE3 = ['BBWWWWWW', 'WBWWBBWW', 'WWBWWWBW', 'WWBBWBBW', 'WWBBBWBW', 'WWBWBWBW', 'WWBBWWWW', '.WBBWW..']



POSICAOVAZIA = '.'
BRANCO = 'W'
PRETO = 'B'
EMPATE = 'D'
DIMENSAOTABULEIRO = 8
CONSTANTEUCB = math.sqrt(2)

class Nodo:  # Classe para armazenar todas as informações de cada nodo da árvore.
    def __init__(self, tabuleiro_,jogador_, vitorias_,jogadas_, pai_, filhos_):
        self.tabuleiro = tabuleiro_
        self.jogador = jogador_
        self.vitorias = vitorias_
        self.jogadas = jogadas_
        self.pai = pai_
        self.filhos = filhos_

def acha_ganhador(tabuleiro):
    pecas_brancas = 0
    pecas_pretas = 0
    for y in range(DIMENSAOTABULEIRO):
        for x in range(DIMENSAOTABULEIRO):
            if tabuleiro[y][x] == BRANCO:
                pecas_brancas = pecas_brancas+1
            elif tabuleiro[y][x] == PRETO:
                pecas_pretas = pecas_pretas+1

    if pecas_pretas == pecas_brancas:
        return EMPATE
    elif pecas_pretas > pecas_brancas:
        return PRETO
    else:
        return BRANCO

def acha_proximo(jogador):
    if jogador == PRETO:  # Determina quem será o próximo jogador (branco ou preto).
        return BRANCO
    else:
        return PRETO

def calcula_ucb (nodo): # Calcula o valor do critério UCB (Upper Confidence Bound), para um nodo da árvore.
    if nodo.jogadas == 0:
        return 0

    criterio_ucb = (nodo.vitorias/nodo.jogadas) + CONSTANTEUCB*math.sqrt((2*math.log(nodo.pai.jogadas))/nodo.jogadas)
    return criterio_ucb

def posiciona_peca(tabuleiro, x, y, jogador): # Insere a peça no tabuleiro, na posição indicada nas coordenadas x e y.
    novo_tabuleiro = tabuleiro.copy() # Realiza uma cópia da posição passada como parâmetro, para atualizá-la.
    lista_aux = list(novo_tabuleiro[y])
    lista_aux[x] = jogador
    novo_tabuleiro[y] = ''.join(lista_aux)
    return novo_tabuleiro

def indice_aleatorio(lista): # Recebe uma lista, e retorna um índice aleatório dela.
    return random.randint(0,len(lista)-1)

def atualiza_tabuleiro (tabuleiro, coordenadas, jogador): # Atualiza o tabuleiro, após a colocação das peças nas coordenadas x e y indicadas na dupla de coordenadas..
    x = coordenadas[0]
    y = coordenadas[1]
    novo_tabuleiro = posiciona_peca(tabuleiro, x, y, jogador)

    # Atualiza as cores das peças capturadas, pela ESQUERDA.
    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-1 >= 0:
        while x-i >= 0:
            if novo_tabuleiro[y][x - i] == jogador:
                j = 1
                if novo_tabuleiro[y][x - j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x-j, y, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pela DIREITA.
    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO:
        while x+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y][x + j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x+j, y, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, por CIMA.
    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y-1 >= 0:
        while y-i >= 0:
            if novo_tabuleiro[y - i][x] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x, y-j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, por BAIXO.
    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y+1 < DIMENSAOTABULEIRO:
        while y+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y + i][x] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x, y+j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pelo CANTO SUPERIOR ESQUERDO.
    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-1 >= 0 and y-1 >= 0:
        while x-i >= 0 and y-i >= 0:
            if novo_tabuleiro[y - i][x - i] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x - j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x-j, y-j, jogador)
                    j = j+1
            i = i+1
    # Atualiza as cores das peças capturadas, pelo CANTO SUPERIOR DIREITO.
    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and y-1 >= 0:
        while x+i < DIMENSAOTABULEIRO and y-i >= 0:
            if novo_tabuleiro[y - i][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x + j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x+j, y-j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pelo CANTO INFERIOR ESQUERDO.
    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-1 >= 0 and y+1 < DIMENSAOTABULEIRO:
        while x-i >= 0 and y+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y + i][x - i] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x - j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x-j, y+j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pelo CANTO INFERIOR DIREITO.
    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and y+1 < DIMENSAOTABULEIRO:
        while x+i < DIMENSAOTABULEIRO and y+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y + i][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x + j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x+j, y+j, jogador)
                    j = j+1
            i = i+1

    return novo_tabuleiro

def calcula_lances(tabuleiro, x, y, jogador):
    if jogador == PRETO: # Verifica quem é o adversário.
        adversario = BRANCO
    else:
        adversario = PRETO

    lista_lances = [] # Lista com todos os lances possíveis de serem feitos com a peça na posição indicada.

    i = 2 # Variável auxiliar, para percorrer as posições do tabuleiro (matriz 8x8) incrementando os índices.
    if x-1 >= 0 and tabuleiro[y][x-1] == adversario: # Busca uma posição válida para colocar a peça, pela ESQUERDA.
        while x-i >= 0:
            if tabuleiro[y][x-i] == POSICAOVAZIA:
                #print('ESQ')
                lista_lances.append((x-i,y))
                break
            elif tabuleiro[y][x-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and tabuleiro[y][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIREITA.
        while x+i < DIMENSAOTABULEIRO:
            if tabuleiro[y][x+i] == POSICAOVAZIA:
                #print('DIR')
                lista_lances.append((x+i,y))
                break
            elif tabuleiro[y][x+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y-1 >= 0 and tabuleiro[y-1][x] == adversario: # Busca uma posição válida para colocar a peça, por CIMA.
        while y-i >= 0:
            if tabuleiro[y-i][x] == POSICAOVAZIA:
                #print('CIMA')
                lista_lances.append((x,y-i))
                break
            elif tabuleiro[y-i][x] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x] == adversario: # Busca uma posição válida para colocar a peça, por BAIXO.
        while y+i < DIMENSAOTABULEIRO:
            if tabuleiro[y+i][x] == POSICAOVAZIA:
                #print('BAIXO')
                lista_lances.append((x,y+i))
                break
            elif tabuleiro[y+i][x] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-1 >= 0 and y-1 >= 0 and tabuleiro[y-1][x-1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR ESQUERDA.
        while x-i >= 0 and y-i >= 0:
            if tabuleiro[y-i][x-i] == POSICAOVAZIA:
                #print('SUP ESQ')
                lista_lances.append((x-i,y-i))
                break
            elif tabuleiro[y-i][x-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and y-1 >= 0 and tabuleiro[y-1][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR DIREITA.
        while x+i < DIMENSAOTABULEIRO and y-i >= 0:
            if tabuleiro[y-i][x+i] == POSICAOVAZIA:
                #print('SUP DIR')
                lista_lances.append((x+i,y-i))
                break
            elif tabuleiro[y-i][x+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-1 >= 0 and y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x-1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR ESQUERDA.
        while x-i >= 0 and y+i < DIMENSAOTABULEIRO:
            if tabuleiro[y+i][x-i] == POSICAOVAZIA:
                #print('INF ESQ')
                lista_lances.append((x-i,y+i))
                break
            elif tabuleiro[y+i][x-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR DIREITA.
        while x+i < DIMENSAOTABULEIRO and y+i < DIMENSAOTABULEIRO:
            if tabuleiro[y+i][x+i] == POSICAOVAZIA:
                #print('INF DIR')
                lista_lances.append((x+i,y+i))
                break
            elif tabuleiro[y+i][x+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    #print(x,y,lista_lances)
    return lista_lances

def acha_lances(tabuleiro, jogador):
    todas_jogadas = []

    for y in range(DIMENSAOTABULEIRO): # Percorre todas as posições do tabuleiro, para verificar se existe algum lance válido.
        for x in range(DIMENSAOTABULEIRO):
            if tabuleiro[y][x] == jogador:
                todas_jogadas += calcula_lances(tabuleiro, x,y, jogador) # Armazena todas as jogadas possíveis, para o jogador da vez.

    lista_final = list(OrderedDict.fromkeys(todas_jogadas)) # Eliminação de jogadas repetidas.
    return lista_final # Retorna a lista com todas as jogadas possíveis.

def expansao(nodo):
    filhos = []
    lances = acha_lances(nodo.tabuleiro,nodo.jogador)

    if nodo.jogador == PRETO:
        proximo_jogador = BRANCO
    else:
        proximo_jogador = PRETO

    for coordenada in lances:
        proxima_posicao = atualiza_tabuleiro(nodo.tabuleiro,coordenada, nodo.jogador)
        filhos.append(Nodo(proxima_posicao.copy(),proximo_jogador,0,0,nodo,[]))

    return filhos

def simulacao(raiz):
    nodo_aux = raiz
    novo_nodo = Nodo('', '', 0, 0, nodo_aux, [])

    while True: # Enquanto houver simulações possíveis, realiza os lances de forma aleatória.
        lances_possiveis = acha_lances(nodo_aux.tabuleiro,nodo_aux.jogador) # Calcula a lista com todos os lances possíveis, na posição atual.

        print('TABULEIRO: ',nodo_aux.tabuleiro, ' JOGADOR: ', nodo_aux.jogador) # TESTE, REMOVER DEPOIS

        if lances_possiveis == []: # Determina se será necessário passar a vez ou encerrar o jogo.
             nodo_aux.jogador = acha_proximo(nodo_aux.jogador)  # Determina quem será o próximo jogador (branco ou preto).
             lances_possiveis = acha_lances(nodo_aux.tabuleiro,nodo_aux.jogador)  # Calcula a lista com todos os lances possíveis, na posição atual.
             if lances_possiveis == []:
                 break

        indice = indice_aleatorio(lances_possiveis)
        lance_aleatorio = lances_possiveis[indice] # Determina um lance aleatório possível.
        novo_tabuleiro = atualiza_tabuleiro(nodo_aux.tabuleiro,lance_aleatorio,nodo_aux.jogador) # Determina o estado do novo tabuleiro, com jogada aleatória.

        if nodo_aux.jogador == PRETO: # Determina quem será o próximo jogador (branco ou preto).
            proximo_jogador = BRANCO
        else:
            proximo_jogador = PRETO

        # Atualiza as informações do novo nodo, obtidas na simulação com aleatoriedade.
        novo_nodo = Nodo(novo_tabuleiro,proximo_jogador,0,0,nodo_aux,[])
        nodo_aux.filhos.append(novo_nodo)
        nodo_aux = novo_nodo

    print('VENCEDOR: ', acha_ganhador(nodo_aux.tabuleiro))  # TESTE, REMOVER DEPOIS

    return raiz

def inicia_programa():
    raiz = Nodo(POSICAOINICIAL,PRETO,0,0,None,[])
    raiz = simulacao(raiz)

def main():
    inicia_programa()

start_time = time.time()
main()
print("\n--- TEMPO DE EXECUÇÃO: %s segundos ---\n" % (time.time() - start_time))
