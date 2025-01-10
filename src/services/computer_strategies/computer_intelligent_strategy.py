import copy
import math
import random

from src.services.board import Board
from src.constants import COMPUTER_SYMBOL, PLAYER_SYMBOL, POSITION, EMPTY_CELL_SYMBOL
from src.exceptions import GameOver, OutOfBoardError


class ComputerIntelligentStrategy(object):
    """
    Strategy that uses the minimax algorithm with alpha-beta pruning.
    """
    def __init__(self, board: Board):
        self.__board = board
        self.__target_depth = 5

        self.__max_player = COMPUTER_SYMBOL
        self.__min_player = PLAYER_SYMBOL

    def get_move(self):
        move = self.__find_best_move()

        piece_position = POSITION(move["row"], move["column"])
        move_position = move["move_position"]

        return piece_position, move_position

    def __find_best_move(self):
        """
        Find the best move from all the possible moves of the computer using the minimax algorithm.
        :return: best move found
        """
        max_player_moves = self.__get_moves_of_player(self.__board, self.__max_player)

        best_evaluation = -math.inf
        best_move = None

        for move in max_player_moves:
            board_copy = copy.deepcopy(self.__board)
            board_copy.move(POSITION(move["row"], move["column"]), move["move_position"], self.__max_player)

            try:
                board_copy.is_board_won(self.__max_player)
            except GameOver:
                return move

            current_evaluation, _ = self.__minimax_algorithm(board_copy, self.__target_depth, -math.inf, math.inf, False)

            if current_evaluation == best_evaluation and best_move != None:
                current_board_evaluation = self.__evaluation_value(board_copy)

                board_copy_best_move_simulation = copy.deepcopy(self.__board)
                board_copy_best_move_simulation.move(POSITION(best_move["row"], best_move["column"]), best_move["move_position"], self.__max_player)
                best_move_board_evaluation = self.__evaluation_value(board_copy_best_move_simulation)

                if current_board_evaluation > best_move_board_evaluation:
                    best_evaluation = current_evaluation
                    best_move = move

            elif current_evaluation >= best_evaluation:
                best_evaluation = current_evaluation
                best_move = move

        return best_move

    def __minimax_algorithm(self, board: Board, depth, alpha, beta, maximize_player):
        """
        Minimax algorithm using alpha-beta pruning.
        - recursive algorithm that finds in its search tree the best move based on the values associated to the leaves (reached the target depth or is a terminal node)
        - if the computer wins the node is associated with value infinity
        - if the player wins the node is associated with value -infinity
        - else the node is associated with the value of an evaluation -- based on the pieces and their positions on current board

        - maximizing player (computer) tries to maximize its own gain <=> minimize its loss
        - minimizing player (human player) tries to minimize the opponents gain <=> maximize its own gain

        - alpha-beta pruning = search algorithm that decreases the number of nodes that are evaluated by the minimax algorithm

        [more info at https://en.wikipedia.org/wiki/Minimax]

        :param board: current board
        :param depth: current depth in the search tree
        :param alpha: minimum score that the maximizing player is assured of
        :param beta: maximum score that the minimizing player is assured of
        :param maximize_player: True if it's the computer's turn, False if it's the human player's turn
        :return: value of the evaluated current board and the best move found
        """
        try:
            board.is_board_won(self.__max_player)
        except GameOver:
            return math.inf, None

        try:
            board.is_board_won(self.__min_player)
        except GameOver:
            return -math.inf, None

        if depth == 0:
            return self.__evaluation_value(board), None

        if maximize_player == True:
            value = -math.inf

            player_moves = self.__get_moves_of_player(board, self.__max_player)

            best_move = None
            if len(player_moves) != 0:
                best_move = random.choice(player_moves)

            for move in player_moves:
                board_copy = copy.deepcopy(board)
                board_copy.move(POSITION(move["row"], move["column"]), move["move_position"], self.__max_player)

                new_value, _ = self.__minimax_algorithm(board_copy, depth - 1, alpha, beta, False)

                if new_value > value:
                    value = new_value
                    best_move = move

                alpha = max(alpha, value)

                if alpha >= beta:
                    break # beta cut-off

            return value, best_move

        elif maximize_player == False:
            value = math.inf

            player_moves = self.__get_moves_of_player(board, self.__min_player)

            best_move = None
            if len(player_moves) != 0:
                best_move = random.choice(player_moves)

            for move in player_moves:
                board_copy = copy.deepcopy(board)
                board_copy.move(POSITION(move["row"], move["column"]), move["move_position"], self.__min_player)

                new_value, _ = self.__minimax_algorithm(board_copy, depth - 1, alpha, beta, True)

                if new_value < value:
                    value = new_value
                    best_move = move

                beta = min(beta, value)
                if beta <= alpha:
                    break # alpha cut-off

            return value, best_move

    def __evaluation_value(self, board):
        """
        Evaluate the board -- associate a value to it based on how well it behaves for the maximizing player
        :param board: the board to evaluate
        :return: associated value
        """
        number_pieces = {self.__min_player: 0, self.__max_player: 0}
        number_capturing_moves = {self.__min_player: 0, self.__max_player: 0}

        for row in range(board.rows):
            for column in range(board.columns):
                cell_symbol = board.get_board_symbol(row, column)
                if cell_symbol != EMPTY_CELL_SYMBOL:
                    number_pieces[cell_symbol] += 1

                    active_piece = POSITION(row, column)
                    adjacent_piece_cells = self.__adjacent_symbol_cells(board, active_piece, cell_symbol)

                    for adjacent_piece in adjacent_piece_cells:
                        opponent_piece = self.__check_can_capture_opponent_piece(board, active_piece, adjacent_piece, board.get_opponent_symbol(cell_symbol))
                        if opponent_piece != None:
                            number_capturing_moves[cell_symbol] += 1

        number_pieces_cost = 10
        capture_move_cost = 5

        evaluation_value = number_pieces_cost * (number_pieces[self.__max_player] - number_pieces[self.__min_player]) + capture_move_cost * (number_capturing_moves[self.__max_player] - number_capturing_moves[self.__min_player])

        return evaluation_value

    def __get_moves_of_player(self, board: Board, player_symbol):
        """
        Find all available moves for a specific player and board.
        :param board: board to search on
        :param player_symbol: symbol of pieces to check
        :return: list with all the moves found
        """
        moves = []

        for row in range(board.rows):
            for column in range(board.columns):
                if board.get_board_symbol(row, column) == player_symbol:
                    piece_moves = self.__get_moves_of_piece(board, row, column, player_symbol)
                    for move in piece_moves:
                        moves.append({"row": row, "column": column, "move_position": move})

        return moves

    def __get_moves_of_piece(self, board: Board, piece_row, piece_column, piece_symbol):
        """
        Find all the available moves for a specific  piece and board.
        :param board: board to search on
        :param piece_row: row of piece to search for
        :param piece_column: column of piece to search for
        :param piece_symbol: symbol of piece to search for
        :return: list of all the moves found for the piece
        """
        moves = []
        piece_position = POSITION(piece_row, piece_column)

        # possible moves to empty adjacent cells
        moves.extend(self.__adjacent_symbol_cells(board, piece_position, EMPTY_CELL_SYMBOL))

        # possible capturing moves
        moves.extend(self.__find_capturing_moves(board, piece_position, piece_symbol))

        return moves

    def __adjacent_symbol_cells(self, board: Board, cell_position, symbol):
        """
        Find all the adjacent cells of a specific position with a specific symbol.
        :param board: board to search on
        :param cell_position: cell for which to find adjacent cells (x, y) = (row, column)
        :param symbol: the symbol to be found in the adjacent cells
        :return: list with the adjacent cells found
        """
        adjacent_cells_positions = []

        if (cell_position.x >= 0 and cell_position.x < board.rows - 1) and board.get_board_symbol(cell_position.x + 1, cell_position.y) == symbol:
            adjacent_cells_positions.append(POSITION(cell_position.x + 1, cell_position.y))
        if (cell_position.x > 0 and cell_position.x <= board.rows - 1) and board.get_board_symbol(cell_position.x - 1, cell_position.y) == symbol:
            adjacent_cells_positions.append(POSITION(cell_position.x - 1, cell_position.y))
        if (cell_position.y >= 0 and cell_position.y < board.columns - 1) and board.get_board_symbol(cell_position.x, cell_position.y + 1) == symbol:
            adjacent_cells_positions.append(POSITION(cell_position.x, cell_position.y + 1))
        if (cell_position.y > 0 and cell_position.y <= board.columns - 1) and board.get_board_symbol(cell_position.x, cell_position.y - 1) == symbol:
            adjacent_cells_positions.append(POSITION(cell_position.x, cell_position.y - 1))

        return adjacent_cells_positions

    def __find_capturing_moves(self, board: Board, piece, piece_symbol):
        """
        Find all the capturing moves available for a specific piece and board.
        :param board: board to search on
        :param piece: the piece for which to find capturing moves
        :param piece_symbol: the symbol of the piece to found moves for
        :return: list with all the capturing moves found for piece
        """
        capturing_positions = []
        adjacent_pieces_list = self.__adjacent_symbol_cells(board, piece, piece_symbol)

        for adjacent_piece in adjacent_pieces_list:
            opponent_captured_piece = self.__check_can_capture_opponent_piece(board, piece, adjacent_piece, board.get_opponent_symbol(piece_symbol))

            if opponent_captured_piece != None:
                capturing_positions.append(opponent_captured_piece)

        return capturing_positions

    def __check_can_capture_opponent_piece(self, board: Board, active_piece, jumped_over_piece, opponent_symbol):
        """
        Check if with the given pieces can be executed a capturing move.
        :param board: board to check on
        :param active_piece: position of piece that will jump
        :param jumped_over_piece: position of piece that will be jumped over
        :param opponent_symbol: symbol of piece that should be found to capture
        :return: position of the captured piece = destination cell if found, else None
        """
        if active_piece.x == jumped_over_piece.x:
            step = active_piece.y - jumped_over_piece.y

            opponent_y = active_piece.y - step * 2

            try:
                if board.get_board_symbol(active_piece.x, opponent_y) == opponent_symbol:
                    return POSITION(active_piece.x, opponent_y)
            except OutOfBoardError:
                return None

        elif active_piece.y == jumped_over_piece.y:
            step = active_piece.x - jumped_over_piece.x

            opponent_x = active_piece.x - step * 2

            try:
                if board.get_board_symbol(opponent_x, active_piece.y) == opponent_symbol:
                    return POSITION(opponent_x, active_piece.y)
            except OutOfBoardError:
                return None

        return None