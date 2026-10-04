"""
@brief      Esse arquivo contém a implementação da busca em largura
            e demais métodos necessários.

@details    pseudocódigo:

            BFS(G, s)

            para cada vértice u ∈ G.V faça
                cor[u] ← BRANCO
                distancia[u] ← ∞
                pai[u] ← NIL

            cor[s] ← CINZA
            distancia[s] ← 0
            pai[s] ← NIL

            crie uma fila Q
            ENFILEIRA(Q, s)

            enquanto Q não estiver vazia faça
                u ← DESENFILEIRA(Q)

                para cada vértice v ∈ G.Adj[u] faça
                    se cor[v] = BRANCO então
                        cor[v] ← CINZA
                        distancia[v] ← distancia[u] + 1
                        pai[v] ← u
                        ENFILEIRA(Q, v)

                cor[u] ← PRETO
"""

import numpy
from maze_generator import Maze 

MAZE_DEPTH = 10
MAZE_WIDTH = 10

class BreadthFirstSearch(Maze):
    def __init__(self, depth, width):
        super().__init__(depth, width)
        self.i = 0
        self.j = 0
        self.iterations = 0
        #self.possibilities = {"UP": 'Y', "D": 'A', "LEFT": 'X', "RIGHT": 'B'}
        self.color = numpy.full((self.depth, self.width), "WHITE", dtype=object)
        self.father = numpy.full((self.depth, self.width), "NIL",dtype=object)
        self.distance = numpy.full((self.depth, self.width), numpy.iinfo(numpy.int64).max, dtype=int)


if __name__ == "__main__":
    breadthFirstSearch = BreadthFirstSearch(MAZE_DEPTH, MAZE_WIDTH)
    print(breadthFirstSearch.color, "\n")
    print(breadthFirstSearch.father, "\n")
    print(breadthFirstSearch.distance, "\n")
