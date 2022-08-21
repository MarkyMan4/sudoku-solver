import random
from typing import List
from sudoku_solver.graph import Graph

BOARD_SIZE = 9
REGION_SIZE = 3

class Solver:
    def __init__(self, board: List[List[int]] = None):
        self.colors = [i for i in range(BOARD_SIZE)]

        # board is represented as a 1D list
        self.board = [0 for _ in range(BOARD_SIZE ** 2)]

        if board:
            self.board = []

            for i in range(len(board)):
                for j in range(len(board[i])):
                    self.board.append(board[i][j])

        self.graph = self.init_graph()

    def init_graph(self) -> Graph:
        # create a graph that represents sudoku board
        # a cell represents a vertex
        # each vertex is connected to all vertices within the same row, column and region
        graph = Graph()
        cells = [i for i in range(BOARD_SIZE ** 2)]

        for i, cell in enumerate(cells):
            # initializing to None for now, this could take in a starting Sudoku board as well
            graph.update_vertex(cell, 1 if self.board[i] == 0 else self.board[i])

        # find the top left of each region
        # hard coding for now, may make this dynamic later to accomodate different board sizes
        regions = [0, 3, 6, 27, 30, 33, 54, 57, 60]

        for cell in cells:
            # add edges to cells within row
            i = cell
            while i % BOARD_SIZE != 0:
                i -= 1
                graph.add_edge(cell, i)

            i = cell
            while (i + 1) % BOARD_SIZE != 0:
                i += 1
                graph.add_edge(cell, i)

            # add edges to cells within column
            i = cell
            while i - BOARD_SIZE > 0:
                i -= BOARD_SIZE
                graph.add_edge(cell, i)

            i = cell
            while i + BOARD_SIZE < BOARD_SIZE ** 2:
                i += BOARD_SIZE
                graph.add_edge(cell, i)

            # add edges to cells within region
            # start by finding the top left of the current region, then iterate through
            # through each cell in that region, adding it as an edge unless it is equal
            # to the current cell, don't add an edge to self

            # determine what region the cell is in
            cell_region = cell
            while cell_region % REGION_SIZE != 0:
                cell_region -= 1

            while cell_region not in regions:
                cell_region -= BOARD_SIZE
            
            # i is now the top left of one of the regions
            # need to iterate through that region and add edges to the current cell
            for i in range(cell_region, cell_region + (BOARD_SIZE * REGION_SIZE), BOARD_SIZE):
                for j in range(i, i + REGION_SIZE):
                    if j != cell and j not in graph.edges[cell]:
                        graph.add_edge(cell, j)

        return graph

    def color_graph(self):
        # shuffled = list(self.graph.vertices.keys())
        # random.shuffle(shuffled)

        # for vertex in shuffled:
        #     if self.graph.vertices[vertex]:
        #         continue
            
        #     adj_vals = self.graph.get_adj_values(vertex)
        #     color = 1

        #     while color in adj_vals:
        #         color += 1

        #     self.graph.update_vertex(vertex, color)

        for vertex in self.graph.edges.keys():
            for edge in self.graph.edges[vertex]:
                if self.graph.vertices[vertex] == self.graph.vertices[edge]:
                    self.graph.update_vertex(edge, self.graph.vertices[edge] + 1)

        for i, vertex in enumerate(self.graph.vertices):
            print('%3s' % self.graph.vertices[vertex], end=' ')

            if (i + 1) % 9 == 0:
                print()
