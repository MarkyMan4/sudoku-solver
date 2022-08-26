import random
from typing import List
from sudoku_solver.graph import Graph

BOARD_SIZE = 9
REGION_SIZE = 3

class Solver:
    def __init__(self, board: List[List[int]] = None):
        self.colors = [i + 1 for i in range(BOARD_SIZE)]

        # board is represented as a 1D list
        self.board = [0 for _ in range(BOARD_SIZE ** 2)]
        self.counts = [20 for _ in range(BOARD_SIZE ** 2)]

        if board:
            self.board = []

            for i in range(len(board)):
                for j in range(len(board[i])):
                    self.board.append(board[i][j])

        self.known_cells = []

        for i in range(len(self.board)):
            if self.board[i] != 0:
                self.known_cells.append(i)

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

    # find the vertex that the largest number of colored cells are connected to
    def get_converging_vertex(self):
        max_connections = 0
        max_vertex = 0

        for vertex in self.graph.vertices:
            if vertex in self.known_cells:
                continue

            connections_to_known = 0
            
            for edge in self.graph.edges[vertex]:
                if edge in self.known_cells:
                    connections_to_known += 1
            
            if connections_to_known > max_connections:
                max_connections = connections_to_known
                max_vertex = vertex

        return max_vertex

    def color_graph(self):
        for _ in range(10):
            max_vertex = self.get_converging_vertex()
            color_options = [color for color in self.colors if color not in self.graph.get_adj_values(max_vertex)]

            if len(color_options) == 1:
                self.graph.update_vertex(max_vertex, color_options[0])
                self.known_cells.append(max_vertex)

            print(max_vertex)
            print(color_options)


        # visited = []

        # for vertex in self.graph.edges.keys():
        #     if vertex in visited:
        #         continue

        #     queue = []
        #     visited.append(vertex)
        #     queue.append(vertex)

        #     while len(queue) > 0:
        #         next_v = queue.pop(0)
        #         vertex_value = self.graph.vertices[next_v]

        #         # print(f'looking at edges for node {next_v} with value {vertex_value}')

        #         for edge in self.graph.edges[next_v]:
        #             edge_value = self.graph.vertices[edge]

        #             if vertex_value == edge_value and edge not in self.known_cells:
        #                 edge_value += 1

        #                 self.graph.update_vertex(edge, edge_value)

        #             if edge_value in self.graph.get_adj_values(edge) or edge not in visited:
        #                 queue.append(edge)

        #             if edge not in visited:
        #                 visited.append(edge)

        res = []
        row = []

        for i, vertex in enumerate(self.graph.vertices):
            print('%3s' % self.graph.vertices[vertex], end=' ')
            row.append(self.graph.vertices[vertex])

            if (i + 1) % 9 == 0:
                print()
                res.append(row)
                row = []

        print('-----------------------------')

        return res
