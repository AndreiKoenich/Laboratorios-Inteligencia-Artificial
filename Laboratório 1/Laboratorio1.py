# Porto Alegre, dezembro de 2022

# Inteligencia Artificial
# Trabalho 1 - Busca em Grafos

# Andrei Pochmann Koenich - Cartao 00308680
# Jean - Cartao
# William - Cartao

import os

SIMBOLOBRANCO = '_' # Constante para indicar o espaco em branco no tabuleiro do 8-puzzle.
POSICAOINICIAL = '123_46758' # Apenas para teste, remover depois
OBJETIVO = '12345678_'
CUSTOINICIAL = 0

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

class Nodo: # Classe para armazenar todas as informacoes de cada nodo da arvore.
    def __init__(self, estado_,pai_,acao_,custo_):
        self.estado = estado_
        self.pai = pai_
        self.acao = acao_
        self.custo = custo_
        
def valida_texto(estado): # Verifica se o texto representando a posicao do puzzle e valido.
    if len(estado) != TOTALPOSICOES: # Testa se o estado possui nove caracteres.
        return False

    if (len(set(estado)) != len(estado)): # Testa se existem elementos repetidos.
        return False

    for i in estado: # Testa se todos os caracteres sao numeros ou espacos em branco.
        if not i.isdigit() and i != SIMBOLOBRANCO:
            return False

    return True

def valida_posicao(estado): # Verifica se a posicao de entrada do puzzle possui solucao viavel.
    conta_inversoes = 0

    for i in range(len(estado)): # Iteracoes para contar o numero de inversoes no tabuleiro (baseado em https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/).
        for j in range(i+1,TOTALPOSICOES):
            if estado[i] != SIMBOLOBRANCO and estado[j] != SIMBOLOBRANCO and estado[i] > estado[j]:
                conta_inversoes += 1

    if (conta_inversoes % 2 == 0): # Se o numero de inversoes e par, entao o tabuleiro possui solucao valida.
        return True

    else: # Se o numero de inversoes e impar, entao o tabuleiro nao possui solucao valida.
        return False  
    
 def permuta_branco(estado, posicao_branco, posicao_numero): # Movimenta a posicao em branco, no tabuleiro.
    lista_posicao = list(estado)
    lista_posicao[posicao_branco], lista_posicao[posicao_numero] = lista_posicao[posicao_numero], lista_posicao[posicao_branco]
    novo_estado = ''.join(lista_posicao)
    return novo_estado

def sucessor(estado): # Recebe um estado e retorna uma lista de tuplas (ação, estado atingido) para cada ação que pode ser realizada no estado recebido como parâmetro.
    movimentos = [] # Inicializa a lista contendo as tuplas que indicam os movimentos.
    posicao_branco = estado.rfind(SIMBOLOBRANCO) # Encontra a posicao do espaco vazio no tabuleiro.

    # Comandos de selecao para verificar como movimentar o espaco em branco.
    if posicao_branco == PRIMEIRAPOSICAO:
        movimentos.append((TEXTODIREITA,permuta_branco(estado,PRIMEIRAPOSICAO,SEGUNDAPOSICAO)))
        movimentos.append((TEXTOBAIXO,permuta_branco(estado,PRIMEIRAPOSICAO,QUARTAPOSICAO)))

    elif posicao_branco == SEGUNDAPOSICAO:
        movimentos.append((TEXTOESQUERDA,permuta_branco(estado,SEGUNDAPOSICAO,PRIMEIRAPOSICAO)))
        movimentos.append((TEXTOBAIXO,permuta_branco(estado,SEGUNDAPOSICAO,QUINTAPOSICAO)))
        movimentos.append((TEXTODIREITA,permuta_branco(estado,SEGUNDAPOSICAO,TERCEIRAPOSICAO)))

    elif posicao_branco == TERCEIRAPOSICAO:
        movimentos.append((TEXTOESQUERDA,permuta_branco(estado,TERCEIRAPOSICAO,SEGUNDAPOSICAO)))
        movimentos.append((TEXTOBAIXO,permuta_branco(estado,TERCEIRAPOSICAO,SEXTAPOSICAO)))

    elif posicao_branco == QUARTAPOSICAO:
        movimentos.append((TEXTOCIMA,permuta_branco(estado,QUARTAPOSICAO,PRIMEIRAPOSICAO)))
        movimentos.append((TEXTODIREITA,permuta_branco(estado,QUARTAPOSICAO,QUINTAPOSICAO)))
        movimentos.append((TEXTOBAIXO,permuta_branco(estado,QUARTAPOSICAO,SETIMAPOSICAO)))

    elif posicao_branco == QUINTAPOSICAO:
        movimentos.append((TEXTOCIMA,permuta_branco(estado,QUINTAPOSICAO,SEGUNDAPOSICAO)))
        movimentos.append((TEXTOESQUERDA,permuta_branco(estado,QUINTAPOSICAO,QUARTAPOSICAO)))
        movimentos.append((TEXTODIREITA,permuta_branco(estado,QUINTAPOSICAO,SEXTAPOSICAO)))
        movimentos.append((TEXTOBAIXO,permuta_branco(estado,QUINTAPOSICAO,OITAVAPOSICAO)))

    elif posicao_branco == SEXTAPOSICAO:
        movimentos.append((TEXTOCIMA,permuta_branco(estado,SEXTAPOSICAO,TERCEIRAPOSICAO)))
        movimentos.append((TEXTOESQUERDA,permuta_branco(estado,SEXTAPOSICAO,QUINTAPOSICAO)))
        movimentos.append((TEXTOBAIXO,permuta_branco(estado,SEXTAPOSICAO,NONAPOSICAO)))

    elif posicao_branco == SETIMAPOSICAO:
        movimentos.append((TEXTOCIMA,permuta_branco(estado,SETIMAPOSICAO,QUARTAPOSICAO)))
        movimentos.append((TEXTODIREITA,permuta_branco(estado,SETIMAPOSICAO,OITAVAPOSICAO)))

    elif posicao_branco == OITAVAPOSICAO:
        movimentos.append((TEXTOESQUERDA, permuta_branco(estado,OITAVAPOSICAO,SETIMAPOSICAO)))
        movimentos.append((TEXTOCIMA,permuta_branco(estado,OITAVAPOSICAO,QUINTAPOSICAO)))
        movimentos.append((TEXTODIREITA, permuta_branco(estado, OITAVAPOSICAO,NONAPOSICAO)))

    elif posicao_branco == NONAPOSICAO:
        movimentos.append((TEXTOCIMA, permuta_branco(estado, NONAPOSICAO, SEXTAPOSICAO)))
        movimentos.append((TEXTOESQUERDA, permuta_branco(estado, NONAPOSICAO, OITAVAPOSICAO)))

    return movimentos   
    
 def expande(nodo): # Realiza todas as movimentacoes possiveis, a partir de um estado no tabuleiro.
    acoes = sucessor(nodo.estado) # Obtem todas as movimentacoes possiveis no tabuleiro.
    lista_nodos = [] # Inicializa a lista contendo os nodos a serem retornados.
    novo_nodo = Nodo('', None, '', 0)

    for i in range(len(acoes)):
        novo_nodo = Nodo(acoes[i][1],nodo,acoes[i][0],nodo.custo+1)
        lista_nodos.append(novo_nodo)

    return lista_nodos  

def bfs(estado_inicial): # Realiza a busca em largura, ate encontrar a posicao que corresponde a solucao do jogo.
    if valida_texto(estado_inicial) == False:
        return None

    elif valida_posicao(estado_inicial) == False:
        return None

    explorados = {} # Inicializa o dicionario, contendo os nos explorados. O estado do tabuleiro sera usado como identificador.
    raiz = Nodo(estado_inicial,None,'',CUSTOINICIAL) # Inicializa a raiz, com o estado inicial do tabuleiro.
    fronteira = [raiz] # Inicializacao da FILA que representa a fronteira.
    movimentos = [] # Inicializacao da lista contendo os movimentos do estado inicial ate a solucao.

    while True: # Iteracao principal para realizar a busca em largura, ate encontrar a solucao.

        if fronteira == []:
            return None

        v = fronteira.pop(0) # Remove o PRIMEIRO elemento adicionado na FILA (FIFO - first in, first out).

        if v.estado == OBJETIVO: # Casos em que foi encontrada a solucao.
            while v.pai != None: # Iteracao para resgatar o caminho de acoes do estado inicial ate a solucao.
                movimentos.append(v.acao)
                v = v.pai
            movimentos.reverse()
            return movimentos

        if v.estado not in explorados:
            explorados[v.estado] = v
            fronteira += expande(v) # Adiciona todos os vizinhos de v na fronteira.

def dfs(estado_inicial): # Realiza a busca em largura, ate encontrar a posicao que corresponde a solucao do jogo.
    if valida_texto(estado_inicial) == False:
        return None

    elif valida_posicao(estado_inicial) == False:
        return None

    explorados = {} # Inicializa o dicionario, contendo os nos explorados. O estado do tabuleiro sera usado como identificador.
    raiz = Nodo(estado_inicial,None,'',CUSTOINICIAL) # Inicializa a raiz, com o estado inicial do tabuleiro.
    fronteira = [raiz] # Inicializacao da PILHA que representa a fronteira.
    caminho = [] # Inicializacao da lista contendo os movimentos do estado inicial ate a solucao.

    while True: # Iteracao principal para realizar a busca em profundidade, ate encontrar a solucao.
        if fronteira == []:
            return None

        v = fronteira.pop() # Remove o ULTIMO elemento adicionado na PILHA (LIFO - last in, first out).

        if v.estado == OBJETIVO: # Casos em que foi encontrada a solucao.
            while v.pai != None: # Iteracao para resgatar o caminho de acoes do estado inicial ate a solucao.
                caminho.append(v.acao)
                v = v.pai
            caminho.reverse()
            return caminho

        if v.estado not in explorados:
            explorados[v.estado] = v
            fronteira += expande(v) # Adiciona todos os vizinhos de v na fronteira.

def inicia_programa():

    #print(sucessor(POSICAOINICIAL))
    print(bfs(POSICAOINICIAL))
    #print(dfs(POSICAOINICIAL))
    #print(astar_hamming(POSICAOINICIAL))
    #print(astar_manhattan(POSICAOINICIAL))


def main():
    inicia_programa()
    os.system("PAUSE")

main()
