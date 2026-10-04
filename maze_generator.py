""""
@brief  Esse arquivo contém a classe Maze, responsável por gerar 
        o labirinto de maneira pseudo-randômica. os algoritmos de 
        solução usarão essa classe em uma composição.
"""

import numpy
import random

MAZE_DEPTH = 10
MAZE_WIDTH = 10

WALL_FLAG = 0
ROUTE_FLAG = 1
INIT_FLAG = 2
END_FLAG = 3

class Maze:

    def __init__(self, depth, width):
        self.depth = depth
        self.width = width
        self.__i = 0
        self.__j = 0
        self.maze = numpy.zeros((depth, width), dtype=int)
        self._solution = numpy.zeros((depth, width), dtype=int)
        self._generate_maze()
        self._trace_route()


    def _generate_maze(self):
        for i in range(self.depth):
            for j in range(self.width):
                if (i == 0) or (i == self.depth - 1):
                    self.maze[i][j] = WALL_FLAG
                else: 
                    self.maze[i][j] = random.choices(
                        [WALL_FLAG, ROUTE_FLAG],
                        weights=[65, 35],
                        k=1
                    )[0]


    def __walk_in_maze(self):

        ngbr = [(self.__i - 1,     self.__j) if (self.__i - 1) >= 0         else None,      #up
                (self.__i + 1,     self.__j) if (self.__i + 1) < self.depth else None,      #down
                (self.__i    , self.__j - 1) if (self.__j - 1) >= 0         else None,      #left
                (self.__i    , self.__j + 1) if (self.__j + 1) < self.width else None]      #right

        route_decision = random.randint(1, 3)       #up move is blocked to avoid infinite recursion
        if ngbr[route_decision] is None: return self.__walk_in_maze()

        match route_decision:
            case 0:
                self.__i -= 1
                self.maze[self.__i][self.__j] = 1
                self._solution[self.__i][self.__j] = 1

            case 1:
                self.__i += 1
                self.maze[self.__i][self.__j] = 1
                self._solution[self.__i][self.__j ] = 1

            case 2:
                self.__j -= 1
                self.maze[self.__i][self.__j] = 1
                self._solution[self.__i][self.__j] = 1

            case 3:
                self.__j += 1
                self.maze[self.__i][self.__j] = 1
                self._solution[self.__i][self.__j] = 1


    def _trace_route(self):

        if self.__i == (self.depth - 1):
            self.maze[self.__i][self.__j] = END_FLAG
            self._solution [self.__i][self.__j] = END_FLAG
            self.__i = 0
            self.__j = 0
            return
        
        elif self.__i == 0:
            self.__j = random.randint(0, self.width - 1)
            self.maze[self.__i][self.__j] = INIT_FLAG
            self._solution [self.__i][self.__j] = INIT_FLAG
            self.maze[self.__i + 1][self.__j] = ROUTE_FLAG
            self._solution [self.__i + 1][self.__j] = ROUTE_FLAG
            self.__i += 1

        else: 
            self.__walk_in_maze()

        self._trace_route()


if __name__ == "__main__":
    maze = Maze(MAZE_DEPTH, MAZE_WIDTH)
    print(maze.maze, "\n")
