from graph import Graph

BOARD_SIZE = 9

# create a graph that represents sudoku board
# a cell represents a vertex
# each vertex is connected to all vertices within the same row, column and region
g = Graph()

cells = [i for i in range(BOARD_SIZE ** 2)]

for cell in cells:
    # add edges to cells within row
    i = cell
    while i % BOARD_SIZE != 0:
        i -= 1
        g.add_edge(cell, i)

    i = cell
    while (i + 1) % BOARD_SIZE != 0:
        i += 1
        g.add_edge(cell, i)

    # add edges to cells within column
    i = cell
    while i - BOARD_SIZE > 0:
        i -= BOARD_SIZE
        g.add_edge(cell, i)

    i = cell
    while i + BOARD_SIZE < BOARD_SIZE ** 2:
        i += BOARD_SIZE
        g.add_edge(cell, i)

    # add edges to cells within region
    # g.add_edge()

print(g.graph[31])

# g.add_edge(1, 2)
# g.add_edge(1, 3)
# g.add_edge(2, 3)
# g.add_edge(2, 4)

