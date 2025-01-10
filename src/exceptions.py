class BoardError(Exception):
    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

class OutOfBoardError(BoardError):
    def __init__(self):
        self.__message = "Position out of board"
        super().__init__(self.__message)

class NotOrthogonalBoardMoveError(BoardError):
    def __init__(self):
        self.__message = "Piece can only move orthogonally (up <-> down or right <-> left)"
        super().__init__(self.__message)

class IncorrectBoardMoveError(BoardError):
    def __init__(self):
        self.__message = "Incorrect move, try again"
        super().__init__(self.__message)

class GameOver(BoardError):
    def __init__(self, symbol):
        if symbol == 'O':
            super().__init__("Congratulations! You won :)")
        else:
            super().__init__("You lost :(")

# --- gui error

class GUIGoToTitleWindow(Exception):
    pass