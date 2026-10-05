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

@reference  CORMEN, Thomas H.; LEISERSON, Charles E.; RIVEST, Ronald L.; STEIN, Clifford.
            Introduction to Algorithms. 4. ed. Cambridge: MIT Press, 2022.
"""

import numpy
from maze_generator import Maze 

MAZE_DEPTH = 8
MAZE_WIDTH = 8

WALL_FLAG = 0
ROUTE_FLAG = 1
INIT_FLAG = 2
END_FLAG = 3

class BreadthFirstSearch():
    def __init__(self, maze):
        self.maze = maze
        self.i = 0
        self.j = 0
        self.iterations = 0
        self.color = numpy.full((self.maze.depth, self.maze.width), "WHITE", dtype=object)
        self.father = numpy.full((self.maze.depth, self.maze.width), "NIL",dtype=object)
        self.distance = numpy.full((self.maze.depth, self.maze.width), numpy.iinfo(numpy.int64).max, dtype=int)


if __name__ == "__main__":
    maze = Maze(MAZE_DEPTH, MAZE_WIDTH)
    breadthFirstSearch = BreadthFirstSearch(maze)
    print(breadthFirstSearch.color, "\n")
    print(breadthFirstSearch.father, "\n")
    print(breadthFirstSearch.distance, "\n")
