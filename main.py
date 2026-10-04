"""
@brief  Esse arquivo contém a classe MazeRunner, responsável por
        aplicar os métodos de busca, comparar os resultados e entregar
        os outputs requeridos na descrição da avaliação
"""

import numpy
from maze_generator import Maze 

x = 10
y = 10

methods = {"Idle": 0b0000, "BFS": 0b0001, "DFS": 0b0010}

class MazeRunner(Maze):
    def __init__(self, algorithm_mask):
        super().__init__(x, y)

        self.i = 0
        self.j = 0
        self.algorithm_mask = algorithm_mask
        self.possibilities = {"UP": 'Y', "D": 'A', "LEFT": 'X', "RIGHT": 'B'}
        self.map = numpy.zeros((super().depth, super().width), dtype=int)


if __name__ == "__main__":
    mazeRunner = MazeRunner(methods["Idle"])



