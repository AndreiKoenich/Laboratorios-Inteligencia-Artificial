# Porto Alegre, dezembro de 2022

# Inteligencia Artificial
# Trabalho 1 - Busca em Grafos

# Andrei Pochmann Koenich - Cartao 00308680
# Jean - Cartao
# William - Cartao

import os

SIMBOLOBRANCO = '_' # Constante para indicar o espaco em branco no tabuleiro do 8-puzzle.
POSICAOPUZZLE = '2_3541687'
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

class Nodo: # Classe para armazenar todas as informacoes de cada nodo da arvore.
    def __init__(self, estado_,pai_,acao_,custo_):
        self.estado = estado_
        self.pai = pai_
        self.acao = acao_
        self.custo = custo_

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
    nodo_pai = Nodo(POSICAOPUZZLE,None,'',CUSTOINICIAL) # Teste, remover depois
    sucessores = expande(nodo_pai) # Teste, remover depois

def main():
    inicia_programa()
    #os.system("PAUSE")

main()