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
import os
import random
from typing import Dict, List, Set, Tuple

RED = True
BLUE = False
possible_moves = [(0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0)]


class Path:
    def __init__(self, last: Tuple[int, int],
                 all_but_last: Set[Tuple[int, int]]) -> None:
        self.last = last
        self.all_but_last = all_but_last

    def is_minimal(self, tile: Tuple[int, int]) -> bool:
        for m in possible_moves:
            if (tile[0] + m[0], tile[1] + m[1]) in self.all_but_last:
                return False
        return True


def add_length(length: int, distr: Dict[int, int]) -> None:
    if length in distr:
        distr[length] += 1
    else:
        distr[length] = 1


def is_in_bounds(rows: int, cols: int, next_move: Tuple[int, int]) -> bool:
    if 0 <= next_move[0] < cols:
        if 0 <= next_move[1] < rows:
            return True
    return False


def print_summary(all_lengths: Dict[int, int],
                  lengths_avoiding_cell: Dict[int, int]) -> None:
    lst = sorted(all_lengths.items(), key=lambda x: (x[0]))
    num_paths = sum(all_lengths.values())
    num_paths_avoiding_cell = sum(lengths_avoiding_cell.values())

    print("\n# of minimal paths: " + str(num_paths))
    print("length distribution of minimal paths:")
    print(lst)

    if cell_to_avoid:
        avoid_lst = sorted(lengths_avoiding_cell.items(), key=lambda x: (x[0]))
        print("\n# of minimal paths avoiding cell(s) " + str(cell_to_avoid) \
              + ": " + str(num_paths_avoiding_cell))
        print("length distribution of minimal paths that avoid cell(s) " \
              + str(cell_to_avoid) + ":")
        print(avoid_lst)

    print("")


def print_grid(rows: int, cols: int, red_moves: Set[Tuple[int, int]],
               blue_moves: Set[Tuple[int, int]], print_length_distr: bool) -> None:
    #os.system('clear') # clear screen before printing updated grid

    if print_length_distr:
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


def compute_paths(rows: int, cols: int, cell_to_avoid: List[Tuple[int, int]],
                  player: bool, returning_all: bool) -> List[Set[Tuple[int, int]]]:
    """ Precondition: rows > 1
    Note: This function returns all possible paths on an empty grid.
          Given a cell (or multiple cells) to avoid, it will only compute
          the length distribution of paths avoiding those cells.
    """
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

    while q:
        p = q.pop() # p is a Path object containing a partial minimal path

        for m in possible_moves:
            next_move = (p.last[0] + m[0], p.last[1] + m[1])

            if is_in_bounds(rows, cols, next_move) and p.is_minimal(next_move):

                # if the next move puts us in the "goal" row
                if next_move[1] == rows - 1:

                    path_length = len(p.all_but_last) + 2
                    ok_to_add = False

                    # if path does not include cell to be avoided, add length
                    # to distribution of lengths of paths avoiding cell
                    if cell_to_avoid:
                        ok_to_add = True
                        for cell in cell_to_avoid:
                            if player == RED:
                                if next_move == cell or p.last == cell:
                                    ok_to_add = False
                                    break
                                if cell in p.all_but_last:
                                    ok_to_add = False
                                    break
                            else:  # player == BLUE
                                swapped_cell = (cell[1], cell[0])
                                if next_move == swapped_cell:
                                    ok_to_add = False
                                    break
                                if p.last == swapped_cell:
                                    ok_to_add = False
                                    break
                                if swapped_cell in p.all_but_last:
                                    ok_to_add = False
                                    break
                        if ok_to_add:
                            add_length(path_length, lengths_avoiding_cell)

                    add_length(path_length, all_lengths)
                    if ok_to_add or returning_all:
                        new_path = p.all_but_last.copy()
                        new_path.add(p.last)
                        new_path.add(next_move)
                        paths.append(new_path)

                # if the next move doesn't put us back in the starting row
                elif next_move[1] != 0:
                    ok_to_add = True
                    if cell_to_avoid:
                        for cell in cell_to_avoid:
                            if player == RED:
                                if next_move == cell:
                                    ok_to_add = False
                            else:  # player == BLUE
                                swapped_cell = (cell[1], cell[0])
                                if next_move == swapped_cell:
                                    ok_to_add = False
                    if ok_to_add or returning_all:
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

        # We computed the set of Blue paths by rotating the board 90 degrees,
        # so we need to swap the coordinates of the tiles in those paths.
        # print('blue paths before swapping coordinates:')
        # for p in paths:
        #     print(p)
        for i in range(0, len(paths)):
            p = set()
            for tile in paths[i]:
                p.add((tile[1], tile[0]))
            paths[i] = p
        # print('blue paths after swapping coordinates:')
        # for p in paths:
        #     print(p)

    return paths


def get_open_tiles(rows: int, cols: int, red_moves: Set[Tuple[int, int]],
                   blue_moves: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
    open_tiles = []
    for x in range(0, cols):
        for y in range(0, rows):
            if (x, y) not in red_moves and (x, y) not in blue_moves:
                open_tiles.append((x, y))
    return open_tiles


def compute_potential(paths: List[Set[Tuple[int, int]]],
                      moves: Set[Tuple[int, int]]):
    potential = 0
    for path in paths:
        potential += (1 / 2) ** (len(path.difference(moves)))
    return potential


def compute_optimal_move(rows: int, cols: int,
                         red_moves: Set[Tuple[int, int]],
                         blue_moves: Set[Tuple[int, int]],
                         red_paths: List[Set[Tuple[int, int]]],
                         blue_paths: List[Set[Tuple[int, int]]],
                         turn: bool):
    '''
    Compute the optimal next move according to the Erdos-Selfridge
    potential strategy. Return the next move and the Erdos-Selfridge
    potential that will result from playing it.

    rows: The number of rows in the grid
    cols: The number of columns in the grid
    red_moves: The cells already occupied by red
    blue_moves: The cells already occupied by blue
    paths: The opposing player's remaining possible winning paths
    turn: Whose turn it is
    '''

    if turn == RED:
        current_player_moves = red_moves
        current_player_paths = red_paths
        opposing_player_moves = blue_moves
        opposing_player_paths = blue_paths
    else:  # turn == BLUE
        current_player_moves = blue_moves
        current_player_paths = blue_paths
        opposing_player_moves = red_moves
        opposing_player_paths = red_paths

    # initialize variables
    open_tiles = get_open_tiles(rows, cols, red_moves, blue_moves)
    next_move = open_tiles[0]
    next_move_potential = 0
    opposing_player_moves.add(next_move)
    for path in opposing_player_paths:
        next_move_potential += (1/2) ** (len(path.difference(opposing_player_moves)))
    opposing_player_moves.remove(next_move)

    # find a move that minimizes the potential function
    for move in open_tiles[1:]:
        temp_potential = 0
        opposing_player_moves.add(move)
        for path in opposing_player_paths:
            temp_potential += (1/2)**(len(path.difference(opposing_player_moves)))
        opposing_player_moves.remove(move)
        if temp_potential > next_move_potential:
            next_move = move
            next_move_potential = temp_potential

    # find the new max value for the potential function after the opposing
    # player's next move
    current_player_moves.add(next_move)
    open_tiles.remove(next_move)
    new_opposing_paths = [p for p in opposing_player_paths if next_move not in p]
    #print("new opposing paths: " + str(new_opposing_paths))
    final_move = open_tiles[0]
    final_move_potential = 0

    for move in open_tiles:
        #print("for move " + str(move) + ": ")
        temp_potential = 0
        opposing_player_moves.add(move)
        for path in new_opposing_paths:
            amt = (1/2)**(len(path.difference(opposing_player_moves)))
            #print("potential of path " + str(path) + " = " + str(amt))
            temp_potential += amt
        opposing_player_moves.remove(move)
        if temp_potential > final_move_potential:
            final_move = move
            final_move_potential = temp_potential

    current_player_moves.remove(next_move)

    return next_move, final_move_potential


if __name__ == "__main__":
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
    cell_to_avoid = []
    if args.cell_to_avoid:
        x, y = (int(c.strip("(), []")) for c in args.cell_to_avoid.split(','))
        if 0 <= x < cols and 0 <= y < rows:
            cell_to_avoid.append((x, y))
    interactive = args.interactive
    visual = args.visual

    all_lengths_red = {}
    lengths_avoiding_cell_red = {}
    all_lengths_blue = {}
    lengths_avoiding_cell_blue = {}

    if interactive:
        game_over = 0 # initialize game loop
        turn = RED # red goes first
        red_moves = set()
        blue_moves = set()

        # Compute sets of minimal winning paths for Red and Blue
        red_paths = compute_paths(rows, cols, [], RED, True)
        if rows == cols:
            blue_paths = red_paths.copy()  # saves time on large grids
            for i in range(0, len(blue_paths)):
                path = set()
                for tile in blue_paths[i]:
                    path.add((tile[1], tile[0]))
                blue_paths[i] = path
        else:
            blue_paths = compute_paths(cols, rows, [], BLUE, True)

        while not game_over:

            # print game state and get user input
            while True:
                if visual:
                    print_grid(rows, cols, red_moves, blue_moves, True)
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
                next_move, _ = compute_optimal_move(rows, cols,
                                                    red_moves, blue_moves,
                                                    blue_paths, turn)

            if turn == RED:
                red_moves.add(next_move)

                # check win condition
                for path in red_paths:
                    if path.issubset(red_moves):
                        game_over = True
                        endgame_message = "Red wins!"
                        if visual: # add color
                            endgame_message = "\033[0;31m" + endgame_message + "\033[0m"

                # remove minimal winning paths containing new Red
                # tile from Blue's path set
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
                            endgame_message = "\033[34m" + \
                                              endgame_message + \
                                              "\033[0m"

                # remove minimal winning paths containing new Blue
                # tile from Red's path set
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
            # (this means there's a bug somewhere)
            if not get_open_tiles(rows, cols, red_moves, blue_moves) and not game_over:
                game_over = True
                endgame_message = "It's a draw."

            turn = not turn  # end turn

        # print final game state and declare winner
        if visual:
            print_grid(rows, cols, red_moves, blue_moves, True)
        else:
            lst = sorted(all_lengths_red.items(), key=lambda x: (x[0]))
            print("\nlength distribution of minimal winning paths remaining (Red): ")
            print(lst)

            print("\nRed tiles: " + str(list(red_moves)))
            print("Blue tiles: " + str(list(blue_moves)) + "\n")
        print(endgame_message)

    else:
        compute_paths(rows, cols, cell_to_avoid, RED, True)
        print_summary(all_lengths_red, lengths_avoiding_cell_red)

    exit(0)



