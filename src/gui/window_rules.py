import sys
import pygame

from src.constants import (PADDING, FPS, RULES_TEXT, BUTTON_FONT, OK_BUTTON_TEXT, FONT_COLOR, HOVERING_SYMBOL, SYMBOLS_FONT, TEXT_FONT, TEXT_SPACING,
                               MENU_SPACING, RULES_LINE_LENGTH, HEIGHT, WIDTH, BACKGROUND_SCROLL, UPDATE_RECTANGLE, HOVERING_SYMBOL_SPACING)


class RulesWindow(object):
    def __init__(self, window):
        self.__window = window

        self.__ok_button_draw = BUTTON_FONT.render(OK_BUTTON_TEXT, 1, FONT_COLOR)
        self.__ok_button_rect = pygame.rect.Rect(WIDTH // 2 - self.__ok_button_draw.get_width() // 2, HEIGHT - PADDING - self.__ok_button_draw.get_height() - MENU_SPACING, self.__ok_button_draw.get_width(), self.__ok_button_draw.get_height())

        self.__hovering_symbol_draw = SYMBOLS_FONT.render(HOVERING_SYMBOL, 1, FONT_COLOR)

    def __draw(self):
        self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))

        self.__draw__text()
        self.__window.blit(self.__ok_button_draw, (self.__ok_button_rect.x, self.__ok_button_rect.y))

        pygame.display.update(UPDATE_RECTANGLE)

    def __draw__text(self):
        to_blit_lines = []
        current_line = ""

        sentences = RULES_TEXT.splitlines()

        for sentence in sentences:
            words = sentence.split(" ")

            for word in words:
                if len(current_line) < RULES_LINE_LENGTH:
                    current_line += " " + word
                if len(current_line) >= RULES_LINE_LENGTH:
                    to_blit_lines.append(current_line)
                    current_line = ""

            if current_line != "":
                to_blit_lines.append(current_line)
                current_line = ""

        y_position = 4 * PADDING
        for line in to_blit_lines:
            line_draw = TEXT_FONT.render(str(line), 1, FONT_COLOR)
            self.__window.blit(line_draw, (WIDTH // 2 - line_draw.get_width() // 2, y_position))

            y_position += line_draw.get_height() + TEXT_SPACING

    def show_rules(self):
        self.__draw()

        clock = pygame.time.Clock()
        already_hovered_button = False

        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    if self.__clicked_ok_button(mouse_x, mouse_y):
                        return

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    if self.__hovered_ok_button_rect(mouse_x, mouse_y) and already_hovered_button == False:
                        already_hovered_button = True
                        self.__window.blit(self.__hovering_symbol_draw, (self.__ok_button_rect.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, self.__ok_button_rect.y - HOVERING_SYMBOL_SPACING))
                        pygame.display.update(pygame.rect.Rect(self.__ok_button_rect.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, self.__ok_button_rect.y - HOVERING_SYMBOL_SPACING, self.__hovering_symbol_draw.get_width(), self.__hovering_symbol_draw.get_height()))

                    elif not self.__hovered_ok_button_rect(mouse_x, mouse_y) and already_hovered_button == True:
                        self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))
                        pygame.display.update(pygame.rect.Rect(self.__ok_button_rect.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, self.__ok_button_rect.y - HOVERING_SYMBOL_SPACING, self.__hovering_symbol_draw.get_width(), self.__hovering_symbol_draw.get_height()))
                        already_hovered_button = False

    def __clicked_ok_button(self, mouse_x, mouse_y):
        if pygame.Rect.collidepoint(self.__ok_button_rect, mouse_x, mouse_y):
            return True

        return  False

    def __hovered_ok_button_rect(self, mouse_x, mouse_y):
        if pygame.Rect.collidepoint(self.__ok_button_rect, mouse_x, mouse_y):
            return True

        return False