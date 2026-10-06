"""
@brief  Esse arquivo contém a classe MazeRunner, responsável por
        aplicar os métodos de busca, comparar os resultados e entregar
        os outputs requeridos na descrição da avaliação
"""

import numpy

from maze_generator import Maze
from bfs_algorithm import BreadthFirstSearch
from dfs_algorithm import DepthFirstSearch


MAZE_DEPTH = 10
MAZE_WIDTH = 10

WALL_FLAG = 0
ROUTE_FLAG = 1
INIT_FLAG = 2
END_FLAG = 3

NUMBER_OF_TESTS = 100

class MazeRunner(Maze):

    def __init__(self):
        super().__init__(MAZE_DEPTH, MAZE_WIDTH)

    def find_start_end(self):
        start = numpy.argwhere(
            self.maze == INIT_FLAG
        )
        end = numpy.argwhere(
            self.maze == END_FLAG
        )
        start = tuple(int(index) for index in start[0])
        end = tuple(int(index) for index in end[0])

        return start, end


    def reconstruct_path(self, father, start, end):
        path = []
        current = end
        while current != start:
            path.append(current)
            if father[current] == "NIL":
                return []
            current = father[current]
        path.append(start)
        path.reverse()
        return path


    def validate_path(self, path):
        if len(path) == 0:
            return False
        # Começo correto
        if self.maze[path[0]] != INIT_FLAG:
            return False
        # Final correto
        if self.maze[path[-1]] != END_FLAG:
            return False
        for i in range(len(path)):
            current = path[i]

            # Não pode passar por parede
            if self.maze[current] == WALL_FLAG:
                return False
            if i < len(path) - 1:
                next_position = path[i + 1]
                delta_i = abs(
                    current[0] - next_position[0]
                )
                delta_j = abs(
                    current[1] - next_position[1]
                )
                # Só aceita movimentos ortogonais
                if delta_i + delta_j != 1:
                    return False
        return True

def test_100_mazes():

    bfs_success = 0
    bfs_failure = 0
    dfs_success = 0
    dfs_failure = 0

    for test in range(NUMBER_OF_TESTS):
        mazeRunner = MazeRunner()
        start, end = mazeRunner.find_start_end()

        # BFS
        bfs = BreadthFirstSearch(mazeRunner)
        bfs.bfs_algorithm(start)
        bfs_path = mazeRunner.reconstruct_path(
            bfs.father,
            start,
            end
        )
        if mazeRunner.validate_path(bfs_path):
            bfs_success += 1
        else:
            bfs_failure += 1

        # DFS
        dfs = DepthFirstSearch(mazeRunner)
        dfs.dfs_algorithm()
        dfs_path = mazeRunner.reconstruct_path(
            dfs.father,
            start,
            end
        )
        if mazeRunner.validate_path(dfs_path):
            dfs_success += 1
        else:
            dfs_failure += 1

    print("TESTE DE 100 LABIRINTOS")
    print("\nBFS")
    print("Sucessos:", bfs_success)
    print("Falhas:", bfs_failure)
    print(
        f"Porcentagem de sucesso: "
        f"{(bfs_success / NUMBER_OF_TESTS) * 100:.2f}%"
    )
    print(
        f"Porcentagem de falha: "
        f"{(bfs_failure / NUMBER_OF_TESTS) * 100:.2f}%"
    )
    print("\nDFS")
    print("Sucessos:", dfs_success)
    print("Falhas:", dfs_failure)
    print(
        f"Porcentagem de sucesso: "
        f"{(dfs_success / NUMBER_OF_TESTS) * 100:.2f}%"
    )
    print(
        f"Porcentagem de falha: "
        f"{(dfs_failure / NUMBER_OF_TESTS) * 100:.2f}%"
    )

def show_single_maze_paths():

    mazeRunner = MazeRunner()
    start, end = mazeRunner.find_start_end()
    print("LABIRINTO")
    print()
    print(mazeRunner.maze)
    print("\nInício:", start)
    print("Fim:", end)

    # BFS

    bfs = BreadthFirstSearch(mazeRunner)
    bfs.bfs_algorithm(start)
    bfs_path = mazeRunner.reconstruct_path(
        bfs.father,
        start,
        end
    )

    print("CAMINHO BFS")
    print()

    if mazeRunner.validate_path(bfs_path):
        print(*bfs_path, sep=" -> ")
        print(
            "\nQuantidade de movimentos:",
            len(bfs_path) - 1
        )

    else:
        print("BFS não encontrou um caminho válido.")
    print("\nMATRIZ DE SAÍDA BFS")
    print(bfs.mirror_solution)


    # DFS
    dfs = DepthFirstSearch(mazeRunner)
    dfs.dfs_algorithm()
    dfs_path = mazeRunner.reconstruct_path(
        dfs.father,
        start,
        end
    )
    print("CAMINHO DFS")
    print()

    if mazeRunner.validate_path(dfs_path):
        print(*dfs_path, sep=" -> ")
        print(
            "\nQuantidade de movimentos:",
            len(dfs_path) - 1
        )

    else:
        print("DFS não encontrou um caminho válido.")
    print("\nMATRIZ DE SAÍDA DFS")
    print(dfs.mirror_solution)

    
if __name__ == "__main__":
    test_100_mazes()
    show_single_maze_paths()
