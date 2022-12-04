# Porto Alegre, dezembro de 2022

# Inteligencia Artificial
# Trabalho 1 - Busca em Grafos

# Andrei Pochmann Koenich - Cartao 00308680
# Jean - Cartao
# William - Cartao

import os

SIMBOLOBRANCO = '_' # Constante para indicar o espaco em branco no tabuleiro do 8-puzzle.
POSICAOINICIAL = '812_43765'
SOLUCAOFINAL = '12345678_'
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

def valida_texto(estado): # Verifica se o texto representando a posicao do puzzle e valido.
    if len(estado) != TOTALPOSICOES: # Testa se o estado possui nove caracteres.
        return False

    if (len(set(estado)) != len(estado)): # Testa se existem elementos repetidos.
        return False

    for i in estado: # Testa se todos os caracteres sao numeros ou espacos em branco.
        if not i.isdigit() and i != SIMBOLOBRANCO:
            return False

    return True

def permuta_branco(estado, posicao_branco, posicao_numero):
    lista_posicao = list(estado)
    lista_posicao[posicao_branco], lista_posicao[posicao_numero] = lista_posicao[posicao_numero], lista_posicao[posicao_branco]
    novo_estado = ''.join(lista_posicao)
    return novo_estado

def expande(nodo):
    acoes = sucessor(nodo.estado) # Obtem todas as movimentacoes possiveis no tabuleiro.
    lista_nodos = [] # Inicializa a lista contendo os nodos a serem retornados.
    novo_nodo = Nodo('', None, '', 0)

    for i in range(len(acoes)):
        novo_nodo = Nodo(acoes[i][1],nodo,acoes[i][0],nodo.custo+1)
        lista_nodos.append(novo_nodo)

    return lista_nodos

def sucessor(estado):
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

def inicia_programa():
    if valida_texto(POSICAOINICIAL) == False:
        print('TEXTO DA POSICAO INICIAL INVALIDO!')
        return

    if valida_posicao(POSICAOINICIAL) == False:
        print('POSICAO INICIAL SEM SOLUCAO!')
        return

    nodo_pai = Nodo(POSICAOINICIAL,None,'',CUSTOINICIAL) # Teste, remover depois
    sucessores = expande(nodo_pai) # Teste, remover depois

def main():
    inicia_programa()
    os.system("PAUSE")

main()
