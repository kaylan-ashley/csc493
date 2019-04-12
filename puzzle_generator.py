import random
from hex import *

GRID_SIZE = 5

# Format: puzzle_number: [rows, cols,
#                         [red cells],
#                         [blue cells]]


def build_random_puzzle():

    red_cells = []
    blue_cells = []

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            num = random.randint(0, 2)
            if num == 0:
                red_cells.append((i, j))
            elif num == 1:
                blue_cells.append((i, j))

    return [GRID_SIZE, GRID_SIZE, red_cells, blue_cells]


def main():

    candidate_puzzles = []

    while True:
        puzzle = build_random_puzzle()

        rows = puzzle[0]
        cols = puzzle[1]
        red_cells = puzzle[2]
        blue_cells = puzzle[3]

        if len(get_open_tiles(rows, cols, set(red_cells), set(blue_cells))) >= 2:
            red_paths = compute_paths(rows, cols, blue_cells, RED, False)
            blue_paths = compute_paths(rows, cols, red_cells, BLUE, False)

            # we use the convention that it is the Blue player's turn
            _, potential = compute_optimal_move(rows,
                                                cols,
                                                set(red_cells),
                                                set(blue_cells),
                                                red_paths,
                                                blue_paths,
                                                BLUE)
            if 0.0 < potential < 1.0 and len(red_cells) - len(blue_cells) == 0:
                if len(blue_cells) < 6:
                    candidate_puzzles.append(puzzle)
                    print_grid(rows, cols,
                               set(red_cells), set(blue_cells),
                               False)
                    _ = input('Press enter to continue')


if __name__ == '__main__':
    main()
