""""
@brief  Esse arquivo contém a classe Maze, responsável por gerar 
        o labirinto randômico. Essa classe será herdada pelos 
        algoritmos de solução.
"""

import numpy
import random

class Maze:

    def __init__(self, depth, width):
        self.depth = depth
        self.width = width
        self.__i = 0
        self.__j = 0
        self.maze = numpy.zeros((depth, width), dtype=int)
        self.__solution = numpy.zeros((depth, width), dtype=int)
        self._generate_maze()
        self._trace_route()

    def _generate_maze(self):
        for __i in range(self.depth):
            for __j in range(self.width):
                if (__i == 0) or (__i == self.depth - 1):
                    self.maze[__i][__j] = 0
                else: 
                    self.maze[__i][__j] = random.choices(
                        [0, 1],
                        weights=[70, 30],
                        k=1
                    )[0]

    def _walk_in_width(self):
        width_decision = random.choices(["left", "right"], k=1)[0]

        if width_decision == "left" and self.__j > 0:
            self.__j -= 1
            self.maze[self.__i][self.__j] = 1
            self.__solution[self.__i][self.__j] = 1

        elif width_decision == "right" and self.__j < (self.width - 1):
            self.__j += 1
            self.maze[self.__i][self.__j] = 1
            self.__solution[self.__i][self.__j ] = 1

        elif width_decision == "left" and self.__j == 0:
            self.__j += 1
            self.maze[self.__i][self.__j] = 1
            self.__solution[self.__i][self.__j] = 1

        elif width_decision == "right" and self.__j == (self.width -1):
            self.__j -= 1  
            self.maze[self.__i][self.__j] = 1
            self.__solution[self.__i][self.__j] = 1        


    def _walk_in_depth(self):
        self.__i += 1
        self.maze[self.__i][self.__j] = 1
        self.__solution[self.__i][self.__j] = 1


    def _trace_route(self):

        if self.__i == 0:
            self.__j = random.randint(0, self.width - 1)
            self.maze[self.__i][self.__j] = 2
            self.__solution[self.__i][self.__j] = 2
            self._walk_in_depth()

        if self.__i == (self.depth - 1):
            self.maze[self.__i][self.__j] = 3
            self.__solution[self.__i][self.__j] = 3
            self.__i = 0
            self.__j = 0
            return

        route_decision = random.choices(["width", "depth"], k=1)[0]
        
        if route_decision == "width":
            self._walk_in_width()
        elif route_decision == "depth":
            self._walk_in_depth()

        self._trace_route()


if __name__ == "__main__":
    maze = Maze(20, 20)

    """
    print(maze.__i, "\n")
    print(maze.__j, "\n")
    """
    #print(maze.__solution, "\n")
    print(maze.maze, "\n")
