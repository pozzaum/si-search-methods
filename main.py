"""
@brief  Esse arquivo contém a classe MazeRunner, responsável por
        aplicar os métodos de busca, comparar os resultados e entregar
        os outputs requeridos na descrição da avaliação
"""

import numpy
from maze_generator import Maze 

MAZE_DEPTH = 10
MAZE_WIDTH = 10

class MazeRunner(Maze):
    def __init__(self):
        super().__init__(MAZE_DEPTH, MAZE_WIDTH)


if __name__ == "__main__":
    a = 0



