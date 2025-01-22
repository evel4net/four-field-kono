from collections import namedtuple

import pygame
import os

pygame.font.init()

# --- colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
OPACITY_VALUE = 127

# --- game window

GAME_TITLE = "Four-field Kono"

WIDTH = 700
HEIGHT = 700
FPS = 60
PADDING = 20

BACKGROUND_SCROLL_IMAGE = pygame.image.load(os.path.join("gui", "assets", "Scroll_background.png"))
BACKGROUND_SCROLL = pygame.transform.scale(BACKGROUND_SCROLL_IMAGE, (WIDTH - 2 * PADDING, HEIGHT - 2 * PADDING))

UPDATE_RECTANGLE = pygame.rect.Rect(PADDING * 3, PADDING * 2, BACKGROUND_SCROLL.get_width() - 4 * PADDING, BACKGROUND_SCROLL.get_height() - 2 * PADDING)

# --- board

ROWS = 4
COLUMNS = 4
CELL_SIZE = WIDTH // COLUMNS
CELL_BORDER_COLOR = WHITE
MAXIMUM_NUMBER_PIECES = 8
PIECE_RADIUS = CELL_SIZE // 2 - 2 * PADDING

BOARD_IMAGE = pygame.image.load(os.path.join("gui", "assets", "Board.png"))
BOARD = pygame.transform.scale(BOARD_IMAGE, (WIDTH, HEIGHT))

# --- players

PLAYER_SYMBOL = 'O'
COMPUTER_SYMBOL = 'X'
EMPTY_CELL_SYMBOL = ' '

POSITION = namedtuple('Position', ['x', 'y'])

PLAYER_PIECE_COLOR = WHITE
PLAYER_ACTIVE_PIECE_BORDER_COLOR = BLACK
PLAYER_BOARD_COLOR = RED

PLAYER_PIECE_IMAGE = pygame.image.load(os.path.join("gui", "assets", "White_piece.png"))
PLAYER_PIECE = pygame.transform.scale(PLAYER_PIECE_IMAGE, (CELL_SIZE, CELL_SIZE))


COMPUTER_PIECE_COLOR = BLACK
COMPUTER_BOARD_COLOR = BLUE

COMPUTER_PIECE_IMAGE = pygame.image.load(os.path.join("gui", "assets", "Black_piece.png"))
COMPUTER_PIECE = pygame.transform.scale(COMPUTER_PIECE_IMAGE, (CELL_SIZE, CELL_SIZE))

# --- texts
FONT_NAME_PATH = os.path.join("gui", "assets", "KozGoPro-Light.otf")
FONT_COLOR = '#26160F'
MENU_SPACING = 50
TEXT_SPACING = 10

TITLE_FONT = pygame.font.Font(os.path.join("gui", "assets", "VINERITC.TTF"), 60)
BUTTON_FONT = pygame.font.Font(FONT_NAME_PATH, 30)
TEXT_FONT = pygame.font.Font(FONT_NAME_PATH, 17)
PLAYER_TURN_FONT = pygame.font.Font(FONT_NAME_PATH, 40)
SYMBOLS_FONT = pygame.font.SysFont("segoeuisymbol",30)

PLAY_BUTTON_TEXT = "PLAY"
RULES_BUTTON_TEXT = "RULES"
QUIT_BUTTON_TEXT = "QUIT"

LEVELS_TEXT = "Level"

EASY_BUTTON_TEXT = "EASY"
MEDIUM_BUTTON_TEXT = "MEDIUM"
HARD_BUTTON_TEXT = "HARD"

OK_BUTTON_TEXT = "OK"
BACK_BUTTON_TEXT = "BACK"

HOVERING_SYMBOL = "❋"
HOVERING_SYMBOL_SPACING = 8

RULES_TEXT = ("Board, dimension 4x4, is completely filled with pieces at the beginning, each player's pieces being set up on their half of the board.\n\n"
              "Rules:\n1. Your first move has to be a capturing move, as the board is full and no cells are empty.\nCapturing move requires a player's piece to jump over one of their own adjacent pieces (orthogonally, "
              "not diagonally) and land onto an enemy piece. Multiple captures are not allowed per turn.\n2. A piece can be moved (orthogonally, not diagonally) into an empty near cell.\n3. Game is won if the opponent "
              "has one piece left (cannot execute a capturing move with only one piece) or they are immobilized, cannot move or capture.")
RULES_LINE_LENGTH = 60

PLAYER_TURN_TEXT = "You start first with"
COMPUTER_TURN_TEXT = "Computer starts first with"

# --- winner/loser banners

WINNER_BANNER_IMAGE = pygame.image.load(os.path.join("gui", "assets", "Winner_sign.png"))
WINNER_BANNER = pygame.transform.scale_by(WINNER_BANNER_IMAGE, (3 * HEIGHT) / (4 * WINNER_BANNER_IMAGE.get_height()))

LOSER_BANNER_IMAGE = pygame.image.load(os.path.join("gui", "assets", "Loser_sign.png"))
LOSER_BANNER = pygame.transform.scale_by(LOSER_BANNER_IMAGE, (3 * HEIGHT) / (4 * LOSER_BANNER_IMAGE.get_height()))