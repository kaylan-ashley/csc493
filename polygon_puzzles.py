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
                [(0, 0), (1, 2), (3, 5)]],
           18: [7, 7,
                [(1, 4), (3, 2), (3, 3), (5, 5)],
                [(0, 5), (4, 5), (6, 0)]],
           19: [5, 5,
                [(0, 0), (0, 1), (0, 2), (4, 1), (4, 4)],
                [(1, 0), (1, 4), (2, 0), (2, 2), (2, 4)]],
           20: [6, 6,
                [(0, 5), (3, 3), (5, 1)],
                [(1, 3), (3, 1)]],
           21: [6, 6,
                [(0, 0), (1, 2), (2, 1), (3, 4), (5, 5)],
                [(2, 0), (2, 2), (2, 4), (4, 1)]],
           22: [7, 7,
                [(3, 3), (4, 4), (5, 5)],
                [(2, 5), (3, 1)]],
           23: [7, 7,
                [(0, 1), (0, 2), (0, 3), (1, 1), (2, 2), (3, 4), (4, 1), (4, 3), (5, 2), (6, 3), (6, 4), (6, 6)],
                [(0, 0), (0, 4), (1, 3), (2, 1), (2, 3), (2, 5), (3, 0), (3, 3), (4, 2), (5, 3), (6, 2)]],
           24: [6, 6,
                [(0, 1), (1, 2), (1, 3), (2, 1), (3, 3), (5, 3)],
                [(0, 4), (2, 3), (2, 5), (4, 3), (4, 5)]],
           25: [6, 6,
                [(0, 0), (0, 1), (0, 2)],
                [(1, 1), (2, 0), (3, 2), (4, 3)]],
           26: [6, 6,
                [(0, 1), (1, 3), (2, 4), (3, 3), (4, 0), (4, 3), (5, 1)],
                [(1, 0), (2, 2), (2, 3), (2, 5), (3, 0), (3, 5)]],
           27: [7, 7,
                [(0, 2), (2, 1), (2, 4), (5, 3), (6, 5)],
                [(2, 3), (3, 3), (4, 1), (4, 3)]],
           28: [6, 6,
                [(0, 4), (1, 1), (1, 2), (4, 2)],
                [(0, 0), (2, 2), (2, 3), (5, 4)]],
           29: [6, 6,
                [(0, 2), (0, 4), (1, 0)],
                [(0, 0), (2, 2)]],
           30: [6, 6,
                [(1, 1), (4, 4)],
                [(1, 2), (2, 5)]],
           31: [7, 7,
                [(0, 0), (1, 3), (2, 2), (4, 1), (4, 3), (4, 5), (5, 6)],
                [(2, 3), (3, 2), (4, 2), (4, 4)]],
           32: [7, 7,
                [(2, 3), (3, 4), (5, 2)],
                [(1, 2), (3, 2), (5, 4)]],
           33: [7, 7,
                [(0, 0), (2, 3), (2, 4), (3, 2), (3, 6), (4, 4)],
                [(2, 0), (2, 2), (3, 3), (3, 4)]],
           34: [7, 7,
                [(1, 1), (1, 2), (3, 3), (4, 5)],
                [(2, 1), (3, 4), (4, 1)]],
           35: [7, 7,
                [(1, 3), (2, 2), (5, 5), (6, 4)],
                [(3, 4), (4, 0), (4, 3)]],
           36: [7, 7,
                [(1, 2), (2, 3), (4, 2), (6, 2), (6, 4), (6, 5)],
                [(3, 1), (3, 4), (4, 3), (4, 5)]],
           37: [6, 6,
                [(0, 2), (0, 3), (1, 1), (3, 3), (5, 3)],
                [(1, 2), (1, 3), (2, 1), (4, 3), (5, 0)]],
           38: [7, 7,
                [(0, 3), (0, 4), (1, 3), (3, 2), (3, 4), (3, 6), (6, 3), (6, 4)],
                [(1, 4), (1, 6), (2, 2), (2, 3), (4, 3), (5, 3), (5, 4), (6, 0)]],
           39: [7, 7,
                [(1, 3), (2, 4), (3, 1), (3, 2), (5, 4)],
                [(2, 6), (4, 1), (4, 5)]],
           40: [7, 7,
                [(0, 3), (2, 3), (4, 4), (5, 2)],
                [(1, 2), (2, 2), (4, 2)]],
           41: [7, 7,
                [(0, 2), (0, 3), (3, 3), (3, 4), (4, 3), (5, 6), (6, 5)],
                [(0, 0), (1, 5), (2, 3), (3, 2), (4, 4), (4, 5), (0, 0)]],
           42: [7, 7,
                [(0, 1), (0, 2), (1, 2), (1, 4), (2, 1), (3, 3), (4, 3), (5, 5)],
                [(1, 1), (1, 6), (2, 3), (2, 4), (4, 1), (4, 5), (6, 6)]],
           # puzzles 43 and onwards are non-canonical (generated by me)
           43: [4, 4,
                [(1, 3), (2, 3), (3, 3)],
                [(1, 2), (2, 0)]]
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

red_paths = compute_paths(rows, cols, blue_cells, RED, False)
blue_paths = compute_paths(rows, cols, red_cells, BLUE, False)
print("red paths: " + str(red_paths))
print("blue paths: " + str(blue_paths))

print_grid(rows, cols, red_cells, blue_cells, False)

# Compute optimal next move for the Blue player, plus the Erdos-Selfridge
# potential from Blue's perspective
next_move, potential = compute_optimal_move(rows, cols,
                                            red_moves, blue_moves,
                                            red_paths, blue_paths,
                                            BLUE)
print("Optimal next move for puzzle " + str(n) + ": " + str(next_move))
print("Erdos-Selfridge potential for puzzle " + str(n) + " = " + str(potential))

if finish_game:
    game_over = False
    while not game_over:
        print_grid(rows, cols, red_moves, blue_moves, False)

        # Blue uses potential strategy
        next_move, potential = compute_optimal_move(rows, cols,
                                                    red_moves, blue_moves,
                                                    red_paths, blue_paths,
                                                    BLUE)
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
        else:  # player == BLUE
            print('Blue\'s turn')
        red_potential = compute_potential(red_paths, red_moves)
        blue_potential = compute_potential(blue_paths, blue_moves)
        print('Red potential = ' + str(red_potential))
        print('Blue potential = ' + str(blue_potential))

        # Compute the optimal next move for the Blue player,
        # plus the Erdos-Selfridge potential from Blue's perspective
        if player == RED:
            next_move, potential = compute_optimal_move(rows, cols,
                                                        red_moves,
                                                        blue_moves,
                                                        red_paths,
                                                        blue_paths,
                                                        RED)

        elif player == BLUE:
            # Compute a move that minimizes the potential Red can reach
            # after selecting their next move.
            next_move, potential = compute_optimal_move(rows, cols,
                                                        red_moves,
                                                        blue_moves,
                                                        red_paths,
                                                        blue_paths,
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
    exit(0)


