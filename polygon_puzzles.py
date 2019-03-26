import argparse
from hex import *

# Format: puzzle_number: [rows, cols,
#                         [red cells],
#                         [blue cells]]
puzzles = {1: [11, 11,
               [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7),
                (3, 8), (3, 9), (7, 4), (7, 5)],
               [(3, 3), (7, 2), (8, 7)]],
           2: [5, 5,
               [(1, 2), (3, 3), (4, 2)],
               [(2, 0), (2, 2), (4, 4)]],
           3: [6, 6,
               [(0, 2), (2, 1), (2, 3), (3, 1)],
               [(1, 2), (4, 1), (4, 5)]],
           4: [3, 3,
               [(0, 1), (1, 0)],
               [(0, 2)]],
           5: [6, 6,
               [(2, 3), (3, 1), (5, 3)],
               [(1, 1), (1, 5)]],
           6: [4, 4,
               [(0, 0), (3, 3)],
               [(2, 2)]],
           7: [4, 4,
               [(0, 0)],
               [(0, 3)]],
           8: [5, 5,
               [(0, 0), (0, 1), (1, 3), (3, 3)],
               [(1, 0), (1, 4), (2, 0), (2, 4), (3, 1)]],
           9: [4, 4,
               [(0, 0), (0, 3), (3, 2)],
               [(1, 0), (3, 1)]],
           10: [5, 5,
                [(0, 1), (1, 2), (4, 2), (4, 4)],
                [(2, 3), (3, 2)]],
           11: [5, 5,
                [(1, 2), (2, 1), (2, 3), (4, 1)],
                [(2, 0), (3, 3), (4, 0)]],
           12: [4, 4,
                [(1, 0), (3, 3)],
                [(0, 1)]],
           13: [5, 5,
                [(1, 1), (1, 3), (4, 1), (4, 2)],
                [(1, 0), (1, 4), (2, 0), (3, 1)]],
           14: [5, 5,
                [(0, 0), (3, 1), (3, 3)],
                [(2, 0), (3, 0), (3, 2)]],
           15: [5, 5,
                [(0, 0), (1, 2), (3, 2)],
                [(2, 2), (3, 4), (4, 1)]],
           16: [5, 5,
                [(0, 3), (1, 1), (1, 2)],
                [(0, 0), (0, 2), (2, 2)]],
           17: [6, 6,
                [(3, 3), (5, 4), (5, 5)],
                [(0, 0), (1, 2), (3, 5)]]
           }


parser = argparse.ArgumentParser()
parser.add_argument('puzzle_number', type=int, help='the puzzle ID number')
parser.add_argument('--finish', action='store_true', default=False,
                    help='finish game automatically using potential \\'
                         ' and random strategies')
parser.add_argument('--play', action='store_true', default=False,
                    help='play the rest of the game manually')
args = parser.parse_args()
n = args.puzzle_number
finish_game = args.finish
play_game = args.play

rows = puzzles[n][0]
cols = puzzles[n][1]
red_cells = puzzles[n][2]
blue_cells = puzzles[n][3]
red_moves = set(red_cells)
blue_moves = set(blue_cells)

# all_blue_paths = compute_paths(rows, cols, [(4, 1)], BLUE, False)
# print("Subset of blue paths avoiding (4, 1)")
# for path in all_blue_paths:
#     if len(path) == 8 and {(0, 4), (1, 4), (2, 4)}.issubset(path):
#         print(path)

red_paths = compute_paths(rows, cols, blue_cells, RED, False)
blue_paths = compute_paths(rows, cols, red_cells, BLUE, False)

print_grid(rows, cols, red_cells, blue_cells, False)

# Compute the optimal next move for the Blue player, plus the Erdos-Selfridge
# potential from Blue's perspective
next_move, potential = compute_optimal_move(rows, cols, red_moves,
                                            blue_moves, red_paths, BLUE)
print("Optimal next move: " + str(next_move))
print("Erdos-Selfridge potential = " + str(potential))

if finish_game:
    game_over = False
    while not game_over:
        print_grid(rows, cols, red_moves, blue_moves, False)

        # Blue uses potential strategy
        next_move, potential = compute_optimal_move(rows, cols,
                                                    red_moves, blue_moves,
                                                    red_paths, BLUE)
        blue_moves.add(next_move)
        for path in blue_paths: # check win condition
            if path.issubset(blue_moves):
                game_over = True
                break

        if not game_over:
            print_grid(rows, cols, red_moves, blue_moves, False)
            # remove Red paths containing last Blue move
            new_red_paths = [p for p in red_paths if next_move not in p]
            red_paths = new_red_paths

            # Red plays randomly
            open_tiles = get_open_tiles(rows, cols, red_moves, blue_moves)
            next_move = open_tiles[random.randint(0, len(open_tiles)-1)]
            red_moves.add(next_move)
            for path in red_paths: # check win condition
                if path.issubset(red_moves):
                    game_over = True
                    break
            # remove Blue paths containing last Red move
            new_blue_paths = [p for p in blue_paths if next_move not in p]
            blue_paths = new_blue_paths

    print_grid(rows, cols, red_moves, blue_moves, False)
    exit(0)

if play_game:
    player = BLUE
    game_over = False
    while not game_over:
        print_grid(rows, cols, red_moves, blue_moves, False)
        if player == RED:
            print('Red\'s turn')
            # print('Red paths: ')
            # for path in red_paths:
            #     print(path)
        else:  # player == BLUE
            print('Blue\'s turn')
            # print('Blue paths: ')
            # for path in blue_paths:
            #     print(path)
        red_potential = compute_potential(red_paths, red_moves)
        blue_potential = compute_potential(blue_paths, blue_moves)
        print('Red potential = ' + str(red_potential))
        print('Blue potential = ' + str(blue_potential))

        # Compute the optimal next move for the Blue player,
        # plus the Erdos-Selfridge potential from Blue's perspective
        if player == RED:
            # next_move, potential = compute_optimal_move(rows, cols,
            #                                             red_moves,
            #                                             blue_moves,
            #                                             red_paths,
            #                                             RED)

            # Compute a move that maximizes Red's potential
            open_tiles = get_open_tiles(rows, cols, red_moves, blue_moves)
            next_move = open_tiles[0]
            red_moves.add(next_move)
            potential = compute_potential(red_paths, red_moves)
            red_moves.remove(next_move)
            for tile in open_tiles:
                red_moves.add(tile)
                temp_potential = compute_potential(red_paths, red_moves)
                red_moves.remove(tile)
                if temp_potential > potential:
                    next_move = tile
                    potential = temp_potential

        elif player == BLUE:
            # Compute a move that minimizes the potential Red can reach
            # after selecting their next move.
            next_move, potential = compute_optimal_move(rows, cols,
                                                        red_moves,
                                                        blue_moves,
                                                        red_paths,
                                                        BLUE)
        print("Optimal next move: " + str(next_move))
        print("Erdos-Selfridge potential = " + str(potential))

        x, y = (int(c.strip("()[] ")) for c in
                input("Please enter x,y coordinates: ").split(','))
        next_move = (x, y)

        if player == RED:
            red_moves.add(next_move)

            # check win condition
            for path in red_paths:
                if path.issubset(red_moves):
                    game_over = True
                    print_grid(rows, cols, red_moves, blue_moves, False)
                    print("Red wins!")

            # remove minimal winning paths containing new Red
            # tile from Blue's path set
            new_blue_paths = [p for p in blue_paths if next_move not in p]
            blue_paths = new_blue_paths

        else:
            blue_moves.add(next_move)

            # check win condition
            for path in blue_paths:
                if path.issubset(blue_moves):
                    game_over = True
                    print_grid(rows, cols, red_moves, blue_moves, False)
                    print("Blue wins!")

            # remove minimal winning paths containing new Blue
            # tile from Red's path set
            new_red_paths = [p for p in red_paths if next_move not in p]
            red_paths = new_red_paths

        player = not player
        assert(not bool(red_moves.intersection(blue_moves)))
