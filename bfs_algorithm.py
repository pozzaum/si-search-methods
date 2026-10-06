"""
@authors    Gabriela Guse Machado e Pedro Santos Pozza

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
from collections import deque
from maze_generator import Maze 

MAZE_DEPTH = 10
MAZE_WIDTH = 10

WALL_FLAG = 0
ROUTE_FLAG = 1
INIT_FLAG = 2
END_FLAG = 3

class BreadthFirstSearch():
    def __init__(self, mazeClass):
        self.mazeClass = mazeClass
        self.__u = (0, 0)
        self.__v = [(0, 0),
                    (0, 0),
                    (0, 0),
                    (0, 0)]
        self.iterations = 0
        self.mirror_solution = numpy.zeros((self.mazeClass.depth, self.mazeClass.width), dtype=int)
        self.color = numpy.full((self.mazeClass.depth, self.mazeClass.width), "WHITE", dtype=object)
        self.distance = numpy.full((self.mazeClass.depth, self.mazeClass.width), numpy.iinfo(numpy.int64).max, dtype=int)
        self.father = numpy.full((self.mazeClass.depth, self.mazeClass.width), "NIL",dtype=object)


    def bfs_algorithm(self, s):
        for j in range (self.mazeClass.width) :
            if self.mazeClass.maze[0][j]: s = (0, j)

        self.color[s] = "CINZA"
        self.distance[s] = 0
        self.father[s] = "NIL"

        Q = deque()
        self.__bfs_enqueue(Q, s)

        while Q:
            self.__u = self.__bfs_dequeue(Q)

            self.__v = [(self.__u[0] - 1,     self.__u[1]) if (self.__u[0] - 1) >= 0                   else None,
                        (self.__u[0] + 1,     self.__u[1]) if (self.__u[0] + 1) < self.mazeClass.depth else None,
                        (self.__u[0]    , self.__u[1] - 1) if (self.__u[1] - 1) >= 0                   else None,
                        (self.__u[0]    , self.__u[1] + 1) if (self.__u[1] + 1) < self.mazeClass.width else None]
            
            for i in range (len(self.__v)):
                if (self.__v[i] is not None) and (self.mazeClass.maze[self.__v[i]] > WALL_FLAG) and (self.color[self.__v[i]] == "WHITE"):
                    self.color[self.__v[i]] = "GREY"
                    self.distance[self.__v[i]] = self.distance[self.__u] + 1
                    self.father[self.__v[i]] = self.__u
                    self.__bfs_enqueue(Q, self.__v[i])

            self.color[self.__u] = "BLACK"
            if self.__u[0] == 0:
                self.mirror_solution[self.__u] = INIT_FLAG
            elif self.__u[0] == (self.mazeClass.depth - 1):
                self.mirror_solution[self.__u] = END_FLAG
            else:
                self.mirror_solution[self.__u] = ROUTE_FLAG


    def __bfs_enqueue(self, Q, s):
        return Q.append(s)


    def __bfs_dequeue(self, Q):
        return Q.popleft()


if __name__ == "__main__":
    mazeClass = Maze(MAZE_DEPTH, MAZE_WIDTH)
    breadthFirstSearch = BreadthFirstSearch(mazeClass)
    breadthFirstSearch.bfs_algorithm((0, 0))

    print("METODO BFS:\n")
    print("Labirinto gerado:\n")
    print(mazeClass.maze, "\n")
    print("Caminho gerado randomicamente:\n")
    print(mazeClass.get_solution(), "\n")
    print("Caminho encontrado pelo algoritmo BFS:\n")
    print(breadthFirstSearch.mirror_solution, "\n")
    print("Cores dos vertices:\n")
    print(breadthFirstSearch.color, "\n")
    print("Vertices pais:\n")
    print(breadthFirstSearch.father, "\n")
    print("Distancias:\n")
    print(breadthFirstSearch.distance, "\n")
