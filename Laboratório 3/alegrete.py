# UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

# Trabalho 3 - Parte 2 - Não me perguntes onde fica o Alegrete...

# Andrei Pochmann Koenich - Cartão 00308680
# Jean Smaniotto Argoud   - Cartão 00275602
# Willian Nunes Reichert  - Cartão 00134090

import time
from random import randint

import matplotlib.pyplot as plt
import numpy as np


def compute_mse(theta_0, theta_1, data):
    """
    Calcula o erro quadratico medio
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    # Extrai as features (área do terreno) e as respostas (preço) do conjunto de dados
    x = data[:, 0]
    y = data[:, 1]

    # Calcula as previsões da regressão linear para cada exemplo do conjunto de dados
    y_pred = theta_0 + theta_1 * x

    # Calcula o erro quadrático médio (MSE) das previsões
    mse = np.mean((y_pred - y) ** 2)

    return mse


def step_gradient(theta_0, theta_1, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de theta_0 e theta_1.
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de theta_0 e theta_1, respectivamente
    """
    # Extrai as features (área do terreno) e as respostas (preço) do conjunto de dados
    x = data[:, 0]
    y = data[:, 1]

    # Calcula as previsões da regressão linear para cada exemplo do conjunto de dados
    y_pred = theta_0 + theta_1 * x

    # Calcula o vetor de erros da regressão
    errors = y_pred - y

    # Calcula o gradiente para theta_0 e theta_1
    gradient_0 = 2 * np.mean(errors)
    gradient_1 = 2 * np.mean(errors * x)

    # Atualiza os valores de theta_0 e theta_1 usando a taxa de aprendizado e o gradiente
    new_theta_0 = theta_0 - alpha * gradient_0
    new_theta_1 = theta_1 - alpha * gradient_1

    return new_theta_0, new_theta_1


def fit(data, theta_0, theta_1, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de theta_0 e theta_1.
    Ao final, retorna duas listas, uma com os theta_0 e outra com os theta_1
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os theta_0 e outra com os theta_1 obtidos ao longo da execução
    """
    # Cria as listas para armazenar os valores atualizados de theta_0 e theta_1 a cada época/iteração
    theta_0_history = [theta_0]
    theta_1_history = [theta_1]

    # Executa o loop de atualização por descida do gradiente por num_iterations épocas/iterações
    for i in range(num_iterations):
        # Executa uma atualização por descida do gradiente
        theta_0, theta_1 = step_gradient(theta_0, theta_1, data, alpha)

        # Armazena os valores atualizados de theta_0 e theta_1 nas listas de histórico
        theta_0_history.append(theta_0)
        theta_1_history.append(theta_1)

    # Retorna as listas com os valores atualizados de theta_0 e theta_1 ao longo das épocas/iterações
    return theta_0_history, theta_1_history


def alegrete(theta_0, theta_1, alpha, num_iterations, plot=False):
    data = np.genfromtxt('alegrete.csv', delimiter=',')

    # Executar o algoritmo de gradiente descendente
    theta_0_history, theta_1_history = fit(data, theta_0, theta_1, alpha, num_iterations)

    # Calcula o erro quadrádico médio após o treino
    mse_final = compute_mse(theta_0_history[-1], theta_1_history[-1], data)

    if plot:
        # Plotar os dados
        plt.scatter(data[:, 0], data[:, 1], color='blue')

        # Plotar a linha de regressão
        x = np.linspace(np.min(data[:, 0]), np.max(data[:, 0]), 100)
        y = theta_0_history[-1] + theta_1_history[-1] * x
        plt.plot(x, y, color='red')

        plt.xlabel('Área do terreno (hectares)')
        plt.ylabel('Preço (milhares de reais)')
        plt.show()

    return mse_final


if __name__ == "__main__":
    start_time = time.time()
    mse_hist = [alegrete(randint(-50, 50), randint(-50, 50), 0.01, 3000) for i in range(250)]

    print(f'MSE mínimo: {min(mse_hist):.8}')
    print(f'MSE máximo: {max(mse_hist):.8}')
    print(f'MSE médio: {(sum(mse_hist) / len(mse_hist)):.8}')
    print(f'\n--- TEMPO DE EXECUÇÃO: {(time.time() - start_time):.6} segundos ---\n')
