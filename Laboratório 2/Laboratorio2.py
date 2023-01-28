# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 2 - Poda alfa-beta ou MCTS em Othello/Reversi

# Andrei Pochmann Koenich - Cartão 00308680
# Jean Smaniotto Argoud   - Cartão 00275602
# Willian Nunes Reichert  - Cartão 00134090

import time
import math

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

def testa_final (tabuleiro): # Verifica se o jogo acabou.
    if (acha_lances(tabuleiro, BRANCO) == [] and acha_lances(tabuleiro, PRETO) == []):
        return True
    return False

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

def atualiza_tabuleiro (tabuleiro, coordenadas, jogador): # Atualiza o tabuleiro, após a colocação das peças nas coordenadas x e y indicadas na dupla de coordenadas..
    x = coordenadas[0]
    y = coordenadas[1]
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

    # Atualiza as cores das peças capturadas, pelo CANTO INFERIOR ESQUERDO.
    i = 2
    if x-1 >= 0 and y+1 < DIMENSAOTABULEIRO:
        while x-i >= 0 and y+i < DIMENSAOTABULEIRO:
            if novo_tabuleiro[y + i][x - i] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x - j] != jogador:
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x-j, y+j, jogador)
                    j = j+1
            i = i+1

    # Atualiza as cores das peças capturadas, pelo CANTO INFERIOR DIREITO.
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
                lista_lances.append((x-i,y))
                break
            elif tabuleiro[y][x-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and tabuleiro[y][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIREITA.
        while x+i < DIMENSAOTABULEIRO:
            if tabuleiro[y][x+i] == POSICAOVAZIA:
                lista_lances.append((x+i,y))
                break
            elif tabuleiro[y][x+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y-1 >= 0 and tabuleiro[y-1][x] == adversario: # Busca uma posição válida para colocar a peça, por CIMA.
        while y-i >= 0:
            if tabuleiro[y-i][x] == POSICAOVAZIA:
                lista_lances.append((x,y-i))
                break
            elif tabuleiro[y-i][x] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x] == adversario: # Busca uma posição válida para colocar a peça, por BAIXO.
        while y+i < DIMENSAOTABULEIRO:
            if tabuleiro[y+i][x] == POSICAOVAZIA:
                lista_lances.append((x,y+i))
                break
            elif tabuleiro[y+i][x] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-1 >= 0 and y-1 >= 0 and tabuleiro[y-1][x-1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR ESQUERDA.
        while x-i >= 0 and y-i >= 0:
            if tabuleiro[y-i][x-i] == POSICAOVAZIA:
                lista_lances.append((x-i,y-i))
                break
            elif tabuleiro[y-i][x-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and y-1 >= 0 and tabuleiro[y-1][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR DIREITA.
        while x+i < DIMENSAOTABULEIRO and y-i >= 0:
            if tabuleiro[y-i][x+i] == POSICAOVAZIA:
                lista_lances.append((x+i,y-i))
                break
            elif tabuleiro[y-i][x+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x-1 >= 0 and y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x-1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR ESQUERDA.
        while x-i >= 0 and y+i < DIMENSAOTABULEIRO:
            if tabuleiro[y+i][x-i] == POSICAOVAZIA:
                lista_lances.append((x-i,y+1))
                break
            elif tabuleiro[y+i][x-i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    i = 2 # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x+1 < DIMENSAOTABULEIRO and y+1 < DIMENSAOTABULEIRO and tabuleiro[y+1][x+1] == adversario: # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR DIREITA.
        while x+i < DIMENSAOTABULEIRO and y+i < DIMENSAOTABULEIRO:
            if tabuleiro[y+i][x+i] == POSICAOVAZIA:
                lista_lances.append((x+i,y+i))
                break
            elif tabuleiro[y+i][x+i] == jogador:
                break # Encerra a busca nessa direção, pois não há lances válidos.
            i = i+1

    return lista_lances

def acha_lances(tabuleiro, jogador):
    todas_jogadas = []

    for y in range(DIMENSAOTABULEIRO): # Percorre todas as posições do tabuleiro, para verificar se existe algum lance válido.
        for x in range(DIMENSAOTABULEIRO):
            if tabuleiro[y][x] == jogador:
                todas_jogadas += calcula_lances(tabuleiro, x,y, jogador) # Armazena todas as jogadas possíveis, para o jogador da vez.

    return todas_jogadas # Retorna a lista com todas as jogadas possíveis.

def calcula_filhos(nodo):
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

def inicia_programa():
    raiz = Nodo(POSICAOINICIAL,PRETO,0,0,None,[])
    raiz.filhos = calcula_filhos(raiz)
    print(raiz.tabuleiro)
    print(acha_ganhador(POSICAOINICIAL))


def main():
    inicia_programa()

start_time = time.time()
main()
print("\n--- TEMPO DE EXECUÇÃO: %s segundos ---\n" % (time.time() - start_time))
