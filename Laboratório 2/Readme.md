 UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL - Semestre 2022/02

 Trabalho 2 - Monte Carlo Tree Search em Othello/Reversi

 Andrei Pochmann Koenich - Cartão 00308680
 Jean Smaniotto Argoud   - Cartão 00275602
 Willian Nunes Reichert  - Cartão 00134090

# Bibliotecas

Utilizamos apenas as bibliotecas comuns da linguagem Python, 
além das importações específicas do laboratório, descritas abaixo:

import copy
import math
import random
import time
from collections import OrderedDict
from typing import Tuple
from ..othello.gamestate import GameState

# Descrição

Foi utilizado o algoritmo Monte Carlo Tree Search da forma descrita em aula, utilizando
o critério UCB na etapa de seleção. O valor utilizado para a constante UCB corresponde
à raiz quadrada de dois.

# Dificuldades

Não houve grandes dificuldades.

# Referências

- https://youtu.be/Fbs4lnGLS8M
- https://www.youtube.com/watch?v=sjRFGR-KQpc
- https://www.youtube.com/watch?v=UYHcKYXQFTo
- https://www.youtube.com/watch?v=SAtsEWxzumM
- https://jyopari.github.io/MCTS.html
- https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
