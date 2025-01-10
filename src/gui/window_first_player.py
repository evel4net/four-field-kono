import pygame

from src.constants import (BACKGROUND_SCROLL, PADDING, UPDATE_RECTANGLE, FONT_COLOR, WIDTH, HEIGHT,
                           PLAYER_TURN_TEXT, COMPUTER_TURN_TEXT, PLAYER_PIECE, COMPUTER_PIECE, CELL_SIZE, PLAYER_TURN_FONT)


class FirstPlayerWindow(object):
    def __init__(self, window):
        self.__window = window

    def __draw(self, player_turn_text, player_piece):
        self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))

        player_turn_text_draw = PLAYER_TURN_FONT.render(player_turn_text, 1, FONT_COLOR)
        player_turn_text_rect = pygame.rect.Rect(WIDTH // 2 - player_turn_text_draw.get_width() // 2, HEIGHT // 3 - player_turn_text_draw.get_height() // 2, player_turn_text_draw.get_width(), player_turn_text_draw.get_height())

        self.__window.blit(player_turn_text_draw, (player_turn_text_rect.x, player_turn_text_rect.y))

        self.__window.blit(player_piece, (WIDTH // 2 - CELL_SIZE, player_turn_text_rect.y + player_turn_text_draw.get_height() + PADDING))

        sentence_end = PLAYER_TURN_FONT.render("pieces.", 1, FONT_COLOR)
        self.__window.blit(sentence_end, (WIDTH // 2 + PADDING, player_turn_text_rect.y + player_turn_text_draw.get_height() + PADDING + (CELL_SIZE // 2 - sentence_end.get_height() // 2)))

        pygame.display.update(UPDATE_RECTANGLE)

    def show(self, is_player_turn: bool):
        if is_player_turn:
            player_turn_text = PLAYER_TURN_TEXT
            player_piece = PLAYER_PIECE
        else:
            player_turn_text = COMPUTER_TURN_TEXT
            player_piece = COMPUTER_PIECE

        self.__draw(player_turn_text, player_piece)

        pygame.time.delay(5000)