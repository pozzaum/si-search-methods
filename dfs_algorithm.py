"""
@brief      Esse arquivo contém a implementação da busca em profundidade
            e demais métodos necessários.

@details    pseudocódigo:

            DFS(G):

            para cada vértice u ∈ G.V faça
                color[u] ← WHITE
                father[u] ← NIL

            tempo ← 0

            para cada vértice u ∈ G.V faça
                se color[u] = WHITE então
                    DFS_VISIT(G, u)

            DFS_VISIT(G, u):

            tempo ← tempo + 1
            descoberta[u] ← tempo

            color[u] ← GREY

            para cada vértice v ∈ G.Adj[u] faça
                se color[v] = WHITE então
                    father[v] ← u
                    DFS_VISIT(G, v)

            color[u] ← BLACK

            tempo ← tempo + 1
            finalizacao[u] ← tempo
"""

import numpy
from maze_generator import Maze 

MAZE_DEPTH = 20
MAZE_WIDTH = 20

WALL_FLAG = 0
ROUTE_FLAG = 1
INIT_FLAG = 2
END_FLAG = 3

class DepthFirstSearch():
    def __init__(self, mazeClass):
        self.mazeClass = mazeClass
        self.__u = (0, 0)
        self.__v = [(0, 0),
                    (0, 0),
                    (0, 0),
                    (0, 0)]
        self.iteration = 0
        self.mirror_solution = numpy.zeros((self.mazeClass.depth, self.mazeClass.width), dtype=int)
        self.color = numpy.full((self.mazeClass.depth, self.mazeClass.width), "WHITE", dtype=object)
        self.father = numpy.full((self.mazeClass.depth, self.mazeClass.width), "NIL",dtype=object)
        self.discovery = numpy.zeros((self.mazeClass.depth, self.mazeClass.width), dtype=int)
        self.finalization = numpy.zeros((self.mazeClass.depth, self.mazeClass.width), dtype=int)



    def dfs_algorithm(self):
        for i in range(self.mazeClass.depth):
            for j in range(self.mazeClass.width):
                if (self.mazeClass.maze[i][j] > WALL_FLAG) and (self.color[i][j] == "WHITE"):
                    self.__u = (i, j)
                    if(self.mazeClass.maze[self.__u] == END_FLAG): 
                        return
                    else:
                        self._dfs_visit(self.__u)


    def _dfs_visit(self, u):

        self.iteration += 1
        self.discovery[u] = self.iteration
        self.color[u] = "GREY"
        self.mirror_solution[u] = ROUTE_FLAG

        self.__v = [(u[0] - 1,     u[1]) if (u[0] - 1) >= 0                   else None,
                    (u[0] + 1,     u[1]) if (u[0] + 1) < self.mazeClass.depth else None,
                    (u[0]    , u[1] - 1) if (u[1] - 1) >= 0                   else None,
                    (u[0]    , u[1] + 1) if (u[1] + 1) < self.mazeClass.width else None]
        
        for i in range (len(self.__v)):
            if (self.__v[i] is not None) and (self.mazeClass.maze[self.__v[i]] > WALL_FLAG) and (self.color[self.__v[i]] == "WHITE"):
                self.father[self.__v[i]] = (u)
                self._dfs_visit(self.__v[i])

        self.color[u] = "BLACK"

        if(self.mazeClass.maze[u] == INIT_FLAG):
            self.mirror_solution[u] = INIT_FLAG
        else:
            self.mirror_solution[u] = ROUTE_FLAG

        self.iteration += 1
        self.finalization[u] = self.iteration


if __name__ == "__main__":
    mazeClass = Maze(MAZE_DEPTH, MAZE_WIDTH)
    depthFirstSearch = DepthFirstSearch(mazeClass)
    depthFirstSearch.dfs_algorithm()

    print(mazeClass.maze, "\n")
    print(mazeClass._solution, "\n")
    #print(depthFirstSearch.mirror_solution, "\n")
    #print(depthFirstSearch.color, "\n")
    #print(depthFirstSearch.father, "\n")
    if (mazeClass.maze == depthFirstSearch.mirror_solution).all():
        print("Possivel erro: dfs igual a labirinto")