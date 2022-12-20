# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 1 - Busca em Grafos

# Andrei Pochmann Koenich - Cartao 00308680
# Jean Smaniotto Argoud   - Cartao 00275602
# Willian Nunes Reichert  - Cartao 00134090

import heapq

SIMBOLOBRANCO = '_'  # Constante para indicar o espaco em branco no tabuleiro do 8-puzzle.
POSICAOINICIAL = '2_3541687'  # Constante para representar o estado inicial.
OBJETIVO = '12345678_'  # Constante para representar o objetivo do jogo.
CUSTOINICIAL = 0  # Custo inicial do nodo referente a primeira posicao.

TEXTOCIMA = 'acima'
TEXTOBAIXO = 'abaixo'
TEXTOESQUERDA = 'esquerda'
TEXTODIREITA = 'direita'

PRIMEIRAPOSICAO = 0
SEGUNDAPOSICAO = 1
TERCEIRAPOSICAO = 2
QUARTAPOSICAO = 3
QUINTAPOSICAO = 4
SEXTAPOSICAO = 5
SETIMAPOSICAO = 6
OITAVAPOSICAO = 7
NONAPOSICAO = 8
TOTALPOSICOES = 9

TESTE = False


class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado, pai, acao, custo, heuristica=0):
        """
        Inicializa o nodo com os atributos recebidos
        :param str estado: representacao do estado do 8-puzzle
        :param Nodo|None pai: referencia ao nodo pai (None no caso do nó raiz)
        :param str|None acao: acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param int custo: custo do caminho da raiz até este nó
        :param int heuristica: (extra) heurística deste nó até o nó objetivo
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.heuristica = heuristica

    def __lt__(self, outro):
        """
        Override do método de comparação 'menor que' para que a gerência da fila de prioridades utilizada nos dois
        métodos A* consiga manter a ordenação dos seus nós
        :param Nodo outro: nó a ser comparado com este
        :return bool: verdadeiro se o custo total f(v) é menor que o custo total f(outro)
        """
        return (self.custo + self.heuristica) < (outro.custo + outro.heuristica)


def movimenta_branco(estado, posicao_branco, posicao_numero):
    """
    Troca o branco e um número de posição no estado do puzzle.
    :param str estado: estado do puzzle
    :param int posicao_branco: posição do branco no estado
    :param int posicao_numero: posição do número no estado
    :return: o estado com as posições trocadas
    """
    lista_posicao = list(estado)
    lista_posicao[posicao_branco], lista_posicao[posicao_numero] = lista_posicao[posicao_numero], lista_posicao[
        posicao_branco]
    novo_estado = ''.join(lista_posicao)
    return novo_estado


def valida_texto(estado):
    """
    Verifica se o texto que representa o estado do puzzle é válido.
    :param str estado: o estado do puzzle a ser verificado
    :return: verdadeiro se o estado é válido
    """
    if len(estado) != TOTALPOSICOES:  # Testa se o estado possui nove caracteres.
        return False

    if len(set(estado)) != len(estado):  # Testa se existem elementos repetidos.
        return False

    for digito in estado:  # Testa se todos os caracteres são dígitos de 1 a 8 ou espaços em branco.
        if digito == '0' or digito == '9':
            return False
        elif not digito.isdigit() and digito != SIMBOLOBRANCO:
            return False

    return True


def valida_posicao(estado):
    """
    Verifica de a posição de entrada do puzzle possui solução viável.
    Baseado em https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
    :param str estado: o estado do puzzle a ser verificado
    :return: verdadeiro se o estado inicial puder levar a uma solução
    """
    conta_inversoes = 0

    for i in range(len(estado)):  # Iterações para contar o número de inversões no tabuleiro.
        for j in range(i + 1, TOTALPOSICOES):
            if estado[i] != SIMBOLOBRANCO and estado[j] != SIMBOLOBRANCO and estado[i] > estado[j]:
                conta_inversoes += 1

    return conta_inversoes % 2 == 0  # Se o número de inversões é par, então o tabuleiro possui solução válida.


def sucessor(estado):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido) para cada ação possível no estado
    recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param str estado: estado do puzzle
    :return: lista de ações e estados atingidos através delas
    """
    movimentos = []  # Inicializa a lista contendo as tuplas que indicam os movimentos.
    posicao_branco = estado.rfind(SIMBOLOBRANCO)  # Encontra a posicao do espaco vazio no tabuleiro.

    # Comandos de selecao para verificar como movimentar o espaco em branco.
    if posicao_branco == PRIMEIRAPOSICAO:
        movimentos.append((TEXTODIREITA, movimenta_branco(estado, PRIMEIRAPOSICAO, SEGUNDAPOSICAO)))
        movimentos.append((TEXTOBAIXO, movimenta_branco(estado, PRIMEIRAPOSICAO, QUARTAPOSICAO)))

    elif posicao_branco == SEGUNDAPOSICAO:
        movimentos.append((TEXTOESQUERDA, movimenta_branco(estado, SEGUNDAPOSICAO, PRIMEIRAPOSICAO)))
        movimentos.append((TEXTOBAIXO, movimenta_branco(estado, SEGUNDAPOSICAO, QUINTAPOSICAO)))
        movimentos.append((TEXTODIREITA, movimenta_branco(estado, SEGUNDAPOSICAO, TERCEIRAPOSICAO)))

    elif posicao_branco == TERCEIRAPOSICAO:
        movimentos.append((TEXTOESQUERDA, movimenta_branco(estado, TERCEIRAPOSICAO, SEGUNDAPOSICAO)))
        movimentos.append((TEXTOBAIXO, movimenta_branco(estado, TERCEIRAPOSICAO, SEXTAPOSICAO)))

    elif posicao_branco == QUARTAPOSICAO:
        movimentos.append((TEXTOCIMA, movimenta_branco(estado, QUARTAPOSICAO, PRIMEIRAPOSICAO)))
        movimentos.append((TEXTODIREITA, movimenta_branco(estado, QUARTAPOSICAO, QUINTAPOSICAO)))
        movimentos.append((TEXTOBAIXO, movimenta_branco(estado, QUARTAPOSICAO, SETIMAPOSICAO)))

    elif posicao_branco == QUINTAPOSICAO:
        movimentos.append((TEXTOCIMA, movimenta_branco(estado, QUINTAPOSICAO, SEGUNDAPOSICAO)))
        movimentos.append((TEXTOESQUERDA, movimenta_branco(estado, QUINTAPOSICAO, QUARTAPOSICAO)))
        movimentos.append((TEXTODIREITA, movimenta_branco(estado, QUINTAPOSICAO, SEXTAPOSICAO)))
        movimentos.append((TEXTOBAIXO, movimenta_branco(estado, QUINTAPOSICAO, OITAVAPOSICAO)))

    elif posicao_branco == SEXTAPOSICAO:
        movimentos.append((TEXTOCIMA, movimenta_branco(estado, SEXTAPOSICAO, TERCEIRAPOSICAO)))
        movimentos.append((TEXTOESQUERDA, movimenta_branco(estado, SEXTAPOSICAO, QUINTAPOSICAO)))
        movimentos.append((TEXTOBAIXO, movimenta_branco(estado, SEXTAPOSICAO, NONAPOSICAO)))

    elif posicao_branco == SETIMAPOSICAO:
        movimentos.append((TEXTOCIMA, movimenta_branco(estado, SETIMAPOSICAO, QUARTAPOSICAO)))
        movimentos.append((TEXTODIREITA, movimenta_branco(estado, SETIMAPOSICAO, OITAVAPOSICAO)))

    elif posicao_branco == OITAVAPOSICAO:
        movimentos.append((TEXTOESQUERDA, movimenta_branco(estado, OITAVAPOSICAO, SETIMAPOSICAO)))
        movimentos.append((TEXTOCIMA, movimenta_branco(estado, OITAVAPOSICAO, QUINTAPOSICAO)))
        movimentos.append((TEXTODIREITA, movimenta_branco(estado, OITAVAPOSICAO, NONAPOSICAO)))

    elif posicao_branco == NONAPOSICAO:
        movimentos.append((TEXTOCIMA, movimenta_branco(estado, NONAPOSICAO, SEXTAPOSICAO)))
        movimentos.append((TEXTOESQUERDA, movimenta_branco(estado, NONAPOSICAO, OITAVAPOSICAO)))

    return movimentos


def expande(nodo):
    """
    Gera os nós sucessores do nó passado como parâmetro.
    :param Nodo nodo: objeto da classe Nodo
    :return: um iterable de nós sucessores
    """
    acoes = sucessor(nodo.estado)  # Obtem todas as movimentacoes possiveis no tabuleiro.
    lista_nodos = []  # Inicializa a lista contendo os nodos a serem retornados.

    for i in range(len(acoes)):
        novo_nodo = Nodo(acoes[i][1], nodo, acoes[i][0], nodo.custo + 1)
        lista_nodos.append(novo_nodo)

    return lista_nodos  # Retorna os novos nodos expandidos, em uma lista.


def bfs(estado):
    """
    Recebe um estado (string), executa a busca em LARGURA e retorna uma lista de ações que leva do estado recebido até
    o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param str estado: estado inicial do puzzle
    :return: uma lista de ações que leva ao estado objetivo, ou None
    """
    if valida_texto(estado) is False:  # Verifica se o texto representando a posição inicial do puzzle é válido.
        return None
    if valida_posicao(estado) is False:  # Verifica se a posição de entrada do puzzle possui solução viável.
        return None

    explorados = {}  # Dicionário contendo os nós explorados. O estado do tabuleiro será usado como identificador.
    raiz = Nodo(estado, None, None, CUSTOINICIAL)  # Raiz com o estado inicial do tabuleiro.
    fronteira = [raiz]  # FILA que representa a fronteira.
    movimentos = []  # Lista contendo os movimentos do estado inicial até a solução.

    while True:  # Iteração principal para realizar a busca em largura.

        if fronteira is []:  # Se a fronteira estiver vazia, então nenhuma solução foi encontrada.
            return None

        v = fronteira.pop(0)  # Remove o PRIMEIRO elemento adicionado na FILA (FIFO - first in, first out).

        if v.estado == OBJETIVO:  # Caso em que foi encontrada a solução.
            if TESTE:
                print(f"[bfs] expandidos: {len(explorados)} nós")
            while v.pai is not None:  # Iteração para resgatar o caminho de ações do estado inicial até a solução.
                movimentos.append(v.acao)
                v = v.pai
            movimentos.reverse()
            return movimentos  # Retorna a lista de movimentos para concluir o jogo.

        if v.estado not in explorados:  # Se o estado ainda nao foi explorado:
            explorados[v.estado] = v  # Adiciona o estado de v aos explorados.
            fronteira += expande(v)  # Adiciona todos os vizinhos de v na fronteira.


def dfs(estado):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e retorna uma lista de ações que leva do estado recebido
    até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param str estado: estado inicial do puzzle
    :return: uma lista de ações que leva ao estado objetivo, ou None
    """
    if valida_texto(estado) is False:  # Verifica se o texto (string) representando a posição do puzzle é válido.
        return None
    if valida_posicao(estado) is False:  # Verifica se a posição de entrada do puzzle possui solução viável.
        return None

    explorados = {}  # Dicionário contendo os nós explorados. O estado do tabuleiro será usado como identificador.
    raiz = Nodo(estado, None, None, CUSTOINICIAL)  # Raiz com o estado inicial do tabuleiro.
    fronteira = [raiz]  # PILHA que representa a fronteira.
    movimentos = []  # Lista contendo os movimentos do estado inicial até a solução.

    while True:  # Iteração principal para realizar a busca em profundidade.

        if fronteira is []:  # Se a fronteira estiver vazia, então nenhuma solução foi encontrada.
            return None

        v = fronteira.pop()  # Remove o ÚLTIMO elemento adicionado na PILHA (LIFO - last in, first out).

        if v.estado == OBJETIVO:  # Caso em que foi encontrada a solução.
            if TESTE:
                print(f"[dfs] expandidos: {len(explorados)} nós")
            while v.pai is not None:  # Iteração para resgatar o caminho de ações do estado inicial até a solução.
                movimentos.append(v.acao)
                v = v.pai
            movimentos.reverse()
            return movimentos  # Retorna a lista de movimentos para concluir o jogo.

        if v.estado not in explorados:  # Se o estado ainda não foi explorado:
            explorados[v.estado] = v  # Adiciona o estado de v aos explorados.
            fronteira += expande(v)  # Adiciona todos os vizinhos de v na fronteira.


def heuristica_hamming(estado):
    """
    Retorna o valor referente à heurística distância de Hamming, equivalente à quantidade de peças fora do lugar.
    A contagem é feita comparando a string do estado com a string do estado objetivo.
    :param str estado: estado a ser utilizado no cálculo
    :return: a distância de Hamming do estado
    """
    return sum([estado[i] != OBJETIVO[i] for i in range(len(estado))])


def astar_hamming(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e retorna uma lista de ações
    que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param str estado: estado inicial do puzzle
    :return: uma lista de ações que leva ao estado objetivo, ou None
    """
    if valida_texto(estado) is False:  # Verifica se o texto (string) representando a posi~çao do puzzle é válido.
        return None
    if valida_posicao(estado) is False:  # Verifica se a posição de entrada do puzzle possui solução viável.
        return None

    explorados = {}  # Dicionário contendo os nós explorados. O estado do tabuleiro será usado como identificador.
    raiz = Nodo(estado, None, None, CUSTOINICIAL, heuristica_hamming(estado))  # Raiz com o estado inicial do tabuleiro.
    fronteira = [raiz]  # FILA DE PRIORIDADES que representa a fronteira.
    movimentos = []  # Inicialização da lista contendo os movimentos do estado inicial até a solução.

    while True:  # Iteração principal para realizar a busca com A* (com a heuristica da distancia de Hamming).

        if fronteira is []:  # Se a fronteira estiver vazia, então nenhuma solução foi encontrada.
            return None

        v = heapq.heappop(fronteira)  # Remove o elemento que possui o MENOR CUSTO TOTAL (custo + hamming(estado)).

        if v.estado == OBJETIVO:  # Caso em que foi encontrada a solução.
            if TESTE:
                print(f"[astar_hamming] expandidos: {len(explorados)} nós")
            while v.pai is not None:  # Iteração para resgatar o caminho de ações do estado inicial até a solução.
                movimentos.append(v.acao)
                v = v.pai
            movimentos.reverse()
            return movimentos  # Retorna a lista de movimentos para concluir o jogo.

        if v.estado not in explorados:  # Atualiza a árvore heap com os novos nós.
            explorados[v.estado] = v
            for nodo in expande(v):  # Adiciona todos os vizinhos de v na fronteira.
                nodo.heuristica = heuristica_hamming(nodo.estado)
                heapq.heappush(fronteira, nodo)


def heuristica_manhattan(estado):
    """
    Retorna o valor referente à heurística distância de Manhattan, equivalente à quantidade de peças fora do lugar.
      Considerando o estado "2_3541687", ele será representado pela lista [1 -1 2 4 3 0 5 7 6], na qual cada número foi
    subtraído de 1 para que ele também passe a representar sua posição objetivo na lista.
      Separando a lista em [ 1 -1 2 | 4 3 0 | 5 7 6 ], temos três blocos que representam as três linhas horizontais do
    tabuleiro. Assim, abs(posicao % 3 - valor % 3) indica quantos movimentos na horizontal o número deverá realizar para
    chegar na sua coluna, e abs(posicao // 3 - valor // 3) indica quantos movimentos na vertical o número deverá
    realizar para chegar na sua linha. A soma desses dois resultados nos dá a distância de Manhattan do número.
    :param str estado: estado a ser utilizado no cálculo
    :return: a distância de Manhattan do estado
    """
    tabuleiro_lista = []
    tabuleiro_lista[:0] = estado  # Converte a string representando o tabuleiro em uma lista.
    tabuleiro_lista[tabuleiro_lista.index(SIMBOLOBRANCO)] = '0'  # Altera o caractere da posição em branco para zero.

    for i in range(len(tabuleiro_lista)):  # Converte cada caractere representando as pecas em valores inteiros.
        tabuleiro_lista[i] = int(tabuleiro_lista[i]) - 1

    # Percorre o tabuleiro calculando as distâncias de cada peça e somando.
    distancia_manhattan = 0
    for posicao, valor in enumerate(tabuleiro_lista):
        if valor < 0:
            continue
        distancia_manhattan += abs(posicao % 3 - valor % 3) + abs(posicao // 3 - valor // 3)
    return distancia_manhattan  # Retorna o valor referente à heurística da distâcia Manhattan.


def astar_manhattan(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e retorna uma lista de
    ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param str estado: estado inicial do puzzle
    :return: uma lista de ações que leva ao estado objetivo, ou None
    """
    if valida_texto(estado) is False:  # Verifica se o texto (string) representando a posição do puzzle é válido.
        return None
    if valida_posicao(estado) is False:  # Verifica se a posição de entrada do puzzle possui solução viável.
        return None

    explorados = {}  # Dicionário contendo os nós explorados. O estado do tabuleiro será usado como identificador.
    raiz = Nodo(estado, None, None, CUSTOINICIAL, heuristica_manhattan(estado))  # Raiz com o estado inicial.
    fronteira = [raiz]  # FILA DE PRIORIDADES que representa a fronteira.
    movimentos = []  # Inicialização da lista contendo os movimentos do estado inicial até a solução.

    while True:  # Iteração principal para realizar a busca com A* (com a heuristica da distancia Manhattan).

        if fronteira is []:  # Se a fronteira estiver vazia, então nenhuma solução foi encontrada.
            return None

        v = heapq.heappop(fronteira)  # Remove o elemento que possui o MENOR CUSTO TOTAL (custo + manhattan(estado)).

        if v.estado == OBJETIVO:  # Caso em que foi encontrada a solução.
            if TESTE:
                print(f"[astar_manhattan] expandidos: {len(explorados)} nós")
            while v.pai is not None:  # Iteração para resgatar o caminho de ações do estado inicial até a solução.
                movimentos.append(v.acao)
                v = v.pai
            movimentos.reverse()
            return movimentos  # Retorna a lista de movimentos para concluir o jogo.

        if v.estado not in explorados:  # Atualiza a árvore heap com os novos nós.
            explorados[v.estado] = v
            for nodo in expande(v):  # Adiciona todos os vizinhos de v na fronteira.
                nodo.heuristica = heuristica_manhattan(nodo.estado)
                heapq.heappush(fronteira, nodo)


if __name__ == "__main__":
    """
    Código utilizado para coletar os dados necessários para cada algoritmo de busca.
    Para o cálculo do tempo de execução, são realizadas múltiplas execuções a fim de obter um tempo médio, visto que o
    tempo resultante entre execuções separadas pode ser bem diferente.
    A flag TESTE serve para habilitar logs dentro das funções que executam os algoritmos.
    """
    import time

    EXECUCOES = 25
    tempo = 0
    for k in range(EXECUCOES):
        instante = time.perf_counter()
        bfs('2_3541687')
        tempo += time.perf_counter() - instante
    tempo_bfs = tempo/EXECUCOES

    tempo = 0
    for k in range(EXECUCOES):
        instante = time.perf_counter()
        dfs('2_3541687')
        tempo += time.perf_counter() - instante
    tempo_dfs = tempo/EXECUCOES

    tempo = 0
    for k in range(EXECUCOES):
        instante = time.perf_counter()
        astar_hamming('2_3541687')
        tempo += time.perf_counter() - instante
    tempo_astar_hamming = tempo/EXECUCOES

    tempo = 0
    for k in range(EXECUCOES):
        instante = time.perf_counter()
        astar_manhattan('2_3541687')
        tempo += time.perf_counter() - instante
    tempo_astar_manhattan = tempo/EXECUCOES

    TESTE = True
    print(f"[bfs] custo: {len(bfs('2_3541687'))} movimentos")
    print(f"[bfs] tempo: {(tempo_bfs * 1000):.5} ms")
    print(f"[dfs] custo: {len(dfs('2_3541687'))} movimentos")
    print(f"[dfs] tempo: {(tempo_dfs * 1000):.5} ms")
    print(f"[astar_hamming] custo: {len(astar_hamming('2_3541687'))} movimentos")
    print(f"[astar_hamming] tempo: {(tempo_astar_hamming * 1000):.5} ms")
    print(f"[astar_manhattan] custo: {len(astar_manhattan('2_3541687'))} movimentos")
    print(f"[astar_manhattan] tempo: {(tempo_astar_manhattan * 1000):.5} ms")
