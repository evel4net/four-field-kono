from src.services.board import Board
from src.constants import COMPUTER_SYMBOL, POSITION, EMPTY_CELL_SYMBOL, PLAYER_SYMBOL
from src.exceptions import OutOfBoardError


class ComputerCapturingStrategy(object):
    """
    Strategy that tries to find the first valid capturing move.
    If no capturing move found, tries to find the first piece that could be moved in an adjacent empty cell and be part of a capturing move in the computer's next turn.
    If neither such move found, executes the first valid movement in adjacent empty cell found.
    """
    def __init__(self, board: Board):
        self.__board = board

    def get_move(self):
        # find first valid capturing move
        for row in range(self.__board.rows):
            for column in range(self.__board.columns):
                if self.__board.get_board_symbol(row, column) == COMPUTER_SYMBOL:
                    active_piece = POSITION(row, column)

                    move_position = self.__find_capturing_move(active_piece)
                    if move_position != None:
                        return active_piece, move_position

        # find first empty adjacent cell that can result in capturing move (in next turn)
        for row in range(self.__board.rows):
            for column in range(self.__board.columns):
                if self.__board.get_board_symbol(row, column) == COMPUTER_SYMBOL:
                    active_piece = POSITION(row, column)
                    empty_adjacent_cells = self.__adjacent_symbol_cells(active_piece, EMPTY_CELL_SYMBOL)

                    for cell in empty_adjacent_cells:
                        possible_capturing_move_position = self.__find_capturing_move(cell)

                        if possible_capturing_move_position != None:
                            return active_piece, cell

        # find first valid movement to adjacent empty cell
        for row in range(self.__board.rows):
            for column in range(self.__board.columns):
                 if self.__board.get_board_symbol(row, column) == COMPUTER_SYMBOL:
                    active_piece = POSITION(row, column)
                    empty_adjacent_cells = self.__adjacent_symbol_cells(active_piece, EMPTY_CELL_SYMBOL)

                    if len(empty_adjacent_cells) != 0:
                        return active_piece, empty_adjacent_cells[0]

    def __find_capturing_move(self, piece):
        """
        Find the first capturing move for a specific piece.
        :param piece: the piece for which to find capturing moves
        :return: the position of the destination cell if found, else None
        """
        adjacent_pieces_list = self.__adjacent_symbol_cells(piece, COMPUTER_SYMBOL)

        for adjacent_piece in adjacent_pieces_list:
            opponent_captured_piece = self.__check_can_capture_opponent_piece(piece, adjacent_piece, PLAYER_SYMBOL)

            if opponent_captured_piece != None:
                return opponent_captured_piece

        return None

    def __adjacent_symbol_cells(self, cell_position, symbol):
        """
        Find all the adjacent cells of a specific position with a specific symbol.
        :param cell_position: cell for which to find adjacent cells
        :param symbol: the symbol to be found in the adjacent cells
        :return: list with the adjacent cells found
        """
        adjacent_cells_positions = []

        if (cell_position.x >= 0 and cell_position.x < self.__board.rows - 1) and self.__board.get_board_symbol(cell_position.x + 1, cell_position.y) == symbol:
            adjacent_cells_positions.append(POSITION(cell_position.x + 1, cell_position.y))
        if (cell_position.x > 0 and cell_position.x <= self.__board.rows - 1) and self.__board.get_board_symbol(cell_position.x - 1, cell_position.y) == symbol:
            adjacent_cells_positions.append(POSITION(cell_position.x - 1, cell_position.y))
        if (cell_position.y >= 0 and cell_position.y < self.__board.columns - 1) and self.__board.get_board_symbol(cell_position.x, cell_position.y + 1) == symbol:
            adjacent_cells_positions.append(POSITION(cell_position.x, cell_position.y + 1))
        if (cell_position.y > 0 and cell_position.y <= self.__board.columns - 1) and self.__board.get_board_symbol(cell_position.x, cell_position.y - 1) == symbol:
            adjacent_cells_positions.append(POSITION(cell_position.x, cell_position.y - 1))

        return adjacent_cells_positions

    def __check_can_capture_opponent_piece(self, active_piece, jumped_over_piece, opponent_symbol):
        """
        Check if with the given pieces can be executed a capturing move.
        :param active_piece: position of piece that will jump
        :param jumped_over_piece: position of piece that will be jumped over
        :param opponent_symbol: symbol of piece that should be found to capture
        :return: position of the captured piece = destination cell if found, else None
        """
        if active_piece.x == jumped_over_piece.x:
            step = active_piece.y - jumped_over_piece.y

            opponent_y = active_piece.y - step * 2

            try:
                if self.__board.get_board_symbol(active_piece.x, opponent_y) == opponent_symbol:
                    return POSITION(active_piece.x, opponent_y)
            except OutOfBoardError:
                return None

        elif active_piece.y == jumped_over_piece.y:
            step = active_piece.x - jumped_over_piece.x

            opponent_x = active_piece.x - step * 2

            try:
                if self.__board.get_board_symbol(opponent_x, active_piece.y) == opponent_symbol:
                    return POSITION(opponent_x, active_piece.y)
            except OutOfBoardError:
                return None