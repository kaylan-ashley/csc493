#!/usr/bin/env python3
"""
Compute the lengths and total number of induced paths on a hex grid.

NOTE: If you are running this program in a bash shell, the optional 
      argument cell_to_avoid requires quotation marks around it. 
      ex: python hex_v4.py 3 4 "(1, 1)"
"""
__author__ = "Kaylan Arnoldt-Smith"
__email__ = "k.arnoldt.smith@mail.utoronto.ca"

import argparse
import random
import time

RED = True
BLUE = False

parser = argparse.ArgumentParser()
parser.add_argument('rows', type=int, help='number of rows in the grid')
parser.add_argument('cols', type=int, help='number of columns in the grid')
parser.add_argument('cell_to_avoid', type=str, nargs='?', default=None,
                    help='coordinates of cell to avoid')
parser.add_argument('--interactive', action='store_true', 
                    help='enable interactive mode')
parser.add_argument('--visual', action='store_true',
                    help='enable visual mode')

args = parser.parse_args()
rows = args.rows
cols = args.cols
if args.cell_to_avoid:
    x, y = (int(c.strip("(), []")) for c in args.cell_to_avoid.split(','))
    if 0 <= x < cols and 0 <= y < rows:
        cell_to_avoid = (x, y)
    else:
        cell_to_avoid = None
else:
    cell_to_avoid = None
interactive = args.interactive
visual = args.visual

possible_moves = [(0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0)]

all_lengths_red = {}
lengths_avoiding_cell_red = {}
all_lengths_blue = {}
lengths_avoiding_cell_blue = {}


class Path:
    def __init__(self, last, all_but_last):
        self.last = last
        self.all_but_last = all_but_last


def add_length(length, distr):
    if length in distr:
        distr[length] += 1
    else:
        distr[length] = 1


def is_minimal(path, tile):
    for m in possible_moves:
        if (tile[0] + m[0], tile[1] + m[1]) in path.all_but_last:
            return False
    return True


def is_in_bounds(rows, cols, next_move):
    if 0 <= next_move[0] < cols:
        if 0 <= next_move[1] < rows:
            return True
    return False


def print_result(all_lengths, lengths_avoiding_cell):
    lst = sorted(all_lengths.items(), key=lambda x: (x[0]))
    num_paths = sum(all_lengths.values())
    num_paths_avoiding_cell = sum(lengths_avoiding_cell.values())

    print("\n# of minimal paths: " + str(num_paths))
    print("length distribution of minimal paths:")
    print(lst)

    if cell_to_avoid:
        avoid_lst = sorted(lengths_avoiding_cell.items(), key=lambda x: (x[0]))
        print("\n# of minimal paths avoiding cell " + str(cell_to_avoid) \
              + ": " + str(num_paths_avoiding_cell))
        print("length distribution of minimal paths that avoid cell " \
              + str(cell_to_avoid) + ":")
        print(avoid_lst)

    print("")


def print_grid(rows, cols, red_moves, blue_moves):

    lst = sorted(all_lengths_red.items(), key=lambda x: (x[0]))
    print("\nlength distribution of minimal winning paths remaining (Red): ")
    print(lst)

    # print top part of top row of hexes
    line = "\n     "
    for _ in range(0, cols):
        line += "/ \\ "
    print(line)

    for j in range(0, rows):
        row_index = (rows - 1) - j; # grid row index (reverse order)
        line = ""

        # print y label
        for _ in range(0, (2*j)+1):
            line += " "
        line += ("\033[34m" + "\033[1m" + str(row_index) + "\033[0m" + "  | ")

        # print middle part of hexes
        for i in range(0, cols):
            if (i, row_index) in red_moves:
                line += "\033[0;31m" + "\033[1m" + "r" + "\033[0m"
            elif (i, row_index) in blue_moves:
                line += "\033[34m" + "\033[1m" + "b" + "\033[0m"
            else:
                line += " "
            line += " | "
        print(line)

        # print bottom part of hexes
        line = "     "
        for _ in range(0, j*2):
            line += " "
        for _ in range(0, cols):
            line += "\\ / "
        if j != rows-1: 
            line += "\\" # omit last backslash in bottom row
        print(line)

    # print x labels
    line = ""
    for _ in range(0, (2*rows)-1):
        line += " "
    line += "       "
    for i in range(0, cols):
        line += ("\033[0;31m" + "\033[1m" + str(i) + "   " + "\033[0m")
    print(line + "\n")


def compute_paths(rows, cols, cell_to_avoid, player):
    q = []
    paths = []
    all_lengths = {}
    lengths_avoiding_cell = {}
    global all_lengths_red
    global all_lengths_blue
    global lengths_avoiding_cell_red
    global lengths_avoiding_cell_blue

    # add starting tiles to queue
    for i in range(0, cols):
        new_path = Path((i, 0), set())
        q.append(new_path)

    # edge case
    if rows == 1:
        all_lengths[1] = cols
        num_paths = cols

        lengths_avoiding_cell[1] = cols
        if cell_to_avoid:
            lengths_avoiding_cell[1] -= 1
        num_paths_avoiding_cell = lengths_avoiding_cell[1]

        # for consistency, remove key if value is 0
        if lengths_avoiding_cell[1] == 0:
            del lengths_avoiding_cell[1]

        # generate list of paths
        for i in range(0, cols):
            paths.append(set([(i, 0)]))

        all_lengths_red = all_lengths
        lengths_avoiding_cell_red = lengths_avoiding_cell

        return paths

    while q:
        p = q.pop() # p is a partial minimal path stored as a Path object

        for m in possible_moves:
            next_move = (p.last[0] + m[0], p.last[1] + m[1])

            if is_in_bounds(rows, cols, next_move) and is_minimal(p, next_move):

                # if the next move puts us in the "goal" row
                if next_move[1] == rows - 1:

                    # add length to overall distribution of lengths
                    path_length = len(p.all_but_last) + 2
                    add_length(path_length, all_lengths)

                    # if path does not include cell to be avoided, add length
                    # to distribution of lengths of paths avoiding cell
                    if cell_to_avoid:
                        if next_move != cell_to_avoid and p.last != cell_to_avoid:
                            if cell_to_avoid not in p.all_but_last:
                                add_length(path_length, lengths_avoiding_cell)

                    # add path to list of paths
                    new_path = p.all_but_last.copy()
                    new_path.add(p.last)
                    new_path.add(next_move)
                    paths.append(new_path)

                # if the next move doesn't put us back in the starting row
                elif next_move[1] != 0:

                    # add path augmented with next move to queue
                    new_path = Path(next_move, p.all_but_last.copy())
                    new_path.all_but_last.add(p.last)
                    q.append(new_path)

    if player == RED:
        all_lengths_red = all_lengths
        lengths_avoiding_cell_red = lengths_avoiding_cell
    else:
        all_lengths_blue = all_lengths
        lengths_avoiding_cell_blue = lengths_avoiding_cell
    return paths


def get_open_tiles(rows, cols, red_moves, blue_moves):
    open_tiles = []
    for x in range(0, cols):
        for y in range(0, rows):
            if (x,y) not in red_moves | blue_moves:
                open_tiles.append((x, y))
    return open_tiles


if (interactive):
    game_over = 0 # initialize game loop
    turn = RED # red goes first
    red_moves = set() 
    blue_moves = set()

    # Compute sets of minimal winning paths for Red and Blue
    red_paths = compute_paths(rows, cols, None, RED)
    if rows == cols:
        blue_paths = red_paths.copy() # saves time, especially on larger grids
    else:
        blue_paths = compute_paths(cols, rows, None, BLUE) 

    # We computed the set of Blue paths by rotating the board 90 degrees,
    # so we need to swap the coordinates of the tiles in those paths.
    for i in range(0, len(blue_paths)):
        path = set()
        for tile in blue_paths[i]:
            path.add((tile[1], tile[0]))
        blue_paths[i] = path

    while not game_over:
        
        # print game state and get user input
        while True:             
            if visual:
                print_grid(rows, cols, red_moves, blue_moves)
            else:
                lst = sorted(all_lengths_red.items(), key=lambda x: (x[0]))
                print("\nlength distribution of minimal winning paths remaining (Red): ")
                print(lst)
                
                print("\nRed tiles: " + str(list(red_moves)))
                print("Blue tiles: " + str(list(blue_moves)) + "\n")

            if turn == RED:
                print("Red's turn")
            else:
                print("Blue's turn")
            
            print("(1) Place a stone at (x,y)")
            print("(2) Place a random stone")
            if turn == RED: 
                print("(3) Play the potential strategy")
            print("(x) Exit")

            opt = input("Choose an option: ").strip("() ")
            if opt == 'x':
                exit(0)
            elif opt in ['1', '2'] or (opt == '3' and turn == RED):
                break
            else:
                print("Option not recognized. Please try again.")

        # let the player choose a tile
        if opt == '1':
            while True:
                try:
                    x, y = (int(c.strip("()[] ")) for c in input("Please enter x,y coordinates: ").split(','))
                    next_move = (x, y)
                    if is_in_bounds(rows, cols, next_move) and next_move not in red_moves | blue_moves:
                        break
                    else:
                        print("Invalid move. Please try again.")
                except:
                    print("Cannot read input. Please try again.")                  

        # choose a random tile
        elif opt == '2':
            open_tiles = get_open_tiles(rows, cols, red_moves, blue_moves)
            next_move = open_tiles[random.randint(0, len(open_tiles)-1)]

        # play the potential strategy
        elif opt == '3' and turn == RED:

            # initialize variables
            open_tiles = get_open_tiles(rows, cols, red_moves, blue_moves)
            next_move = open_tiles[0]
            next_move_potential = 0
            for path in blue_paths:
                if next_move not in path:
                    next_move_potential += (1/2)**(len(path.difference(blue_moves)))

            # find a tile that minimizes the potential function
            for move in open_tiles[1:]:
                move_potential = 0
                for path in blue_paths:
                    if move not in path:
                        move_potential += (1/2)**(len(path.difference(blue_moves)))
                if move_potential < next_move_potential:
                    next_move = move
                    next_move_potential = move_potential

        if turn == RED:
            red_moves.add(next_move)

            # check win condition
            for path in red_paths:
                if path.issubset(red_moves): 
                    game_over = True
                    endgame_message = "Red wins!"
                    if visual: # add color
                        endgame_message = "\033[0;31m" + endgame_message + "\033[0m"

            # remove minimal winning paths containing new Red tile from Blue's path set
            new_blue_paths = [p for p in blue_paths if next_move not in p]
            blue_paths = new_blue_paths

            # rebuild path length dictionary
            all_lengths_blue = {}
            for path in blue_paths:
                path_length = len(path)
                if path_length in all_lengths_blue:
                    all_lengths_blue[path_length] += 1
                else:
                    all_lengths_blue[path_length] = 1

        else:
            blue_moves.add(next_move)
            
            # check win condition
            for path in blue_paths:
                if path.issubset(blue_moves):
                    game_over = True
                    endgame_message = "Blue wins!"
                    if visual: # add color
                        endgame_message = "\033[34m" + endgame_message + "\033[0m"

            # remove minimal winning paths containing new Blue tile from Red's path set
            new_red_paths = [p for p in red_paths if next_move not in p]
            red_paths = new_red_paths

            # rebuild path length dictionary
            all_lengths_red = {}
            for path in red_paths:
                path_length = len(path)
                if path_length in all_lengths_red:
                    all_lengths_red[path_length] += 1
                else:
                    all_lengths_red[path_length] = 1

        # if there are no remaining open tiles, the game is a draw
        if not get_open_tiles(rows, cols, red_moves, blue_moves) and not game_over:
            game_over = True
            endgame_message = "It's a draw."

        turn = not turn # end turn

    # print final game state and declare winner
    if visual:
        print_grid(rows, cols, red_moves, blue_moves)
    else:
        lst = sorted(all_lengths_red.items(), key=lambda x: (x[0]))
        print("\nlength distribution of minimal winning paths remaining (Red): ")
        print(lst)

        print("\nRed tiles: " + str(list(red_moves)))
        print("Blue tiles: " + str(list(blue_moves)) + "\n")
    print(endgame_message)

else:
    compute_paths(rows, cols, cell_to_avoid, RED)
    print_result(all_lengths_red, lengths_avoiding_cell_red)

exit(0)



