import random

from src.services.board import Board
from src.constants import POSITION, COMPUTER_SYMBOL


class ComputerRandomStrategy(object):
    """
    Strategy that chooses a random valid move for the computer.
    """
    def __init__(self, board: Board):
        self.__board = board

    def get_move(self):
        """
        Generates random positions for the piece to move and the destination cell until it finds a valid move for the pair of possitions
        :return: corresponding positions for the random valid move found
        """
        while True:
            piece_row = random.randint(0, self.__board.rows - 1)
            piece_column = random.randint(0,self.__board.columns - 1)

            move_row = random.randint(0,self.__board.rows - 1)
            move_column = random.randint(0,self.__board.columns - 1)

            piece_position = POSITION(piece_row, piece_column)
            move_position = POSITION(move_row, move_column)

            if self.__board.check_valid_move(piece_position, move_position, COMPUTER_SYMBOL):
                return piece_position, move_position
