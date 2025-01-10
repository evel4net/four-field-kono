# ❋ Four-field Kono

Four-field Kono point-and-click game made in python using pygame. The game is human VS computer. 

## About four-field kono
Four-field kono is a korea strategy game being recorded to have been played since the late 19th century. The game is played on a 4x4 board with 16 pieces: 8 black pieces and 8 white pieces.

Move types (executed orthogonally, not diagonally):
1. CAPTURING MOVE --> one player's piece has to jump over one piece of their own and land onto an opponent's piece. The opponent's captured piece is removed from the board and replaced with the player's piece.

![capturing_move_gif](./four-field-kono/screenshots/capturing_move.gif)

3. MOVE TO EMPTY CELL --> player's can move a piece to a near empty cell
![empty_cell_move_gif](./four-field-kono/screenshots/capturing_move.gif)

Game rules:
- at the start of the game, the board is filled with all the pieces, each player's pieces being set on their side of the board

![board](./four-field-kono/screenshots/board.png)

- first player has to execute a capturing move because the board is full and there are no empty cells 
- players take turns, each executing only one move per turn
- A player wins if the opponent has only one piece left (cannot capture with only one piece) or the opponent is immobilized (cannot move or capture anymore)

## How to run the game
Make sure you have [python](https://www.python.org/downloads/) installed. Clone the repository and open the project in your preferred IDE.
Run the `main.py` file to start the game.

## Screenshots
![window_title](./four-field-kono/screenshots/window_title.png)

![window_rules](./four-field-kono/screenshots/window_rules.png)

![window_levels](./four-field-kono/screenshots/window_levels.png)

![player_first](./four-field-kono/screenshots/window_player_starts.png)
![computer_first](./four-field-kono/screenshots/window_computer_starts.png)

![banner_winner](./four-field-kono/screenshots/banner_winner.png)
![banner_loser](./four-field-kono/screenshots/banner_loser.png)
