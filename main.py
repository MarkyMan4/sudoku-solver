from sudoku_solver.solver import Solver

def main():
    # read in file and format as 2d array
    with open('puzzles/test_0') as f:
        lines = f.readlines()

    lines = [line.replace('\n', '') for line in lines]
    puzzle = []
    
    for line in lines:
        row = []
        for num in line:
            row.append(int(num))

        puzzle.append(row)

    s = Solver(puzzle)
    res = s.color_graph()


if __name__ == '__main__':
    main()
