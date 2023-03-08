UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

Trabalho 3 - Genética da Realeza & Não me Perguntes Onde Fica o Alegrete

Andrei Pochmann Koenich - Cartão 00308680 - Turma A
Jean Smaniotto Argoud - Cartão 00275602 - Turma B
Willian Nunes Reichert - Cartão 00134090 - Turma B

GENÉTICA DA REALEZA ---------------------------------------------------------------

Solução final encontrada, com número de conflitos igual a zero:
[4, 7, 5, 3, 1, 6, 8, 2]

Parâmetros do algoritmo genético utilizados:
	numero de gerações (g) = 100
	numero de individuos (n) = 75
	numero de participantes do torneio (k) = 20
	probabilidade de mutação (m) = 0.30
	número de indivíduos no elitismo (e) = 5

Chamada da função:
	run_ga(100, 75, 20, 0.30, 5)

Para executar o algoritmo e gerar o gráfico que foi incluído na entrega do
trabalho, basta trocar a chamada de run_ga(...) na linha 226 do eight_queens.py por
run_ga_with_plot(...) (os parâmetros são os mesmos).

NÃO ME PERGUNTES ONDE FICA O ALEGRETE ---------------------------------------------

Parâmetros da regressão linear utilizados:
	intercepto inicial (theta_0) = inteiro aleatório entre -50 e 50 nos testes
	inclinação inicial (theta_1) = inteiro aleatório entre -50 e 50 nos testes
	taxa de aprendizado (alpha) = 0.01
	número de iterações (num_iterations) = 3000

Os testes mostraram que taxas de aprendizado levemente maiores resultam em
overshooting, ao passo que taxas menores tornam a convergência após a redução dos
gradientes muito mais lenta. Além disso, as 3000 iterações garantem que o erro
quadrático médio final seja sempre consistente até 6 casas decimais (i.e., sempre
termina em 8.527708...) dentro do intervalo (propositalmente grande em relação aos
valores dos dados de teste) mencionado para os thetas iniciais.
