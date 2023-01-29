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
POSICAOTESTE4 = ['WWWWWWWW', 'BBBBBBBB','........', '........', '........', '........', '........', '........']

POSICAOVAZIA = '.'
BRANCO = 'W'
PRETO = 'B'
EMPATE = 'D'
DIMENSAOTABULEIRO = 8
CONSTANTEUCB = math.sqrt(2)
SEMLANCES = (-1,-1)

TOTALSIMULACOES_INICIO = 300
TOTALSIMULACOES_MONTECARLO = 2300

class Nodo:  # Classe para armazenar todas as informações de cada nodo da árvore.
    def __init__(self, tabuleiro_,jogador_, vitorias_,jogadas_, pai_, filhos_, ucb_):
        self.tabuleiro = tabuleiro_
        self.jogador = jogador_
        self.vitorias = vitorias_
        self.jogadas = jogadas_
        self.pai = pai_
        self.filhos = filhos_
        self.ucb = ucb_

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
                lista_lances.append((x-i,y+i))
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

def selecao(raiz): # Realiza a etapa de SELEÇÃO do Monte Carlo Tree Search (MCTS).
    for filho in raiz.filhos:  # Iteração para atualizar o critério UCB de cada nodo filho.
        filho.ucb = calcula_ucb(filho)

    maior_ucb = raiz.filhos[0].ucb
    indice_aux = 0
    indice_melhor = 0

    for indice_aux in range(len(raiz.filhos)):  # Iteração para verificar qual nodo possui o melhor critério UCB (SELEÇÃO).
        if raiz.filhos[indice_aux].ucb > maior_ucb:
            maior_ucb = filho.ucb
            indice_melhor = indice_aux  # Faz a SELEÇÃO.

    # Retorna o índice que corresponde ao nodo da lista de filhos com o melhor critério UCB.
    return indice_melhor

def expansao(nodo):
    filhos = []
    lances = acha_lances(nodo.tabuleiro,nodo.jogador)

    if nodo.jogador == PRETO:
        proximo_jogador = BRANCO
    else:
        proximo_jogador = PRETO

    for coordenada in lances:
        proxima_posicao = atualiza_tabuleiro(nodo.tabuleiro,coordenada, nodo.jogador)
        filhos.append(Nodo(proxima_posicao.copy(),proximo_jogador,0,0,nodo,[],0))

    return filhos

def simulacao(raiz):
    nodo_aux = Nodo(raiz.tabuleiro,raiz.jogador,raiz.vitorias,raiz.jogadas,raiz.pai,raiz.filhos,raiz.ucb)

    while True: # Enquanto houver simulações possíveis, realiza os lances de forma aleatória.
        lances_possiveis = acha_lances(nodo_aux.tabuleiro,nodo_aux.jogador) # Calcula a lista com todos os lances possíveis, na posição atual.

        #print('TABULEIRO: ',nodo_aux.tabuleiro, ' JOGADOR: ', nodo_aux.jogador) # TESTE, REMOVER DEPOIS

        if lances_possiveis == []: # Determina se será necessário passar a vez ou encerrar o jogo.
             nodo_aux.jogador = acha_proximo(nodo_aux.jogador)  # Determina quem será o próximo jogador (branco ou preto).
             lances_possiveis = acha_lances(nodo_aux.tabuleiro,nodo_aux.jogador)  # Calcula a lista com todos os lances possíveis, na posição atual, passando a vez.
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
        novo_nodo = Nodo(novo_tabuleiro,proximo_jogador,0,0,nodo_aux,[],0)
        nodo_aux.filhos.append(novo_nodo)
        nodo_aux = novo_nodo

    resultado = acha_ganhador(nodo_aux.tabuleiro)
    #print('VENCEDOR: ', resultado)  # TESTE, REMOVER DEPOIS
    return resultado

def monte_carlo(raiz,jogador,oponente):
    simulacoes = 0
    while simulacoes < TOTALSIMULACOES_MONTECARLO:
        indice_melhor = selecao(raiz) # Etapa de SELEÇÃO do algoritmo Monte Carlo Tree Search (MCTS).
        vencedor = simulacao(raiz.filhos[indice_melhor]) # Etapa de SIMULAÇÃO do algoritmo Monte Carlo Tree Search (MCTS).
        simulacoes += 1
        # Etapa de RETROPROPAGAÇÃO do algoritmo Monte Carlo Tree Search (MCTS).
        raiz.jogadas += 1
        raiz.filhos[indice_melhor].jogadas += 1
        if vencedor == jogador:
            raiz.filhos[indice_melhor].vitorias += 1
        elif vencedor == oponente:
            raiz.filhos[indice_melhor].vitorias -= 1

    lista_lances = acha_lances(raiz.tabuleiro,jogador)
    return lista_lances[indice_melhor]

def make_move(tabuleiro, jogador):

    if acha_lances(tabuleiro,jogador) == []:
        return SEMLANCES

    raiz = Nodo(tabuleiro,jogador,0,TOTALSIMULACOES_INICIO,None,[],0)
    raiz.filhos = expansao(raiz) # Etapa de EXPANSÃO do algoritmo Monte Carlo Tree Search (MCTS).

    if jogador == PRETO:
        oponente = BRANCO
    else:
        oponente = PRETO

    simulacoes = 0 # Contador de simulacoes, para verificar se o limite foi atingido.

    while simulacoes < TOTALSIMULACOES_INICIO: # Iteração para realizar simulações até o limite desejado.
        for filho in raiz.filhos: # Percorre a lista de todos os filhos expandidos, realizando as simulações.
            vencedor = simulacao(filho) # Realiza algumas simulações iniciais, antes de aplicar o Monte Carlo Tree Search (MCTS).
            filho.jogadas += 1
            if vencedor == jogador:
                filho.vitorias += 1
            elif vencedor == oponente:
                filho.vitorias -= 1
            simulacoes += 1

    # Realiza as aplicações das etapas de SELEÇÃO, SIMULAÇÃO, EXPANSÃO e RETROPROPAGAÇÃO, após realizar as simulações iniciais.
    proximo_lance = monte_carlo(raiz,jogador,oponente) # Determina o próximo lance, com o algoritmo Monte Carlo Tree Search (MCTS).
    return proximo_lance # Retorna o próximo lance.

def teste_botbranco(): # TESTE, REMOVER DEPOIS

    tabuleiro = POSICAOINICIAL

    while True:
        lista_lancespreto = acha_lances(tabuleiro, PRETO)

        if (lista_lancespreto != []):
            proximo_lance = lista_lancespreto[0]
            tabuleiro = atualiza_tabuleiro(tabuleiro,proximo_lance,PRETO)
            print('TABULEIRO: ', tabuleiro, 'ULTIMO JOGADOR: ', PRETO)

        proximo_lance = make_move(tabuleiro,BRANCO)
        if (proximo_lance != SEMLANCES):
            tabuleiro = atualiza_tabuleiro(tabuleiro,proximo_lance,BRANCO)
            print('TABULEIRO: ', tabuleiro, 'ULTIMO JOGADOR: ', BRANCO)

        if (proximo_lance == SEMLANCES and lista_lancespreto == []):
            break

    resultado = acha_ganhador(tabuleiro)
    print('VENCEDOR: ', resultado)  # TESTE, REMOVER DEPOIS

    pretas = 0
    brancas = 0
    for y in range(DIMENSAOTABULEIRO): # Percorre todas as posições do tabuleiro, para verificar se existe algum lance válido.
        for x in range(DIMENSAOTABULEIRO):
            if tabuleiro[y][x] == PRETO:
                pretas += 1
            elif tabuleiro[y][x] == BRANCO:
                brancas += 1

    print(pretas,' x ',brancas)

def teste_botpreto(): # TESTE, REMOVER DEPOIS

    tabuleiro = POSICAOINICIAL

    while True:
        proximo_lance = make_move(tabuleiro,PRETO)
        if (proximo_lance != SEMLANCES):
            tabuleiro = atualiza_tabuleiro(tabuleiro,proximo_lance,PRETO)
            print('TABULEIRO: ', tabuleiro, 'ULTIMO JOGADOR: ', PRETO)

        lista_lancesbranco = acha_lances(tabuleiro, BRANCO)

        if (lista_lancesbranco != []):
            proximo_lance = lista_lancesbranco[0]
            tabuleiro = atualiza_tabuleiro(tabuleiro,proximo_lance,BRANCO)
            print('TABULEIRO: ', tabuleiro, 'ULTIMO JOGADOR: ', BRANCO)

        if (proximo_lance == SEMLANCES and lista_lancesbranco == []):
            break

    resultado = acha_ganhador(tabuleiro)
    print('VENCEDOR: ', resultado)  # TESTE, REMOVER DEPOIS

    pretas = 0
    brancas = 0
    for y in range(DIMENSAOTABULEIRO): # Percorre todas as posições do tabuleiro, para verificar se existe algum lance válido.
        for x in range(DIMENSAOTABULEIRO):
            if tabuleiro[y][x] == PRETO:
                pretas += 1
            elif tabuleiro[y][x] == BRANCO:
                brancas += 1

    print(pretas,' x ',brancas)

def main():
    #teste_botpreto() # TESTA COM O BOT ASSUMINDO AS PEÇAS PRETAS
    teste_botbranco() # TESTA COM O BOT ASSUMINDO AS PEÇAS BRANCAS

start_time = time.time()
main()
print("\n--- TEMPO DE EXECUÇÃO: %s segundos ---\n" % (time.time() - start_time))
