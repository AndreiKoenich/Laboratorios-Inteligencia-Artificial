import unittest
import timer
import solucao


class TestesUnitarios(unittest.TestCase):

    def test_funcao_sucessor(self):
        """
        Testa a funcao sucessor para o estado "2_3541687"
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

    def test_hamming_dist(self):
        """
        Testa o cálculo da distância de Hamming.
        """
        self.assertEqual(7, solucao.heuristica_hamming("2_3541687"))

    def test_manhattan_dist(self):
        """
        Testa o cálculo da distância de Manhattan.
        """
        self.assertEqual(11, solucao.heuristica_manhattan("2_3541687"))

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
        """
        # no estado 2_3541687, a solucao otima tem 23 movimentos.
        self.assertEqual(23, len(self.run_algorithm(solucao.bfs, "2_3541687")))

        # nao ha solucao a partir do estado 185423_67
        self.assertIsNone(self.run_algorithm(solucao.bfs, "185423_67"))

    def test_solution_bfs(self):
        """
        Testa se os movimentos retornados pela busca BFS levam ao objetivo.
        """
        estado = "2_3541687"
        movimentos: list = self.run_algorithm(solucao.bfs, estado)
        for i in range(len(movimentos)):
            movimento = movimentos.pop(0)
            for succ in solucao.sucessor(estado):
                if succ[0] == movimento:
                    estado = succ[1]
        self.assertEqual("12345678_", estado)
        self.assertEqual([], movimentos)

    def test_run_astar_hamming(self):
        """
        Testa o A* com dist. Hamming em um estado com solução e outro sem solução.
        Atencao! Passar nesse teste com '2_3541687' apenas significa que a lista retornada tem o
        numero correto de elementos. O teste nao checa se as acoes levam para a solucao!
        """
        # no estado 2_3541687, a solucao otima tem 23 movimentos.
        self.assertEqual(23, len(self.run_algorithm(solucao.astar_hamming, "2_3541687")))

        # nao ha solucao a partir do estado 185423_67
        self.assertIsNone(self.run_algorithm(solucao.astar_hamming, "185423_67"))

    def test_solution_astar_hamming(self):
        """
        Testa se os movimentos retornados pela busca A* hamming levam ao objetivo.
        """
        estado = "2_3541687"
        movimentos: list = self.run_algorithm(solucao.astar_hamming, estado)
        for i in range(len(movimentos)):
            movimento = movimentos.pop(0)
            for succ in solucao.sucessor(estado):
                if succ[0] == movimento:
                    estado = succ[1]
        self.assertEqual("12345678_", estado)
        self.assertEqual([], movimentos)

    def test_run_astar_manhattan(self):
        """
        Testa o A* com dist. Manhattan em um estado com solução e outro sem solução.
        Atencao! Passar nesse teste com '2_3541687' apenas significa que a lista retornada tem o
        numero correto de elementos. O teste nao checa se as acoes levam para a solucao!
        """
        # no estado 2_3541687, a solucao otima tem 23 movimentos.
        self.assertEqual(23, len(self.run_algorithm(solucao.astar_manhattan, "2_3541687")))

        # nao ha solucao a partir do estado 185423_67
        self.assertIsNone(self.run_algorithm(solucao.astar_manhattan, "185423_67"))

    def test_solution_astar_manhattan(self):
        """
        Testa se os movimentos retornados pela busca A* manhattan levam ao objetivo.
        """
        estado = "2_3541687"
        movimentos: list = self.run_algorithm(solucao.astar_manhattan, estado)
        for i in range(len(movimentos)):
            movimento = movimentos.pop(0)
            for succ in solucao.sucessor(estado):
                if succ[0] == movimento:
                    estado = succ[1]
        self.assertEqual("12345678_", estado)
        self.assertEqual([], movimentos)

    def test_run_dfs(self):
        """
        Testa o DFS apenas em um estado sem solucao pq ele nao e' obrigado
        a retornar o caminho minimo
        """
        # nao ha solucao a partir do estado 185423_67
        self.assertIsNone(self.run_algorithm(solucao.dfs, "185423_67"))

    def test_solution_dfs(self):
        """
        Testa se os movimentos retornados pela busca DFS levam ao objetivo.
        """
        estado = "2_3541687"
        movimentos: list = self.run_algorithm(solucao.dfs, estado)
        for i in range(len(movimentos)):
            movimento = movimentos.pop(0)
            for succ in solucao.sucessor(estado):
                if succ[0] == movimento:
                    estado = succ[1]
        self.assertEqual("12345678_", estado)
        self.assertEqual([], movimentos)

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
