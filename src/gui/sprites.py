from src.constants import BOARD, ROWS, COLUMNS, PADDING, CELL_SIZE, PLAYER_PIECE_COLOR, PLAYER_PIECE, COMPUTER_PIECE_COLOR, COMPUTER_PIECE


class BoardDrawing(object):
    def __init__(self, window):
        self.__rows = ROWS
        self.__columns = COLUMNS
        self.__window = window

    def draw(self):
        self.__window.blit(BOARD, (0, 0))


class Piece(object):
    def __init__(self, window, x, y, color):
        self.__window = window

        # x and y represent the top-left corner's coordinates of the piece image
        self.__x = x
        self.__y = y

        self.__color = color
        self.__is_active = False

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x):
        self.__x = new_x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y):
        self.__y = new_y

    @property
    def color(self):
        return self.__color

    @property
    def row(self):
        if self.is_active:
            return (self.y + PADDING) // CELL_SIZE

        return self.y // CELL_SIZE

    @property
    def column(self):
        return self.x // CELL_SIZE

    @property
    def is_active(self):
        return self.__is_active

    def set_active_state(self, state=True):
        if state == True:
            self.y -= PADDING
        else:
            self.y += PADDING

        self.__is_active = state

    def was_clicked(self, mouse_x, mouse_y):
        if self.x <= mouse_x <= (self.x + CELL_SIZE) and self.y <= mouse_y <= (self.y + CELL_SIZE):
            return True

        return False

    def draw(self):
        if self.__color == PLAYER_PIECE_COLOR:
            self.__window.blit(PLAYER_PIECE, (self.x, self.y))
        elif self.__color == COMPUTER_PIECE_COLOR:
            self.__window.blit(COMPUTER_PIECE, (self.x, self.y))