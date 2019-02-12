import argparse, os, random


class Board:
    def __init__(self, n):
        self.size = n
        self.cells = [[' ' for _ in range(n)] for _ in range(n)]
        self.winning_lines = []
        
        # add winning rows
        for i in range(n):
            self.winning_lines.append([])
            for j in range(n):
                self.winning_lines[-1].append((i, j))
                
        # add winning columns
        for i in range(n):
            self.winning_lines.append([])
            for j in range(n):
                self.winning_lines[-1].append((j, i))
                
        # add winning diagonal lines
        self.winning_lines.append([])
        for i in range(n):
            self.winning_lines[-1].append((i, i))
        self.winning_lines.append([])
        for i in range(n):
            self.winning_lines[-1].append(((n-1)-i, i))

    def __str__(self):
        result = ''
        for i in range(self.size):
            # print top part of row
            line = '  '
            for _ in range(self.size):
                line += '+---'
            line += '+\n'
            result += line

            # print middle section of row
            line = str(self.size - 1 - i) + ' '
            for j in range(self.size):
                line += '| ' + self.cells[i][j] + ' '
            line += '|\n'
            result += line

        # print bottom line of bottom row with labels
        line = '  '
        labels = '    '
        for i in range(self.size):
            line += '+---'
            labels += str(i) + '   '
        line += '+\n'
        result += line + labels

        return result

    def get_open_cells(self):
        open_cells = []
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j] == ' ':
                    open_cells.append((i, j))
        return open_cells

    def compute_danger(self):
        # for simplicity, we only compute player x danger
        # = sum of (1/2)^(# of open cells remaining
        # in line that contains no o's)
        danger = 0
        for line in self.winning_lines:
            if 'O' not in line:
                danger += (1/2)**(len(line) - line.count('X'))
        return danger

    def get_optimal_move(self):
        # maximize the value we subtract from the "danger" function
        open_cells = self.get_open_cells()
        best_move = open_cells[0]
        best_move_val = 0

        for pos in open_cells:
            val = 0
            for line in self.winning_lines:
                if pos in line and 'O' not in line:
                    val += (1/2)**(len(line) - line.count('X'))
            if val > best_move_val:
                best_move = pos
                best_move_val = val

        return best_move

    def add_move(self, position, symbol):
        # in all lines, replace position with symbol
        for i in range(len(self.winning_lines)):
            for j in range(len(self.winning_lines[i])):
                if self.winning_lines[i][j] == position:
                    self.winning_lines[i][j] = symbol

        # remove winning lines that contain both symbols
        temp = list(filter(lambda lst: not('X' in lst and 'O' in lst), self.winning_lines))
        self.winning_lines = temp

        # add move to board
        self.cells[position[0]][position[1]] = symbol

    def check_for_win(self):
        if len(self.winning_lines) == 0:
            return True, 'No one'

        for line in self.winning_lines:
            if line.count('X') == len(line):
                return True, 'Player X'
            elif line.count('O') == len(line):
                return True, 'Player O'
        return False, None


class Player:
    def __init__(self, symbol, board):
        self.symbol = symbol
        self.board = board

    def add_move(self, position):
        self.board.add_move(position, self.symbol)

    def choose_move(self):
        while True:
            try:
                pos = input('Please enter x,y coordinates: ').split(',')
                pos = convert_to_working(tuple(int(c.strip("()[] ")) for c in pos), self.board)
                if pos in self.board.get_open_cells():
                    self.board.add_move(pos, self.symbol)
                    break
                else:
                    print('Cell not available.')
            except:
                print('Cannot read input. Please try again.')

    def random_move(self):
        open_cells = self.board.get_open_cells()
        random_index = random.randint(0, len(open_cells)-1)
        position = open_cells[random_index]
        self.board.add_move(position, self.symbol)


def convert_to_display(coordinates, board):
    x = coordinates[1]
    y = (board.size - 1) - coordinates[0]
    return (x, y)


def convert_to_working(coordinates, board):
    x = (board.size - 1) - coordinates[1]
    y = coordinates[0]
    return (x, y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('size', type=int, help='size of board (height/width')
    args = parser.parse_args()
    size = args.size

    board = Board(size)
    player_x = Player('X', board)
    player_o = Player('O', board)
    game_over = False
    winner = None

    while True:
        os.system('clear') # clear screen before printing updated grid
        print(board)
        print('Player X, choose an option:')
        opt = input('(1) Enter a move\n(2) Random move\n(x) Exit\n').strip()
        if opt == '1':
            player_x.choose_move()
        elif opt == '2':
            player_x.random_move()
        elif opt == 'x':
            exit(0)

        game_over, winner = board.check_for_win()
        if game_over:
            break

        potential = board.compute_danger()
        optimal_move = board.get_optimal_move()
        
        os.system('clear') # clear screen before printing updated grid
        print(board)
        print('Erdos-Selfridge potential: ' + str(potential))
        print('Optimal move: ' + str(convert_to_display(optimal_move, board)) + '\n')

        print('Player O, choose an option:')
        opt = input('(1) Enter a move\n(2) Random move\n(3) Potential strategy\n(x) Exit\n').strip()
        if opt == '1':
            player_o.choose_move()
        elif opt == '2':
            player_o.random_move()
        elif opt == '3':
            player_o.add_move(optimal_move)
        elif opt == 'x':
            exit(0)

        game_over, winner = board.check_for_win()
        if game_over:
            break

    os.system('clear') # clear screen before printing updated grid
    print(board)
    print('Game over. ' + str(winner) + ' wins!')

