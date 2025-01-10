# Board: 4 x 4
#     player piece: 'O'
#     computer piece: 'X'
#
# Starting Board:
# *---*---*---*---*
# | X | X | X | X |
# *---*---*---*---*
# | X | X | X | X |
# *---*---*---*---*
# | O | O | O | O |
# *---*---*---*---*
# | O | O | O | O |
# *---*---*---*---*

# from texttable import Texttable

from src.constants import EMPTY_CELL_SYMBOL, ROWS, COLUMNS, COMPUTER_SYMBOL, PLAYER_SYMBOL, MAXIMUM_NUMBER_PIECES
from src.exceptions import OutOfBoardError, NotOrthogonalBoardMoveError, IncorrectBoardMoveError, GameOver


class Board(object):
    def __init__(self, rows = ROWS, columns = COLUMNS):
        self.__rows = rows
        self.__columns = columns
        self.__board = []
        self.__number_of_pieces = None

        self.load_start_board()

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    def load_start_board(self):
        """
        Populate the board with pieces to start a game.
        :return: None
        """
        self.__board.clear()
        self.__board = [[COMPUTER_SYMBOL for _ in range(self.__rows)] for _ in range(self.__columns // 2)]
        self.__board.extend([[PLAYER_SYMBOL for _ in range(self.__rows)] for _ in range(self.__columns - self.__columns // 2)])
        self.__number_of_pieces = {PLAYER_SYMBOL: MAXIMUM_NUMBER_PIECES, COMPUTER_SYMBOL: MAXIMUM_NUMBER_PIECES}

    def get_board_symbol(self, row: int, column: int):
        if not (0 <= row < self.__rows and 0 <= column < self.__columns):
            raise OutOfBoardError()

        return self.__board[row][column]

    def move(self, piece_position, move_position, symbol):
        """
        Move the corresponding player or computer piece to its new position -- capturing move or movement to adjacent empty cell
        :param piece_position: POSITION(current_piece_row, current_piece_column)
        :param move_position: POSITION(destination_cell_row, destination_cell_column)
        :param symbol: what piece is moved (PLAYER_SYMBOl or COMPUTER_SYMBOL)
        :return: None
        :raises OutOfBoardError, IncorrectBoardMoveError, NotOrthogonalBoardMoveError: if the piece position and/or destination position are not valid
        """

        if not (0 <= piece_position.x < self.__rows and 0 <= piece_position.y < self.__columns and 0 <= move_position.x < self.__rows and 0 <= move_position.y < self.__columns):
            raise OutOfBoardError()

        if self.__board[piece_position.x][piece_position.y] == EMPTY_CELL_SYMBOL:
            raise IncorrectBoardMoveError()

        if not self.__board[piece_position.x][piece_position.y] == symbol:
            raise IncorrectBoardMoveError()

        if piece_position.x == move_position.x:
            if abs(piece_position.y - move_position.y) == 1 and self.__board[move_position.x][move_position.y] == EMPTY_CELL_SYMBOL:
                self.__board[piece_position.x][piece_position.y] = EMPTY_CELL_SYMBOL
                self.__board[move_position.x][move_position.y] = symbol
            elif abs(piece_position.y - move_position.y) == 2 and self.__board[piece_position.x][(piece_position.y + move_position.y) // 2] == symbol and self.__board[move_position.x][move_position.y] == self.get_opponent_symbol(symbol):
                # capturing move
                self.__board[piece_position.x][piece_position.y] = EMPTY_CELL_SYMBOL
                self.__board[move_position.x][move_position.y] = symbol
                self.__number_of_pieces[self.get_opponent_symbol(symbol)] -= 1
            else:
                raise IncorrectBoardMoveError()

        elif piece_position.y == move_position.y:
            if abs(piece_position.x - move_position.x) == 1 and self.__board[move_position.x][move_position.y] == EMPTY_CELL_SYMBOL:
                self.__board[piece_position.x][piece_position.y] = EMPTY_CELL_SYMBOL
                self.__board[move_position.x][move_position.y] = symbol
            elif abs(piece_position.x - move_position.x) == 2 and self.__board[(piece_position.x + move_position.x) // 2][piece_position.y] == symbol and self.__board[move_position.x][move_position.y] == self.get_opponent_symbol(symbol):
                # capturing move
                self.__board[piece_position.x][piece_position.y] = EMPTY_CELL_SYMBOL
                self.__board[move_position.x][move_position.y] = symbol
                self.__number_of_pieces[self.get_opponent_symbol(symbol)] -= 1
            else:
                raise IncorrectBoardMoveError()

        else:
            # move is not orthogonally
            raise NotOrthogonalBoardMoveError()

    def is_board_won(self, symbol):
        """
        Raise a GameOver error if the board is won by the player with the specified symbol -- opponent has only one piece left or opponent is immobilized (cannot make any move).
        :param symbol: symbol of the player to check if board is won for
        :return: None
        :raise GameOver: is board is won by 'symbol'
        """

        if self.__number_of_pieces[self.get_opponent_symbol(symbol)] == 1:
            raise GameOver(symbol)

        # check if opponent is immobilized
        immobilized_pieces = 0
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_board_symbol(row, column) == self.get_opponent_symbol(symbol):
                    blocked_sides = 0
                    if (row >= 0 and row < self.__rows - 1) and self.get_board_symbol(row + 1, column) == symbol:
                        blocked_sides += 1

                    if (row > 0 and row <= self.__rows - 1) and self.get_board_symbol(row - 1, column) == symbol:
                        blocked_sides += 1

                    if (column >= 0 and column < self.__columns - 1) and self.get_board_symbol(row, column + 1) == symbol:
                        blocked_sides += 1

                    if (column > 0 and column <= self.__columns - 1) and self.get_board_symbol(row, column - 1) == symbol:
                        blocked_sides += 1

                    # check if piece is completely immobilized
                    if row == 0 or row == self.__rows - 1:
                        if (column == 0 or column == self.__columns - 1) and blocked_sides == 2:
                            immobilized_pieces += 1
                        elif blocked_sides == 3:
                            immobilized_pieces += 1
                    elif blocked_sides == 4:
                        immobilized_pieces += 1

        if immobilized_pieces == self.__number_of_pieces[self.get_opponent_symbol(symbol)]:
            raise GameOver(symbol)

    def get_opponent_symbol(self, symbol):
        if symbol == PLAYER_SYMBOL:
            return COMPUTER_SYMBOL
        else:
            return PLAYER_SYMBOL

    def check_valid_move(self, piece_position, move_position, symbol):
        """
        Check if the move can be executed -- move to adjacent piece or capturing move.
        :param piece_position: POSITION(current_piece_row, current_piece_column)
        :param move_position: POSITION(destination_cell_row, destination_cell_column)
        :param symbol: what piece is moved (PLAYER_SYMBOl or COMPUTER_SYMBOL)
        :return: True if the move is possible, else False
        """
        if not (0 <= piece_position.x < self.__rows or 0 <= piece_position.y < self.__columns or 0 <= move_position.x < self.__rows or 0 <= move_position.y < self.__columns):
            return False

        if self.__board[piece_position.x][piece_position.y] == EMPTY_CELL_SYMBOL:
            return False

        if not self.__board[piece_position.x][piece_position.y] == symbol:
            return False

        if piece_position.x == move_position.x:
            if abs(piece_position.y - move_position.y) == 1 and self.__board[move_position.x][move_position.y] == EMPTY_CELL_SYMBOL:
                return True
            elif abs(piece_position.y - move_position.y) == 2 and self.__board[piece_position.x][(piece_position.y + move_position.y) // 2] == symbol and self.__board[move_position.x][move_position.y] == self.get_opponent_symbol(symbol):
                return True

        elif piece_position.y == move_position.y:
            if abs(piece_position.x - move_position.x) == 1 and self.__board[move_position.x][move_position.y] == EMPTY_CELL_SYMBOL:
                return True
            elif abs(piece_position.x - move_position.x) == 2 and self.__board[(piece_position.x + move_position.x) // 2][piece_position.y] == symbol and self.__board[move_position.x][move_position.y] == self.get_opponent_symbol(symbol):
                return True

        else:
            return False

    # def __str__(self):
    #     table = Texttable()
    #     header = ["/"]
    #     for index in range(self.__columns):
    #         header.append(str(index))
    #     table.header(header)
    #
    #     for row in range(self.__rows):
    #         table_row = [str(row)]
    #         table_row.extend(self.__board[row])
    #         table.add_row(table_row)
    #
    #     return table.draw()