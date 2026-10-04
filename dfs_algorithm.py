"""
@brief      Esse arquivo contém a implementação da busca em profundidade
            e demais métodos necessários.

@details    pseudocódigo:

            DFS(G):

            para cada vértice u ∈ G.V faça
                color[u] ← BRANCO
                father[u] ← NIL

            tempo ← 0

            para cada vértice u ∈ G.V faça
                se color[u] = BRANCO então
                    DFS_VISIT(G, u)

            DFS_VISIT(G, u):

            tempo ← tempo + 1
            descoberta[u] ← tempo

            color[u] ← CINZA

            para cada vértice v ∈ G.Adj[u] faça
                se color[v] = BRANCO então
                    father[v] ← u
                    DFS_VISIT(G, v)

            color[u] ← PRETO

            tempo ← tempo + 1
            finalizacao[u] ← tempo
"""

import numpy
from maze_generator import Maze 

MAZE_DEPTH = 10
MAZE_WIDTH = 10

class DepthFirstSearch(Maze):
    def __init__(self, depth, width):
        super().__init__(depth, width)
        self.i = 0
        self.j = 0
        self.iterations = 0
        #self.possibilities = {"UP": 'Y', "D": 'A', "LEFT": 'X', "RIGHT": 'B'}
        self.color = numpy.full((self.depth, self.width), "WHITE", dtype=object)
        self.father = numpy.full((self.depth, self.width), "NIL",dtype=object)
        self.distance = numpy.full((self.depth, self.width), numpy.iinfo(numpy.int64).max, dtype=int)

    def _dfs_visit(self):
        self.iteration += 1



if __name__ == "__main__":
    depthFirstSearch = DepthFirstSearch(MAZE_DEPTH, MAZE_WIDTH)
    print(depthFirstSearch.color, "\n")
    print(depthFirstSearch.father, "\n")
    print(depthFirstSearch.distance, "\n")