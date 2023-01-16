# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 1 - Busca em Grafos

# Andrei Pochmann Koenich - Cartao 00308680
# Jean Smaniotto Argoud   - Cartao 00275602
# Willian Nunes Reichert  - Cartao 00134090

import heapq
import unittest
import time
import solucao

SIMBOLOBRANCO = '_'             # Constante para indicar o espaco em branco no tabuleiro do 8-puzzle.
POSICAOINICIAL = '123_46758'    # Constante para representar o estado inicial.
OBJETIVO = '12345678_'          # Constante para representar o objetivo do jogo.
CUSTOINICIAL = 0                # Custo inicial do nodo referente a primeira posicao.

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

class Nodo:  # Classe para armazenar todas as informacoes de cada nodo da arvore.
    def __init__(self, estado_, pai_, acao_, custo_, heuristica_=0):
        self.estado = estado_
        self.pai = pai_
        self.acao = acao_
        self.custo = custo_
        self.heuristica = heuristica_

    def __lt__(self, other):  # Necessario para ordenar a fila de prioridades pelo custo do nodo.
        return (self.custo + self.heuristica) < (other.custo + other.heuristica)

class TestaSolucao(unittest.TestCase):

    def test_funcao_sucessor(self):
        """
        Testa a funcao sucessor para o estado "2_3541687"
        :return:

        """
        # a lista de sucessores esperados é igual ao conjunto abaixo (ordem nao importa)
        succ_esperados = {("abaixo", "2435_1687"), ("esquerda", "_23541687"), ("direita", "23_541687")}

        sucessores = solucao.sucessor("2_3541687")  # obtem os sucessores chamando a funcao implementada
        self.assertEqual(3, len(sucessores))  # verifica se foram retornados 3 sucessores
        for s in sucessores:  # verifica se os sucessores retornados estao entre os esperados
            self.assertIn(s, succ_esperados)

    def test_funcao_expande(self):
        """
        Testa a função expande para um Node com estado "185432_67" e custo 2
        :return:
        """
        estado_pai = "185432_67"
        pai = solucao.Nodo(estado_pai, None, "abaixo", 2)  # o pai do pai esta incorreto, mas nao interfere no teste
        # a resposta esperada deve conter nodos com os seguintes atributos (ordem dos nodos nao importa)
        resposta_esperada = {
            ("185_32467", estado_pai, "acima", 3),
            ("1854326_7", estado_pai, "direita", 3),
        }

        resposta = solucao.expande(pai)  # obtem a resposta chamando a funcao implementada
        self.assertEqual(2, len(resposta))  # verifica se foram retornados 2 nodos
        for nodo in resposta:
            # verifica se a tupla com os atributos do nodo esta' presente no conjunto com os nodos esperados
            self.assertIn((nodo.estado, nodo.pai.estado, nodo.acao, nodo.custo), resposta_esperada)

    def run_algorithm(self, alg, input):
        """
        Um helper que executa o algoritmo verificando timeout. Falha se der timeout
        ou retorna a resposta do algoritmo caso contrario.
        """
        response = timer.timeout(
            alg,
            args=(input,),  # must be a 1-element tuple or it doesn't work
            time_limit=60, default='timeout'
        )
        if response == 'timeout':
            self.fail(f"{alg.__name__}: timeout")

        return response

    def test_run_bfs(self):
        """
        Testa o BFS em um estado com solução e outro sem solução.
        Atencao! Passar nesse teste com '2_3541687' apenas significa que a lista retornada tem o
        numero correto de elementos. O teste nao checa se as acoes levam para a solucao!
        :return:
        """
        # no estado 2_3541687, a solucao otima tem 23 movimentos.
        self.assertEqual(23, len(self.run_algorithm(solucao.bfs, "2_3541687")))

        # nao ha solucao a partir do estado 185423_67
        self.assertIsNone(self.run_algorithm(solucao.bfs, "185423_67"))

    def test_run_astar_hamming(self):
        """
        Testa o A* com dist. Hamming em um estado com solução e outro sem solução.
        Atencao! Passar nesse teste com '2_3541687' apenas significa que a lista retornada tem o
        numero correto de elementos. O teste nao checa se as acoes levam para a solucao!
        :return:
        """
        # no estado 2_3541687, a solucao otima tem 23 movimentos.
        self.assertEqual(23, len(self.run_algorithm(solucao.astar_hamming, "2_3541687")))

        # nao ha solucao a partir do estado 185423_67
        self.assertIsNone(self.run_algorithm(solucao.astar_hamming, "185423_67"))

    def test_run_astar_manhattan(self):
        """
        Testa o A* com dist. Manhattan em um estado com solução e outro sem solução.
        Atencao! Passar nesse teste com '2_3541687' apenas significa que a lista retornada tem o
        numero correto de elementos. O teste nao checa se as acoes levam para a solucao!
        :return:
        """
        # no estado 2_3541687, a solucao otima tem 23 movimentos.
        self.assertEqual(23, len(self.run_algorithm(solucao.astar_manhattan, "2_3541687")))

        # nao ha solucao a partir do estado 185423_67
        self.assertIsNone(self.run_algorithm(solucao.astar_manhattan, "185423_67"))

    def test_run_dfs(self):
        """
        Testa o DFS apenas em um estado sem solucao pq ele nao e' obrigado
        a retornar o caminho minimo
        :param estado: str
        :return:
        """
        # nao ha solucao a partir do estado 185423_67
        self.assertIsNone(self.run_algorithm(solucao.dfs, "185423_67"))

    def test_run_action_order(self):
        """
        Testa se BFS e A* retornam a sequencia de acoes na ordem correta
        """
        estado = "1235_6478"
        solucao_otima = ['esquerda', 'abaixo', 'direita', 'direita']

        for alg in [solucao.bfs, solucao.astar_hamming, solucao.astar_manhattan]:
            self.assertEqual(solucao_otima, self.run_algorithm(alg, estado))

if __name__ == '__main__':
    unittest.main()

def valida_texto(estado):  # Verifica se o texto representando a posicao do puzzle e valido.
    if len(estado) != TOTALPOSICOES:  # Testa se o estado possui nove caracteres.
        return False

    if len(set(estado)) != len(estado):  # Testa se existem elementos repetidos.
        return False

    for i in estado:  # Testa se todos os caracteres sao numeros ou espacos em branco.
        if i == '0':
            return False
        elif not i.isdigit() and i != SIMBOLOBRANCO:
            return False

    return True

def valida_posicao(estado):  # Verifica se a posicao de entrada do puzzle possui solucao viavel.
    conta_inversoes = 0

    for i in range(len(estado)):  # Iteracoes para contar o numero de inversoes no tabuleiro (baseado em https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/).
        for j in range(i + 1, TOTALPOSICOES):
            if estado[i] != SIMBOLOBRANCO and estado[j] != SIMBOLOBRANCO and estado[i] > estado[j]:
                conta_inversoes += 1

    if conta_inversoes % 2 == 0:  # Se o numero de inversoes e par, entao o tabuleiro possui solucao valida.
        return True
    else:  # Se o numero de inversoes e impar, entao o tabuleiro nao possui solucao valida.
        return False

def movimenta_branco(estado, posicao_branco, posicao_numero):  # Movimenta a posicao em branco, no tabuleiro.
    lista_posicao = list(estado)
    lista_posicao[posicao_branco], lista_posicao[posicao_numero] = lista_posicao[posicao_numero], lista_posicao[posicao_branco]
    novo_estado = ''.join(lista_posicao)
    return novo_estado

def sucessor(estado):  # Recebe um estado e retorna uma lista de tuplas (ação, estado atingido) para cada ação que pode ser realizada no estado recebido como parâmetro.
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

    return movimentos # Retorna a string representando o tabuleiro, com a posicao do espaco branco atualizada.

def expande(nodo):  # Realiza todas as movimentacoes possiveis, a partir de um estado no tabuleiro.
    acoes = sucessor(nodo.estado)  # Obtem todas as movimentacoes possiveis no tabuleiro.
    lista_nodos = []  # Inicializa a lista contendo os nodos a serem retornados.

    for i in range(len(acoes)):
        novo_nodo = Nodo(acoes[i][1], nodo, acoes[i][0], nodo.custo + 1)
        lista_nodos.append(novo_nodo)

    return lista_nodos # Retorna os novos nodos expandidos, em uma lista.

def bfs(estado_inicial):  # Realiza a busca em largura, ate encontrar a posicao que corresponde a solucao do jogo.
    if valida_texto(estado_inicial) is False:  # Verifica se o texto (string) representando a posicao do puzzle e valido.
        return None
    if valida_posicao(estado_inicial) is False:  # Verifica se a posicao de entrada do puzzle possui solucao viavel.
        return None

    explorados = {}  # Inicializa o dicionario, contendo os nos explorados. O estado do tabuleiro sera usado como identificador.
    raiz = Nodo(estado_inicial, None, '', CUSTOINICIAL)  # Inicializa a raiz, com o estado inicial do tabuleiro.
    fronteira = [raiz]  # Inicializacao da FILA que representa a fronteira.
    movimentos = []  # Inicializacao da lista contendo os movimentos do estado inicial ate a solucao.

    while True:  # Iteracao principal para realizar a busca em largura, ate encontrar a solucao.

        if fronteira == []: # Se nao foi possivel aumentar a fronteira, falhou.
            return None

        v = fronteira.pop(0)  # Remove o PRIMEIRO elemento adicionado na FILA (FIFO - first in, first out).

        if v.estado == OBJETIVO:  # Casos em que foi encontrada a solucao.
            while v.pai is not None:  # Iteracao para resgatar o caminho de acoes do estado inicial ate a solucao.
                movimentos.append(v.acao)
                v = v.pai
            movimentos.reverse()
            return movimentos

        if v.estado not in explorados: # Se o estado ainda nao foi explorado, entao ele e incluido no conjunto de explorados e a fronteira e expandida.
            explorados[v.estado] = v
            fronteira += expande(v)  # Adiciona todos os vizinhos de v na fronteira.

def dfs(estado_inicial):  # Realiza a busca em profundidade, ate encontrar a posicao que corresponde a solucao do jogo.
    if valida_texto(estado_inicial) is False:  # Verifica se o texto (string) representando a posicao do puzzle e valido.
        return None
    if valida_posicao(estado_inicial) is False:  # Verifica se a posicao de entrada do puzzle possui solucao viavel.
        return None

    explorados = {}  # Inicializa o dicionario, contendo os nos explorados. O estado do tabuleiro sera usado como identificador.
    raiz = Nodo(estado_inicial, None, '', CUSTOINICIAL)  # Inicializa a raiz, com o estado inicial do tabuleiro.
    fronteira = [raiz]  # Inicializacao da PILHA que representa a fronteira.
    caminho = []  # Inicializacao da lista contendo os movimentos do estado inicial ate a solucao.

    while True:  # Iteracao principal para realizar a busca em profundidade, ate encontrar a solucao.

        if fronteira == []: # Se nao foi possivel aumentar a fronteira, falhou.
            return None

        v = fronteira.pop()  # Remove o ULTIMO elemento adicionado na PILHA (LIFO - last in, first out).

        if v.estado == OBJETIVO:  # Casos em que foi encontrada a solucao.
            while v.pai is not None:  # Iteracao para resgatar o caminho de acoes do estado inicial ate a solucao.
                caminho.append(v.acao)
                v = v.pai
            caminho.reverse()
            return caminho

        if v.estado not in explorados: # Se o estado ainda nao foi explorado, entao ele e incluido no conjunto de explorados e a fronteira e expandida.
            explorados[v.estado] = v
            fronteira += expande(v)  # Adiciona todos os vizinhos de v na fronteira.

def heuristica_hamming(estado): # Obtem o valor referente a heuristica de Hamming (numero total de pecas fora do lugar).
    return sum([estado[i] != OBJETIVO[i] for i in range(len(estado))]) # Retorna o valor referente a heuristica de Hamming (numero total de pecas fora do lugar).

def astar_hamming(estado_inicial):  # Realiza a busca com A* (com a heuristica da distancia de Hamming) ate encontrar a posicao que corresponde a solucao do jogo.
    if valida_texto(estado_inicial) is False:  # Verifica se o texto (string) representando a posicao do puzzle e valido.
        return None
    if valida_posicao(estado_inicial) is False:  # Verifica se a posicao de entrada do puzzle possui solucao viavel.
        return None

    explorados = {}  # Inicializa o dicionario contendo os nos explorados. O estado do tabuleiro sera usado como identificador.
    raiz = Nodo(estado_inicial, None, '', CUSTOINICIAL, heuristica_hamming(estado_inicial))  # Inicializa a raiz com o estado inicial do tabuleiro.
    fronteira = [raiz]  # Inicializacao da FILA DE PRIORIDADE que representa a fronteira.
    movimentos = []  # Inicializacao da lista contendo os movimentos do estado inicial ate a solucao.

    while True:  # Iteracao principal para realizar a busca com A* (com a heuristica da distancia de Hamming) ate encontrar a solucao.

        if fronteira == []: # Se nao foi possivel aumentar a fronteira, falhou.
            return None

        v = heapq.heappop(fronteira)  # Remove o elemento que possui o MENOR CUSTO TOTAL (custo + hamming(estado)) adicionado na FILA DE PRIORIDADES.

        if v.estado == OBJETIVO:  # Casos em que foi encontrada a solucao.
            while v.pai is not None:  # Iteracao para resgatar o caminho de acoes do estado inicial ate a solucao.
                movimentos.append(v.acao)
                v = v.pai
            movimentos.reverse()
            return movimentos # Retorna a lista de movimentos, para concluir o jogo.

        if v.estado not in explorados: # Atualiza a arvore heap, com os novos nodos.
            explorados[v.estado] = v
            for nodo in expande(v):  # Adiciona todos os vizinhos de v na fronteira.
                nodo.heuristica = heuristica_hamming(nodo.estado)
                heapq.heappush(fronteira, nodo)

def heuristica_manhattan(estado): # Obtem o valor referente a heuristica da distancia Manhattan.
    tabuleiro_lista = []
    tabuleiro_lista[:0] = estado # Converte a string representando o tabuleiro em uma lista.
    tabuleiro_lista[tabuleiro_lista.index(SIMBOLOBRANCO)] = '0' # Altera o caractere da posicao em branco para zero.

    for i in range(len(tabuleiro_lista)): # Converte cada caractere representando as pecas em valores inteiros.
        tabuleiro_lista[i] = int(tabuleiro_lista[i])

    distancia_manhattan = 0
    # Percorre o tabuleiro, calculando as distancias de cada peca e somando.
    distancia_manhattan = sum(abs((valor - 1) % 3 - i % 3) + abs((valor - 1) // 3 - i // 3) for i, valor in enumerate(tabuleiro_lista) if valor)
    return distancia_manhattan # Retorna o valor referente a heuristica da distancia Manhattan.

def astar_manhattan(estado_inicial):  # Realiza a busca com A* (com a heuristica da distancia Manhattan) ate encontrar a posicao que corresponde a solucao do jogo.
    if valida_texto(estado_inicial) is False:  # Verifica se o texto (string) representando a posicao do puzzle e valido.
        return None
    if valida_posicao(estado_inicial) is False:  # Verifica se a posicao de entrada do puzzle possui solucao viavel.
        return None

    explorados = {}  # Inicializa o dicionario contendo os nos explorados. O estado do tabuleiro sera usado como identificador.
    raiz = Nodo(estado_inicial, None, '', CUSTOINICIAL,heuristica_manhattan(estado_inicial))  # Inicializa a raiz com o estado inicial do tabuleiro.
    fronteira = [raiz]  # Inicializacao da FILA DE PRIORIDADE que representa a fronteira.
    movimentos = []  # Inicializacao da lista contendo os movimentos do estado inicial ate a solucao.

    while True:  # Iteracao principal para realizar a busca com A* (com a heuristica da distancia Manhattan) ate encontrar a solucao.

        if fronteira == []: # Se nao foi possivel aumentar a fronteira, falhou.
            return None

        v = heapq.heappop(fronteira)  # Remove o elemento que possui o MENOR CUSTO TOTAL (custo + hamming(estado)) adicionado na FILA DE PRIORIDADES.

        if v.estado == OBJETIVO:  # Casos em que foi encontrada a solucao.
            while v.pai is not None:  # Iteracao para resgatar o caminho de acoes do estado inicial ate a solucao.
                movimentos.append(v.acao)
                v = v.pai
            movimentos.reverse()
            return movimentos # Retorna a lista de movimentos, para concluir o jogo.

        if v.estado not in explorados: # Atualiza a arvore heap, com os novos nodos.
            explorados[v.estado] = v
            for nodo in expande(v):  # Adiciona todos os vizinhos de v na fronteira.
                nodo.heuristica = heuristica_manhattan(nodo.estado)
                heapq.heappush(fronteira, nodo)


def main():
    test_funcao_sucessor('2_3541687')


main()
