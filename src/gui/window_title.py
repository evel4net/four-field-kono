import sys
import pygame

from src.constants import (PADDING, FPS, BUTTON_FONT, GAME_TITLE, FONT_COLOR, PLAY_BUTTON_TEXT, RULES_BUTTON_TEXT, QUIT_BUTTON_TEXT, HOVERING_SYMBOL,
                                   SYMBOLS_FONT, MENU_SPACING, WIDTH, HEIGHT, BACKGROUND_SCROLL, UPDATE_RECTANGLE, TITLE_FONT, HOVERING_SYMBOL_SPACING)


class TitleWindow(object):
    def __init__(self, window):
        self.__window = window

        self.__title_draw = TITLE_FONT.render(GAME_TITLE, 1, FONT_COLOR)
        self.__title_rect = pygame.rect.Rect(WIDTH // 2 - self.__title_draw.get_width() // 2, HEIGHT // 4, self.__title_draw.get_width(), self.__title_draw.get_height())

        self.__play_button_draw = BUTTON_FONT.render(PLAY_BUTTON_TEXT, 1, FONT_COLOR)
        self.__play_button_rect = pygame.rect.Rect(WIDTH // 2 - self.__play_button_draw.get_width() // 2, self.__title_rect.y + self.__title_rect.height + MENU_SPACING, self.__play_button_draw.get_width(), self.__play_button_draw.get_height())

        self.__rules_button_draw = BUTTON_FONT.render(RULES_BUTTON_TEXT, 1, FONT_COLOR)
        self.__rules_button_rect = pygame.rect.Rect(WIDTH // 2 - self.__rules_button_draw.get_width() // 2, self.__play_button_rect.y + self.__play_button_rect.height + MENU_SPACING, self.__rules_button_draw.get_width(), self.__rules_button_draw.get_height())

        self.__quit_button_draw = BUTTON_FONT.render(QUIT_BUTTON_TEXT, 1, FONT_COLOR)
        self.__quit_button_rect = pygame.rect.Rect(WIDTH // 2 - self.__quit_button_draw.get_width() // 2, self.__rules_button_rect.y + self.__rules_button_rect.height + MENU_SPACING, self.__quit_button_draw.get_width(), self.__quit_button_draw.get_height())

        self.__hovering_symbol_draw = SYMBOLS_FONT.render(HOVERING_SYMBOL, 1, FONT_COLOR)

    def __draw(self):
        self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))

        self.__window.blit(self.__title_draw, (self.__title_rect.x, self.__title_rect.y))
        self.__window.blit(self.__play_button_draw, (self.__play_button_rect.x, self.__play_button_rect.y))
        self.__window.blit(self.__rules_button_draw, (self.__rules_button_rect.x, self.__rules_button_rect.y))
        self.__window.blit(self.__quit_button_draw, (self.__quit_button_rect.x, self.__quit_button_rect.y))

        pygame.display.update(UPDATE_RECTANGLE)

    def choose_menu_option(self):
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

                    menu_action = self.__clicked_button(mouse_x, mouse_y)

                    if menu_action == PLAY_BUTTON_TEXT:
                        return menu_action
                    elif menu_action == RULES_BUTTON_TEXT:
                        return menu_action
                    elif menu_action == QUIT_BUTTON_TEXT:
                        run = False
                        pygame.quit()
                        sys.exit()

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
                        pygame.display.update(pygame.rect.Rect(hovered_button.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, hovered_button.y - HOVERING_SYMBOL_SPACING , self.__hovering_symbol_draw.get_width(), self.__hovering_symbol_draw.get_height()))

                    elif hovered_button == None:
                        if current_hovered_button != None:
                            self.__window.blit(BACKGROUND_SCROLL, (PADDING, PADDING))
                            pygame.display.update(pygame.rect.Rect(current_hovered_button.x - self.__hovering_symbol_draw.get_width() - HOVERING_SYMBOL_SPACING, current_hovered_button.y - HOVERING_SYMBOL_SPACING, self.__hovering_symbol_draw.get_width(), self.__hovering_symbol_draw.get_height()))
                            current_hovered_button = None

    def __clicked_button(self, mouse_x, mouse_y):
        if pygame.Rect.collidepoint(self.__play_button_rect, mouse_x, mouse_y):
            return PLAY_BUTTON_TEXT
        elif pygame.Rect.collidepoint(self.__rules_button_rect, mouse_x, mouse_y):
            return RULES_BUTTON_TEXT
        elif pygame.Rect.collidepoint(self.__quit_button_rect, mouse_x, mouse_y):
            return QUIT_BUTTON_TEXT
        else:
            return None

    def __hovered_button_rect(self, mouse_x, mouse_y):
        if pygame.Rect.collidepoint(self.__play_button_rect, mouse_x, mouse_y):
            return self.__play_button_rect
        elif pygame.Rect.collidepoint(self.__rules_button_rect, mouse_x, mouse_y):
            return self.__rules_button_rect
        elif pygame.Rect.collidepoint(self.__quit_button_rect, mouse_x, mouse_y):
            return self.__quit_button_rect
        else:
            return None