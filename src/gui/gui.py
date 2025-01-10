import sys
import pygame
import random

from src.services.board import Board
from src.exceptions import GameOver, BoardError, GUIGoToTitleWindow
from src.services.game import Game
from src.gui.window_first_player import FirstPlayerWindow
from src.constants import (ROWS, COLUMNS, COMPUTER_SYMBOL, PLAYER_SYMBOL, EMPTY_CELL_SYMBOL, WIDTH, HEIGHT, FPS, PLAYER_PIECE_COLOR, COMPUTER_PIECE_COLOR, PADDING, CELL_SIZE,
                           GAME_TITLE, PLAY_BUTTON_TEXT, RULES_BUTTON_TEXT, WINNER_BANNER, LOSER_BANNER, BACKGROUND_SCROLL, BLACK, OPACITY_VALUE, HOVERING_SYMBOL, SYMBOLS_FONT)
from src.gui.window_levels import LevelsWindow
from src.gui.window_rules import RulesWindow
from src.gui.sprites import BoardDrawing, Piece
from src.gui.window_title import TitleWindow

class GUI(object):
    def __init__(self):
        self.__width = WIDTH
        self.__height = HEIGHT
        self.__window = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption(GAME_TITLE)

        pygame.display.set_icon(SYMBOLS_FONT.render(HOVERING_SYMBOL, 1, BLACK))

        self.__board = Board()
        self.__game = None
        self.__pieces = []
        self.__load_pieces()

        self.__board_drawing = BoardDrawing(self.__window)
        self.__levels_window = LevelsWindow(self.__window)
        self.__title_window = TitleWindow(self.__window)
        self.__rules_window = RulesWindow(self.__window)
        self.__first_player_window = FirstPlayerWindow(self.__window)

        self.__player_turn = random.choice([True, False])

    def __load_pieces(self):
        self.__pieces.clear()

        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.__board.get_board_symbol(row, column) == COMPUTER_SYMBOL:
                    self.__pieces.append(Piece(self.__window, column * CELL_SIZE, row * CELL_SIZE, COMPUTER_PIECE_COLOR))
                elif self.__board.get_board_symbol(row, column) == PLAYER_SYMBOL:
                    self.__pieces.append(Piece(self.__window, column * CELL_SIZE, row * CELL_SIZE, PLAYER_PIECE_COLOR))

    def open_game_application(self):
        self.__draw()
        self.__dim_screen()
        self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))
        pygame.display.update()

        self.__show_title_window()

        self.start_game()

    def __show_title_window(self):
        menu_action = self.__title_window.choose_menu_option()

        if menu_action == PLAY_BUTTON_TEXT:
            self.__show_levels_window()

        elif menu_action == RULES_BUTTON_TEXT:
            self.__show_rules_window()

    def __show_rules_window(self):
        self.__rules_window.show_rules()
        self.__show_title_window()

    def __show_levels_window(self):
        try:
            computer_strategy = self.__levels_window.choose_level()
            self.__game = Game(self.__board, computer_strategy(self.__board))

            self.__first_player_window.show(self.__player_turn)
        except GUIGoToTitleWindow:
            self.__show_title_window()

    def __dim_screen(self):
        darkened_screen = pygame.Surface(self.__window.get_size(), pygame.SRCALPHA)
        darkened_screen.fill(BLACK)
        darkened_screen.set_alpha(OPACITY_VALUE)
        self.__window.blit(darkened_screen, (0, 0))
        pygame.display.update()

    def start_game(self):
        chose_active_piece = False
        active_piece = None

        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(FPS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.__player_turn == True:
                    mouse_x, mouse_y = event.pos

                    if chose_active_piece == True and self.__adjacent_empty_cell_clicked(mouse_x, mouse_y, active_piece):
                        # move active piece to adjacent empty cell
                        adjacent_cell_x = (mouse_x // CELL_SIZE) * CELL_SIZE
                        adjacent_cell_y = (mouse_y // CELL_SIZE) * CELL_SIZE

                        self.__move_to_adjacent_cell(active_piece, adjacent_cell_x, adjacent_cell_y)

                        if self.__is_game_won():
                            run = False

                    else:
                        piece_index = 0

                        while self.__player_turn == True and piece_index < len(self.__pieces):
                            piece = self.__pieces[piece_index]

                            if piece.was_clicked(mouse_x, mouse_y) and piece.color == PLAYER_PIECE_COLOR and chose_active_piece == False:
                                # set current active piece
                                active_piece = piece
                                active_piece.set_active_state(True)
                                chose_active_piece = True

                            elif piece.was_clicked(mouse_x, mouse_y) and piece.color == PLAYER_PIECE_COLOR and chose_active_piece == True:
                                if active_piece == piece:
                                    # deselect the active piece
                                    piece.set_active_state(False)
                                    active_piece = None
                                    chose_active_piece = False
                                else:
                                    # change the current active piece with another
                                    previous_active_piece = active_piece
                                    previous_active_piece.set_active_state(False)
                                    active_piece = piece
                                    active_piece.set_active_state(True)

                            elif piece.was_clicked(mouse_x, mouse_y) and piece.color == COMPUTER_PIECE_COLOR and chose_active_piece == True:
                                # capturing move
                                self.__capturing_move(active_piece, piece)

                                if self.__is_game_won():
                                    run = False

                            piece_index += 1

            if self.__player_turn == False:
                pygame.time.delay(500)

                self.__computer_turn()
                self.__player_turn = True

                if self.__is_game_won():
                    run = False

            self.__draw()

        self.__restart_game()

    def __is_empty_cell(self, mouse_x, mouse_y):
        row = mouse_y // CELL_SIZE
        column = mouse_x // CELL_SIZE

        if self.__board.get_board_symbol(row, column) == EMPTY_CELL_SYMBOL:
            return True

        return False

    def __adjacent_empty_cell_clicked(self, mouse_x, mouse_y, piece: Piece):
        if not self.__is_empty_cell(mouse_x, mouse_y):
            return False

        if piece.y < mouse_y < (piece.y + CELL_SIZE): # same row
            if (piece.x - CELL_SIZE) < mouse_x < piece.x: # left cell
                return True
            elif (piece.x + CELL_SIZE) < mouse_x < (piece.x + 2 * CELL_SIZE): # right cell
                return True

        elif piece.x < mouse_x < (piece.x + CELL_SIZE): # same column
            if (piece.y - CELL_SIZE) < mouse_y < piece.y: # top cell
                return True
            elif (piece.y + CELL_SIZE) < mouse_y < (piece.y + 2 * CELL_SIZE): # bottom cell
                return True

        return False

    def __move_to_adjacent_cell(self, active_piece, adjacent_cell_x, adjacent_cell_y):
        try:
            self.__game.player_move(active_piece.row, active_piece.column, adjacent_cell_y // CELL_SIZE, adjacent_cell_x // CELL_SIZE)
            active_piece.x, active_piece.y = adjacent_cell_x, adjacent_cell_y
            active_piece.set_active_state(True)
            self.__player_turn = False

            self.__draw()
            pygame.display.update()
        except BoardError:
            pass

    def __capturing_move(self, active_piece, opponent_piece):
        try:
            self.__game.player_move(active_piece.row, active_piece.column, opponent_piece.row, opponent_piece.column)
            active_piece.x = opponent_piece.x
            active_piece.y = opponent_piece.y
            self.__pieces.remove(opponent_piece)
            active_piece.set_active_state(True)
            self.__player_turn = False

            self.__draw()
            pygame.display.update()
        except BoardError:
            pass

    def __computer_turn(self):
        piece_position, move_position = self.__game.computer_move()

        for piece in self.__pieces:
            if piece.row == move_position.x and piece.column == move_position.y and piece.color == PLAYER_PIECE_COLOR:
                self.__pieces.remove(piece)

            elif piece.row == piece_position.x and piece.column == piece_position.y and piece.color == COMPUTER_PIECE_COLOR:
                active_piece = piece

                active_piece.x = move_position.y * CELL_SIZE
                active_piece.y = move_position.x * CELL_SIZE

    def __is_game_won(self):
        if self.__player_turn == False:
            symbol = PLAYER_SYMBOL
        else: # self.__player_turn == True:
            symbol = COMPUTER_SYMBOL

        try:
            self.__board.is_board_won(symbol)
            return False
        except GameOver:
            self.__draw()
            self.__draw_winner(symbol)
            return True

    def __draw_winner(self, symbol):
        self.__dim_screen()

        if symbol == PLAYER_SYMBOL:
            self.__window.blit(WINNER_BANNER, (WIDTH // 2 - WINNER_BANNER.get_width() // 2, HEIGHT // 2 - WINNER_BANNER.get_height() // 2))
        else:
            self.__window.blit(LOSER_BANNER, (WIDTH // 2 - LOSER_BANNER.get_width() // 2, HEIGHT // 2 - LOSER_BANNER.get_height() // 2))

        pygame.display.update()
        pygame.time.delay(5000)

    def __draw(self):
        self.__board_drawing.draw()

        for piece in self.__pieces:
            piece.draw()

    def __restart_game(self):
        self.__board.load_start_board()
        self.__load_pieces()

        self.__draw()
        self.__dim_screen()
        self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))
        pygame.display.update()

        self.__player_turn = random.choice([True, False])

        self.__show_levels_window()

        self.start_game()