# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 2 - Monte Carlo Tree Search em Othello/Reversi

# Andrei Pochmann Koenich - Cartão 00308680
# Jean Smaniotto Argoud   - Cartão 00275602
# Willian Nunes Reichert  - Cartão 00134090

import copy
import math
import random
import time
from collections import OrderedDict
from typing import Tuple
from ..othello.gamestate import GameState

# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 2 - Monte Carlo Tree Search em Othello/Reversi

# Andrei Pochmann Koenich - Cartão 00308680
# Jean Smaniotto Argoud   - Cartão 00275602
# Willian Nunes Reichert  - Cartão 00134090

import copy
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

POSICAOVAZIA = '.'
BRANCO = 'W'
PRETO = 'B'
EMPATE = 'E'
VITORIA = 'V'
DERROTA = 'D'
DIMENSAOTABULEIRO = 8
CONSTANTEUCB = math.sqrt(2)
SEMLANCES = (-1, -1)

LIMITETEMPO = 4.50  # Limite do tempo de execução do Monte Carlo Tree Search (MCTS).


class Nodo:  # Classe para armazenar todas as informações de cada nodo da árvore.
    def __init__(self, tabuleiro_, jogador_, vitorias_, jogadas_, pai_, filhos_, ucb_):
        self.tabuleiro = tabuleiro_
        self.jogador = jogador_
        self.vitorias = vitorias_
        self.jogadas = jogadas_
        self.pai = pai_
        self.filhos = filhos_
        self.ucb = ucb_

def acha_ganhador(tabuleiro):  # Obtem um tabuleiro, e verifica qual dos dois jogadores venceu (ou se ocorreu empate).
    pecas_brancas = 0
    pecas_pretas = 0
    for y in range(DIMENSAOTABULEIRO):  # Percorre o tabuleiro, contando a quantidade de peças brancas e negras.
        for x in range(DIMENSAOTABULEIRO):
            if tabuleiro[y][x] == BRANCO:
                pecas_brancas = pecas_brancas + 1
            elif tabuleiro[y][x] == PRETO:
                pecas_pretas = pecas_pretas + 1

    if pecas_pretas == pecas_brancas:  # Retorna o jogador vencedor (ou empate).
        return EMPATE
    elif pecas_pretas > pecas_brancas:
        return PRETO
    else:
        return BRANCO

def acha_proximo(jogador):  # Determina quem será o próximo jogador da vez (branco ou preto).
    if jogador == PRETO:
        return BRANCO
    else:
        return PRETO

def calcula_ucb(nodo):  # Calcula o valor do critério UCB (Upper Confidence Bound), para um nodo da árvore.
    jogadas_filho = nodo.jogadas
    jogadas_pai = nodo.pai.jogadas

    if jogadas_filho == 0:
        jogadas_filho = 1

    if nodo.pai.jogadas == 0:
        jogadas_pai = 1

    # Cálculo segundo a fórmula vista em aula https://www.youtube.com/watch?v=sjRFGR-KQpc
    criterio_ucb = (nodo.vitorias / jogadas_filho) + (CONSTANTEUCB * math.sqrt((2 * math.log(jogadas_pai)) / jogadas_filho))
    return criterio_ucb

def posiciona_peca(tabuleiro, x, y, jogador):  # Insere a peça no tabuleiro, na posição indicada nas coordenadas x e y.
    novo_tabuleiro = tabuleiro.copy()  # Realiza uma cópia da posição passada como parâmetro, para atualizá-la.
    lista_aux = list(novo_tabuleiro[y])
    lista_aux[x] = jogador
    novo_tabuleiro[y] = ''.join(lista_aux)
    return novo_tabuleiro

def indice_aleatorio(lista):  # Recebe uma lista, e retorna um índice aleatório dela.
    return random.randint(0, len(lista) - 1)

def atualiza_tabuleiro(tabuleiro, coordenadas,jogador):  # Atualiza o tabuleiro, após a colocação das peças nas coordenadas x e y indicadas na dupla de coordenadas..
    x = coordenadas[0]  # Extração dos valores X e Y da tupla recebida como parâmetro.
    y = coordenadas[1]
    novo_tabuleiro = posiciona_peca(tabuleiro, x, y, jogador)  # Insere a nova peça no tabuleiro.

    # Abaixo, comandos de seleção para atualizar as cores das peças capturadas, em todas as direções.

    # Atualiza as cores das peças capturadas, pela ESQUERDA.
    i = 1  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x - 1 >= 0:
        while x - i >= 0 and novo_tabuleiro[y][x - i] != POSICAOVAZIA:
            if novo_tabuleiro[y][x - i] == jogador:
                j = 1
                while novo_tabuleiro[y][x - j] != jogador:
                    # print('ESQ')
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x - j, y, jogador)
                    j = j + 1
            i = i + 1

    # Atualiza as cores das peças capturadas, pela DIREITA.
    i = 1  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x + 1 < DIMENSAOTABULEIRO:
        while x + i < DIMENSAOTABULEIRO and novo_tabuleiro[y][x + i] != POSICAOVAZIA:
            if novo_tabuleiro[y][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y][x + j] != jogador:
                    # print('DIR')
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x + j, y, jogador)
                    j = j + 1
            i = i + 1

    # Atualiza as cores das peças capturadas, por CIMA.
    i = 1  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y - 1 >= 0:
        while y - i >= 0 and novo_tabuleiro[y - i][x] != POSICAOVAZIA:
            if novo_tabuleiro[y - i][x] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x] != jogador:
                    # print('CIMA')
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x, y - j, jogador)
                    j = j + 1
            i = i + 1

    # Atualiza as cores das peças capturadas, por BAIXO.
    i = 1  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y + 1 < DIMENSAOTABULEIRO:
        while y + i < DIMENSAOTABULEIRO and novo_tabuleiro[y + i][x] != POSICAOVAZIA:
            if novo_tabuleiro[y + i][x] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x] != jogador:
                    # print('BAIXO')
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x, y + j, jogador)
                    j = j + 1
            i = i + 1

    # Atualiza as cores das peças capturadas, pelo CANTO SUPERIOR ESQUERDO.
    i = 1  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x - 1 >= 0 and y - 1 >= 0:
        while x - i >= 0 and y - i >= 0 and novo_tabuleiro[y - i][x - i] != POSICAOVAZIA:
            if novo_tabuleiro[y - i][x - i] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x - j] != jogador:
                    # print('SUP ESQ')
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x - j, y - j, jogador)
                    j = j + 1
            i = i + 1
    # Atualiza as cores das peças capturadas, pelo CANTO SUPERIOR DIREITO.
    i = 1  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x + 1 < DIMENSAOTABULEIRO and y - 1 >= 0:
        while x + i < DIMENSAOTABULEIRO and y - i >= 0 and novo_tabuleiro[y - i][x + i] != POSICAOVAZIA:
            if novo_tabuleiro[y - i][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y - j][x + j] != jogador:
                    # print('SUP DIR')
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x + j, y - j, jogador)
                    j = j + 1
            i = i + 1

    # Atualiza as cores das peças capturadas, pelo CANTO INFERIOR ESQUERDO.
    i = 1  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x - 1 >= 0 and y + 1 < DIMENSAOTABULEIRO:
        while x - i >= 0 and y + i < DIMENSAOTABULEIRO and novo_tabuleiro[y + i][x - i] != POSICAOVAZIA:
            if novo_tabuleiro[y + i][x - i] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x - j] != jogador:
                    # print('INF ESQ')
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x - j, y + j, jogador)
                    j = j + 1
            i = i + 1

    # Atualiza as cores das peças capturadas, pelo CANTO INFERIOR DIREITO.
    i = 1  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x + 1 < DIMENSAOTABULEIRO and y + 1 < DIMENSAOTABULEIRO:
        while x + i < DIMENSAOTABULEIRO and y + i < DIMENSAOTABULEIRO and novo_tabuleiro[y + i][x + i] != POSICAOVAZIA:
            if novo_tabuleiro[y + i][x + i] == jogador:
                j = 1
                while novo_tabuleiro[y + j][x + j] != jogador:
                    # print('INF DIR')
                    novo_tabuleiro = posiciona_peca(novo_tabuleiro, x + j, y + j, jogador)
                    j = j + 1
            i = i + 1

    return novo_tabuleiro  # Retorna o tabuleiro atualizado, após as capturas de peças.


def calcula_lances(tabuleiro, x, y,jogador):  # Determina todos os lances possíveis de serem jogados, em uma certa posição, por um dos jogadores.
    if jogador == PRETO:  # Verifica quem é o adversário.
        adversario = BRANCO
    else:
        adversario = PRETO

    lista_lances = []  # Lista com todos os lances possíveis de serem feitos com a peça na posição indicada.

    # Abaixo, comandos de seleção para verificar todos os lances possíveis, em todas as direções.

    i = 2  # Variável auxiliar, para percorrer as posições do tabuleiro (matriz 8x8) incrementando os índices.
    if x - 1 >= 0 and tabuleiro[y][x - 1] == adversario:  # Busca uma posição válida para colocar a peça, pela ESQUERDA.
        while x - i >= 0:
            if tabuleiro[y][x - i] == POSICAOVAZIA:
                lista_lances.append((x - i, y))
                break
            elif tabuleiro[y][x - i] == jogador:
                break  # Encerra a busca nessa direção, pois não há lances válidos.
            i += 1

    i = 2  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x + 1 < DIMENSAOTABULEIRO and tabuleiro[y][
        x + 1] == adversario:  # Busca uma posição válida para colocar a peça, pela DIREITA.
        while x + i < DIMENSAOTABULEIRO:
            if tabuleiro[y][x + i] == POSICAOVAZIA:
                lista_lances.append((x + i, y))
                break
            elif tabuleiro[y][x + i] == jogador:
                break  # Encerra a busca nessa direção, pois não há lances válidos.
            i += 1

    i = 2  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y - 1 >= 0 and tabuleiro[y - 1][x] == adversario:  # Busca uma posição válida para colocar a peça, por CIMA.
        while y - i >= 0:
            if tabuleiro[y - i][x] == POSICAOVAZIA:
                lista_lances.append((x, y - i))
                break
            elif tabuleiro[y - i][x] == jogador:
                break  # Encerra a busca nessa direção, pois não há lances válidos.
            i += 1

    i = 2  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if y + 1 < DIMENSAOTABULEIRO and tabuleiro[y + 1][
        x] == adversario:  # Busca uma posição válida para colocar a peça, por BAIXO.
        while y + i < DIMENSAOTABULEIRO:
            if tabuleiro[y + i][x] == POSICAOVAZIA:
                lista_lances.append((x, y + i))
                break
            elif tabuleiro[y + i][x] == jogador:
                break  # Encerra a busca nessa direção, pois não há lances válidos.
            i += 1

    i = 2  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x - 1 >= 0 and y - 1 >= 0 and tabuleiro[y - 1][
        x - 1] == adversario:  # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR ESQUERDA.
        while x - i >= 0 and y - i >= 0:
            if tabuleiro[y - i][x - i] == POSICAOVAZIA:
                lista_lances.append((x - i, y - i))
                break
            elif tabuleiro[y - i][x - i] == jogador:
                break  # Encerra a busca nessa direção, pois não há lances válidos.
            i += 1

    i = 2  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x + 1 < DIMENSAOTABULEIRO and y - 1 >= 0 and tabuleiro[y - 1][
        x + 1] == adversario:  # Busca uma posição válida para colocar a peça, pela DIAGONAL SUPERIOR DIREITA.
        while x + i < DIMENSAOTABULEIRO and y - i >= 0:
            if tabuleiro[y - i][x + i] == POSICAOVAZIA:
                lista_lances.append((x + i, y - i))
                break
            elif tabuleiro[y - i][x + i] == jogador:
                break  # Encerra a busca nessa direção, pois não há lances válidos.
            i += 1

    i = 2  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x - 1 >= 0 and y + 1 < DIMENSAOTABULEIRO and tabuleiro[y + 1][
        x - 1] == adversario:  # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR ESQUERDA.
        while x - i >= 0 and y + i < DIMENSAOTABULEIRO:
            if tabuleiro[y + i][x - i] == POSICAOVAZIA:
                lista_lances.append((x - i, y + i))
                break
            elif tabuleiro[y + i][x - i] == jogador:
                break  # Encerra a busca nessa direção, pois não há lances válidos.
            i += 1

    i = 2  # Reinicia o valor da variável auxiliar para o próximo teste, em outra direção.
    if x + 1 < DIMENSAOTABULEIRO and y + 1 < DIMENSAOTABULEIRO and tabuleiro[y + 1][
        x + 1] == adversario:  # Busca uma posição válida para colocar a peça, pela DIAGONAL INFERIOR DIREITA.
        while x + i < DIMENSAOTABULEIRO and y + i < DIMENSAOTABULEIRO:
            if tabuleiro[y + i][x + i] == POSICAOVAZIA:
                lista_lances.append((x + i, y + i))
                break
            elif tabuleiro[y + i][x + i] == jogador:
                break  # Encerra a busca nessa direção, pois não há lances válidos.
            i += 1

    return lista_lances  # Retorna todas as listas

def acha_lances(tabuleiro, jogador):
    todas_jogadas = []  # Lista que conterá todas as jogadas possíveis, considerando o estado atual do tabuleiro e o jogador da vez.

    for y in range(DIMENSAOTABULEIRO):  # Percorre todas as posições do tabuleiro, para verificar se existe algum lance válido.
        for x in range(DIMENSAOTABULEIRO):
            if tabuleiro[y][x] == jogador:
                todas_jogadas += calcula_lances(tabuleiro, x, y, jogador)  # Armazena todas as jogadas possíveis, para o jogador da vez.

    lista_final = list(OrderedDict.fromkeys(todas_jogadas))  # Eliminação de jogadas repetidas, da lista de jogadas possíveis.
    return lista_final  # Retorna a lista com todas as jogadas possíveis.

def acha_indicemaiorUCB(lista_nodos):
    maior_ucb = lista_nodos[0].ucb
    indice_aux = 0
    indice_melhor = 0

    for indice_aux in range(len(lista_nodos)):  # Iteração para verificar qual nodo possui o melhor critério UCB (SELEÇÃO).
        if lista_nodos[indice_aux].ucb > maior_ucb:
            maior_ucb = lista_nodos[indice_aux].ucb
            indice_melhor = indice_aux  # Faz a SELEÇÃO.

    return indice_melhor
def selecao(raiz): # Realiza a etapa de SELEÇÃO do Monte Carlo Tree Search (MCTS).
    # Nodo auxiliar, para percorrer a árvore do jogo, da raiz até a folha.
    nodo_melhor = raiz

    while nodo_melhor.filhos != []:
        for filho in nodo_melhor.filhos:  # Iteração para atualizar o critério UCB de cada nodo filho.
            filho.ucb = calcula_ucb(filho)

        indice_melhor = acha_indicemaiorUCB(nodo_melhor.filhos)
        nodo_melhor = nodo_melhor.filhos[indice_melhor] # Desce um nível na árvore, ao fim de cada iteração.

    # Retorna o índice que corresponde ao nodo da lista de filhos com o melhor critério UCB.

    return nodo_melhor

def expansao(nodo):  # Realiza a etapa de EXPANSÃO do Monte Carlo Tree Search (MCTS).
    filhos = []  # Lista que irá conter todos os filhos do nodo atual do jogo.
    lances = acha_lances(nodo.tabuleiro, nodo.jogador)  # Determina todos os lances possíveis.

    if nodo.jogador == PRETO:  # Determina quem será o próximo jogador, depois dessa vez.
        proximo_jogador = BRANCO
    else:
        proximo_jogador = PRETO

    for coordenada in lances:
        proxima_posicao = atualiza_tabuleiro(nodo.tabuleiro, coordenada,nodo.jogador)  # Atualiza o tabuleiro com cada um dos lances possíveis, para armazenar os estados.
        filhos.append(Nodo(proxima_posicao.copy(), proximo_jogador, 0, 0, nodo, [],0))  # Armazena os estados possíveis do tabuleiro, para cada lance.

    return filhos  # Retorna a lista com todos os nodos filhos.

def simulacao(raiz):  # Realiza a etapa de SIMULAÇÃO do Monte Carlo Tree Search (MCTS).
    # Nodo auxiliar, para percorrer a árvore do jogo, da raiz até a folha.
    nodo_aux = copy.deepcopy(raiz)

    while True:  # Enquanto houver simulações possíveis, realiza os lances de forma aleatória (SIMULAÇÃO).
        lances_possiveis = acha_lances(nodo_aux.tabuleiro,nodo_aux.jogador)  # Calcula a lista com todos os lances possíveis, na posição atual.

        if lances_possiveis == []:  # Determina se será necessário passar a vez ou encerrar o jogo.
            nodo_aux.jogador = acha_proximo(nodo_aux.jogador)  # Determina quem será o próximo jogador (branco ou preto).
            lances_possiveis = acha_lances(nodo_aux.tabuleiro,nodo_aux.jogador)  # Calcula a lista com todos os lances possíveis, na posição atual, passando a vez.
            if lances_possiveis == []:
                break

        indice = indice_aleatorio(lances_possiveis)  # Determina um índice aleatório, da lista de lances possíveis.
        lance_aleatorio = lances_possiveis[indice]  # Determina um lance aleatório possível.
        novo_tabuleiro = atualiza_tabuleiro(nodo_aux.tabuleiro, lance_aleatorio,nodo_aux.jogador)  # Determina o estado do novo tabuleiro, com jogada aleatória.

        if nodo_aux.jogador == PRETO:  # Determina quem será o próximo jogador (branco ou preto).
            proximo_jogador = BRANCO
        else:
            proximo_jogador = PRETO

        # Atualiza as informações do novo nodo, obtidas na simulação com aleatoriedade.
        novo_nodo = Nodo(novo_tabuleiro, proximo_jogador, 0, 0, nodo_aux, [], 0)
        nodo_aux.filhos.append(novo_nodo)
        nodo_aux = novo_nodo

    resultado = acha_ganhador(nodo_aux.tabuleiro)  # Determina quem ganhou a partida, ou se a partida empatou.
    return resultado

def monte_carlo(raiz,jogador):
    tempo_inicio = time.time()
    while time.time()-tempo_inicio < LIMITETEMPO: # Enquanto não atingir o limite de tempo de execução, continua explorando o jogo.
        nodo_melhor = selecao(raiz) # Etapa de SELEÇÃO do algoritmo Monte Carlo Tree Search (MCTS).
        nodo_melhor.filhos = expansao(nodo_melhor) # Etapa de EXPANSÃO do algoritmo Monte Carlo Tree Search (MCTS).

        if (nodo_melhor.filhos == []):
            continue

        indice_simulacao = indice_aleatorio(nodo_melhor.filhos) # Escolhe, dentre os nós expandidos na EXPANSÃO, um nó aleatório para realizar a simulação.
        vencedor = simulacao(nodo_melhor.filhos[indice_simulacao]) # Etapa de SIMULAÇÃO do algoritmo Monte Carlo Tree Search (MCTS).

        while (nodo_melhor != None): # Etapa de RETROPROPAGAÇÃO do algoritmo Monte Carlo Tree Search (MCTS).
            nodo_melhor.jogadas += 1
            if vencedor != nodo_melhor.jogador and vencedor != EMPATE: # Incrementa o número de vitórias, encorajando o BOT a seguir o caminho.
                nodo_melhor.vitorias += 1 # Atualiza número de vitórias do FILHO.
            else:
                nodo_melhor.vitorias -= 1
            nodo_melhor = nodo_melhor.pai

    indice_melhor = acha_indicemaiorUCB(raiz.filhos)
    lista_lances = acha_lances(raiz.tabuleiro,jogador)
    return lista_lances[indice_melhor] # Retorna a tupla (x,y), contendo a melhor jogada.

def make_move(state: GameState) -> Tuple[int, int]:
    """
    Returns an Othello move
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    tabuleiro = state.board.tiles # Extração das informações relevantes para aplicar o Monte Carlo Tree Search (MCTS).
    jogador = state.player

    if acha_lances(tabuleiro, jogador) == []:  # Verifica se existe algum lance válido.
        return SEMLANCES

    raiz = Nodo(tabuleiro, jogador, 0, 0, None, [], 0)

    # Realiza as aplicações das etapas de SELEÇÃO, SIMULAÇÃO, EXPANSÃO e RETROPROPAGAÇÃO, após realizar as simulações iniciais.
    proximo_lance = monte_carlo(raiz, jogador)  # Determina o próximo lance, com o algoritmo Monte Carlo Tree Search (MCTS).
    return proximo_lance  # Retorna o próximo lance.