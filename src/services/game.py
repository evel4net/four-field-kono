from src.services.board import Board
from src.constants import PLAYER_SYMBOL, COMPUTER_SYMBOL, POSITION

class Game(object):
    def __init__(self, board: Board, computer_strategy):
        self.__board = board
        self.__computer_strategy = computer_strategy

    def player_move(self, piece_row, piece_column, move_row, move_column):
        piece_position = POSITION(piece_row, piece_column)
        move_position = POSITION(move_row, move_column)

        self.__board.move(piece_position, move_position, PLAYER_SYMBOL)

    def computer_move(self):
        piece_position, move_position = self.__computer_strategy.get_move()

        self.__board.move(piece_position, move_position, COMPUTER_SYMBOL)

        return piece_position, move_position