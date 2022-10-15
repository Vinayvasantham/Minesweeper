import random
import re
# first create a board to represent the minesweeper game
# this is so that we can say "create a new board object" or
# "dig here" or "render this game for this object"


class Board:
    def __init__(self, board_size, num_bombs):
        self.board_size = board_size
        self.num_bombs = num_bombs

        # let's create the board
        # helper function
        self.board = self.make_new_board()   # plant the bombs
        self.assign_values_to_board()

        # initialize a set to know the uncovered positions
        # we'll save (row,col) positions in the set
        self.dug = set()  # if we dig at position (0, 0) then self.dug = ({0, 0})

    def make_new_board(self):
        # construct a new board based on the dimensions and num_bombs
        # we should construct the lists in list here (or whatever representation you prefer ,
        # but since we have a 2D board, list of lists is most natural)

        # generate a new board

        board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        # this creates an array like this
        # [[None, None, None],
        # [None, None, None],
        # [None, None, None]]
        # we can see how it will represent a board

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.board_size ** 2 - 1)  # return a random integer from a given range
            row = loc // self.board_size   #
            col = loc % self.board_size

            if board[row][col] == "*":
                # we have to tell there is already bomb planted
                continue

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign the numbers (0-8) for the neighbouring spaces, which
        # represents the how? many neighbouring bombs are there. we can precompute these it will save us some effort
        # checking what's around the board later on :)
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '*':
                    # if it's  already a bomb we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)

    def get_num_neighbouring_bombs(self, row, col):
        # let's iterate through the neighbouring positions of and sum number of bombs
        # top_left : (row-1, col-1)
        # top_middle : (row-1, col)
        # top_right : (row-1, col+1)
        # left : (row, col-1)
        # right : (row, col+1)
        # bottom_left : (row+1, col-1)
        # bottom_middle : (row+1, col)
        # bottom_right : (row+1, col+1)

        # make sure not to go out of bounds!

        num_neighbouring_bombs = 0
        for r in range(max(0, row-1), min(self.board_size-1, row + 1) + 1):
            for c in range(max(0, col-1), min(self.board_size-1, col + 1) + 1):
                if r == row and c == col:
                    # our original location don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs += 1

        return num_neighbouring_bombs

    # here we will plant the bombs in the board


    def dig(self, row, col):
        # dig at that location
        # if our location is not a bomb return True or else False

        self.dug.add((row, col))
        # dug scenarios:
        # dig location is not a bomb -> dig start
        # dig at location with neighbouring bombs -> finish digs
        # dig at location with no neighbouring bombs -> recursively digs until end

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row - 1), min(self.board_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.board_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue  # don't dig where already you dug
                self.dig(r, c)
        # if our initial dig is not a bomb , we should  not hit a bomb here
        return True

    def __str__(self):

        visible_board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.board_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.board_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % col)
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % col)
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.board_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


def play(board_size=10, num_bombs=10):
    # Step-1 : Create the board and plant the
    safe = True
    board = Board(board_size, num_bombs)
    # Step-2 : show the board to player and ask where to dig

    # step-3 : if location is a bomb show game is over
    # step-4 : if location is not a bomb dig recursively until end of mines
    # step-5 : if the boxes is completed Victory!
    while len(board.dug) < board.board_size**2 - num_bombs:
        print(board)

        user_input = re.split(',(\\s)*', input('where you want to dig? input as row,col: '))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.board_size or col < 0 or col >= board_size:
            print('Invalid Input. Try again! ')
            continue

        safe = board.dig(row, col)

        if not safe:
            break

    if safe:
        print("CONGRATULATIONS YOU'RE VICTORIOUS")
    else:
        print("You have dug the bomb.you lost.")
        board.dug = [(r, c) for r in range(board.board_size) for c in range(board.board_size)]
        print(board)


if __name__ == '__main__':
    play()