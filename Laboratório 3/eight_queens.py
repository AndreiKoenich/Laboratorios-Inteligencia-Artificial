# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 3 - Parte 1 - Genética da Realeza

# Andrei Pochmann Koenich - Cartão 00308680
# Jean Smaniotto Argoud   - Cartão 00275602
# Willian Nunes Reichert  - Cartão 00134090

import copy
import random

import matplotlib.pyplot as plt
import numpy as np

TAMANHOTABULEIRO = 8  # Tamanho do tabuleiro de xadrez 8x8.


def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 10.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    ataques = 0
    for i in range(TAMANHOTABULEIRO - 1):
        for j in range(i + 1, TAMANHOTABULEIRO):  # Teste na direção HORIZONTAL, para a DIREITA.
            if individual[i] == individual[j]:
                ataques += 1

        k = 1
        for j in range(i + 1, TAMANHOTABULEIRO):  # Teste na direção INFERIOR DIREITA.
            if individual[j] == individual[i] + k:
                ataques += 1
            k += 1

        k = 1
        for j in range(i + 1, TAMANHOTABULEIRO):  # Teste na direção SUPERIOR DIREITA.
            if individual[j] == individual[i] - k:
                ataques += 1
            k += 1

    return ataques


def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    melhor = participants[0]
    menor_conflitos = evaluate(participants[0])
    # Percorre toda a lista de participantes, testando o número de conflitos de cada um.
    for i in range(1, len(participants)):
        conflitos = evaluate(participants[i])
        if conflitos < menor_conflitos:  # Verifica se o participante atual tem menos conflitos, e salva a informação.
            menor_conflitos = conflitos
            melhor = participants[i]
    return melhor  # Retorna o melhor participante, que possui menos conflitos.


def selecao(participantes, k):  # Retorna os k indivíduos mais aptos da população.
    if k > len(participantes):
        return []

    participantes_aux = random.sample(participantes, k)

    mais_aptos = []
    for i in range(0, 2):  # Realiza o torneio duas vezes, para obter os dois indivíduos mais aptos.
        vencedor = tournament(participantes_aux)
        participantes_aux.remove(vencedor)
        mais_aptos.append(vencedor)

    return mais_aptos


def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    # Lista que irá conter os dois novos indivíduos, após a troca de material genético.
    lista_individuos = [copy.copy(parent1), copy.copy(parent2)]
    for i in range(index, TAMANHOTABULEIRO):
        lista_individuos[0][i] = parent2[i]
        lista_individuos[1][i] = parent1[i]
    return lista_individuos


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    posicao_aleatoria = random.randint(0, TAMANHOTABULEIRO - 1)
    numero_aleatorio = random.randint(1, TAMANHOTABULEIRO)
    if random.random() < m:
        individual[posicao_aleatoria] = numero_aleatorio
    return individual


def gera_aleatorio():  # Geração de população aleatória para o jogo das oito damas.
    lista = []
    for i in range(TAMANHOTABULEIRO):
        lista.append(random.randint(1, TAMANHOTABULEIRO))
    return lista


def tournament_pior(participants):
    melhor = participants[0]
    menor_conflitos = evaluate(participants[0])
    for i in range(1, len(participants)):
        conflitos = evaluate(participants[i])
        if conflitos > menor_conflitos:
            menor_conflitos = conflitos
            melhor = participants[i]
    return melhor


def media_conflitos(participants):
    media = 0
    for i in participants:
        media += evaluate(i)
    media /= len(participants)
    return media


def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:int - número de indivíduos no elitismo
    :return:list - melhor individuo encontrado
    """
    populacao = [gera_aleatorio() for _ in range(0, n)]

    for i in range(0, g):
        populacao = sorted(populacao, key=evaluate)
        populacao_nova = populacao[:e]  # Conserva os e indivíduos mais aptos da população (ELITISMO).
        while len(populacao_nova) < n:
            mais_aptos = selecao(populacao, k)  # Realiza o torneio (SELEÇÃO) entre k indivíduos aleatórios.
            ponto_cruzamento = random.randint(0, 7)
            # Realiza o CROSSOVER entre os dois indivíduos mais aptos.
            descendentes = crossover(mais_aptos[0], mais_aptos[1], ponto_cruzamento)
            descendentes[0] = mutate(descendentes[0], m)  # Realiza a MUTAÇÃO no primeiro descendente do crossover.
            descendentes[1] = mutate(descendentes[1], m)  # Realiza a MUTAÇÃO no segundo descendente do crossover.
            populacao_nova.append(descendentes[0])  # Salva o primeiro descendente do crossover.
            populacao_nova.append(descendentes[1])  # Salva o segundo descendente do crossover.
        populacao = populacao_nova  # Atualiza a população.

    melhor_individuo = tournament(populacao)  # Obtém o melhor indivíduo, após o fim das gerações.
    return melhor_individuo  # Retorna o melhor indivíduo.


def run_ga_with_plot(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas.
    Além disso, cria um gráfico com o histórico de conflitos ao longo das gerações
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:int - número de indivíduos no elitismo
    :return:list - melhor individuo encontrado
    """
    min_conflitos = []
    max_conflitos = []
    med_conflitos = []
    populacao = [gera_aleatorio() for _ in range(0, n)]

    for i in range(0, g):
        max_conflitos.append(evaluate(tournament_pior(populacao)))
        min_conflitos.append(evaluate(tournament(populacao)))
        med_conflitos.append(media_conflitos(populacao))

        populacao = sorted(populacao, key=evaluate)
        populacao_nova = populacao[:e]  # Conserva os e indivíduos mais aptos da população (ELITISMO).
        while len(populacao_nova) < n:
            mais_aptos = selecao(populacao, k)  # Realiza o torneio (SELEÇÃO) entre k indivíduos aleatórios.
            ponto_cruzamento = random.randint(0, 7)
            # Realiza o CROSSOVER entre os dois indivíduos mais aptos.
            descendentes = crossover(mais_aptos[0], mais_aptos[1], ponto_cruzamento)
            descendentes[0] = mutate(descendentes[0], m)  # Realiza a MUTAÇÃO no primeiro descendente do crossover.
            descendentes[1] = mutate(descendentes[1], m)  # Realiza a MUTAÇÃO no segundo descendente do crossover.
            populacao_nova.append(descendentes[0])  # Salva o primeiro descendente do crossover.
            populacao_nova.append(descendentes[1])  # Salva o segundo descendente do crossover.
        populacao = populacao_nova  # Atualiza a população.

    plt.plot(max_conflitos, color='tomato')
    plt.plot(med_conflitos, color='limegreen')
    plt.plot(min_conflitos, color='dodgerblue')
    plt.title('Conflitos em Cada Geração', fontweight="bold")
    plt.xlabel('Geração')
    plt.ylabel('Conflitos')
    plt.xticks(np.arange(0, len(max_conflitos) + 1, 10))
    plt.yticks(np.arange(min(min_conflitos), max(max_conflitos) + 1, 1))
    plt.grid(color='0.90')
    plt.legend(["Maior conflito", "Média dos conflitos", "Menor conflito"], loc="upper right")
    plt.show()

    melhor_individuo = tournament(populacao)  # Obtém o melhor indivíduo, após o fim das gerações.
    return melhor_individuo  # Retorna o melhor indivíduo.


if __name__ == '__main__':
    vencedor = run_ga(100, 75, 20, 0.3, 5)
    print("VENCEDOR:", vencedor)
    print("NUMERO DE ATAQUES:", evaluate(vencedor))
