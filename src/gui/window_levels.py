import sys
import pygame

from src.services.computer_strategies.computer_capturing_strategy import ComputerCapturingStrategy
from src.services.computer_strategies.computer_intelligent_strategy import ComputerIntelligentStrategy
from src.services.computer_strategies.computer_random_strategy import ComputerRandomStrategy
from src.constants import (EASY_BUTTON_TEXT, LEVELS_TEXT, MEDIUM_BUTTON_TEXT, PADDING, FPS, TITLE_FONT, FONT_COLOR,
                           BUTTON_FONT, HARD_BUTTON_TEXT, HOVERING_SYMBOL, SYMBOLS_FONT, BACK_BUTTON_TEXT, WIDTH, HEIGHT, MENU_SPACING,
                           BACKGROUND_SCROLL, UPDATE_RECTANGLE, HOVERING_SYMBOL_SPACING)
from src.exceptions import GUIGoToTitleWindow

class LevelsWindow(object):
    def __init__(self, window):
        self.__window = window
        self.__computer_strategies = {EASY_BUTTON_TEXT: ComputerRandomStrategy, MEDIUM_BUTTON_TEXT: ComputerCapturingStrategy, HARD_BUTTON_TEXT: ComputerIntelligentStrategy}

        self.__levels_text_draw = TITLE_FONT.render(LEVELS_TEXT, 1, FONT_COLOR)
        self.__levels_text_rect = pygame.rect.Rect(WIDTH // 2 - self.__levels_text_draw.get_width() // 2, HEIGHT // 4, self.__levels_text_draw.get_width(), self.__levels_text_draw.get_height())

        self.__easy_button_draw = BUTTON_FONT.render(EASY_BUTTON_TEXT, 1, FONT_COLOR)
        self.__easy_button_rect = pygame.rect.Rect(WIDTH // 2 - self.__easy_button_draw.get_width() // 2, self.__levels_text_rect.y + self.__levels_text_rect.height + MENU_SPACING, self.__easy_button_draw.get_width(), self.__easy_button_draw.get_height())

        self.__medium_button_draw = BUTTON_FONT.render(MEDIUM_BUTTON_TEXT, 1, FONT_COLOR)
        self.__medium_button_rect = pygame.rect.Rect(WIDTH // 2 - self.__medium_button_draw.get_width() // 2, self.__easy_button_rect.y + self.__easy_button_rect.height + MENU_SPACING, self.__medium_button_draw.get_width(), self.__medium_button_draw.get_height())

        self.__hard_button_draw = BUTTON_FONT.render(HARD_BUTTON_TEXT, 1, FONT_COLOR)
        self.__hard_button_rect = pygame.rect.Rect(WIDTH // 2 - self.__hard_button_draw.get_width() // 2, self.__medium_button_rect.y + self.__medium_button_rect.height + MENU_SPACING, self.__hard_button_draw.get_width(), self.__hard_button_draw.get_height())

        self.__back_button_draw = BUTTON_FONT.render(BACK_BUTTON_TEXT, 1, FONT_COLOR)
        self.__back_button_rect = pygame.rect.Rect(WIDTH // 2 - self.__back_button_draw.get_width() // 2, HEIGHT - PADDING - self.__back_button_draw.get_height() - MENU_SPACING, self.__back_button_draw.get_width(), self.__back_button_draw.get_height())

        self.__hovering_symbol_draw = SYMBOLS_FONT.render(HOVERING_SYMBOL, 1, FONT_COLOR)

    def __draw(self):
        self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))

        self.__window.blit(self.__levels_text_draw, (self.__levels_text_rect.x, self.__levels_text_rect.y))
        self.__window.blit(self.__easy_button_draw, (self.__easy_button_rect.x, self.__easy_button_rect.y))
        self.__window.blit(self.__medium_button_draw, (self.__medium_button_rect.x, self.__medium_button_rect.y))
        self.__window.blit(self.__hard_button_draw, (self.__hard_button_rect.x, self.__hard_button_rect.y))
        self.__window.blit(self.__back_button_draw, (self.__back_button_rect.x, self.__back_button_rect.y))

        pygame.display.update(UPDATE_RECTANGLE)

    def choose_level(self):
        self.__draw()

        current_hovered_button = None
        clock = pygame.time.Clock()

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

                    if self.__clicked_back_button(mouse_x, mouse_y):
                        raise GUIGoToTitleWindow()

                    computer_strategy = self.__clicked_level_button(mouse_x, mouse_y)

                    if computer_strategy != None:
                        return computer_strategy

                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    hovered_button = self.__hovered_button_rect(mouse_x, mouse_y)

                    if hovered_button != None:
                        if current_hovered_button == None:
                            current_hovered_button = hovered_button
                        elif current_hovered_button != None:
                            self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))
                            pygame.display.update(pygame.rect.Rect(current_hovered_button.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, current_hovered_button.y - HOVERING_SYMBOL_SPACING, self.__hovering_symbol_draw.get_width(), self.__hovering_symbol_draw.get_height()))

                        self.__window.blit(self.__hovering_symbol_draw, (hovered_button.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, hovered_button.y - HOVERING_SYMBOL_SPACING))
                        pygame.display.update(pygame.rect.Rect(hovered_button.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, hovered_button.y - HOVERING_SYMBOL_SPACING, self.__hovering_symbol_draw.get_width(), self.__hovering_symbol_draw.get_height()))

                    elif hovered_button == None:
                        if current_hovered_button != None:
                            self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))
                            pygame.display.update(pygame.rect.Rect(current_hovered_button.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, current_hovered_button.y - HOVERING_SYMBOL_SPACING, self.__hovering_symbol_draw.get_width(), self.__hovering_symbol_draw.get_height()))
                            current_hovered_button = None


    def __clicked_level_button(self, mouse_x, mouse_y):
        if pygame.Rect.collidepoint(self.__easy_button_rect, mouse_x, mouse_y):
            return self.__computer_strategies[EASY_BUTTON_TEXT]
        elif pygame.Rect.collidepoint(self.__medium_button_rect, mouse_x, mouse_y):
            return self.__computer_strategies[MEDIUM_BUTTON_TEXT]
        elif pygame.Rect.collidepoint(self.__hard_button_rect, mouse_x, mouse_y):
            return self.__computer_strategies[HARD_BUTTON_TEXT]
        else:
            return None

    def __clicked_back_button(self, mouse_x, mouse_y):
        if pygame.Rect.collidepoint(self.__back_button_rect, mouse_x, mouse_y):
            return True

        return False

    def __hovered_button_rect(self, mouse_x, mouse_y):
        if pygame.Rect.collidepoint(self.__easy_button_rect, mouse_x, mouse_y):
            return self.__easy_button_rect
        elif pygame.Rect.collidepoint(self.__medium_button_rect, mouse_x, mouse_y):
            return self.__medium_button_rect
        elif pygame.Rect.collidepoint(self.__hard_button_rect, mouse_x, mouse_y):
            return self.__hard_button_rect
        elif pygame.Rect.collidepoint(self.__back_button_rect, mouse_x, mouse_y):
            return self.__back_button_rect
        else:
            return None
