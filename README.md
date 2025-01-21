# ❋ Four-field Kono Game
Four-field Kono point-and-click game made in Python (using pygame) for a university CS assignment. The game is human vs. computer. 

## About four-field kono
Four-field Kono is a korean strategy game being recorded to have been played since the late 19th century. The game is played on a 4x4 board with 16 pieces: 8 black pieces and 8 white pieces.

### Move types 
!! moves are executed orthogonally, not diagonally

1. CAPTURING MOVE --> one player's piece has to jump over one piece of their own and land onto an opponent's piece. The opponent's captured piece is removed from the board and replaced with the player's piece. <br>
<p align="center"><img src="/screenshots/capturing_move.gif" width="25%"/></p>


3. MOVE TO EMPTY CELL --> player's can move a piece to a near empty cell <br>
<p align="center"><img src="/screenshots/empty_cell_move.gif" width="25%"/></p>

### Game rules
- at the start of the game, the board is filled with all the pieces, each player's pieces being set on their side of the board <br>
<p align="center"><img src="/screenshots/board.png" width="25%"/></p>

- first player has to execute a capturing move because the board is full and there are no empty cells 
- players take turns, each executing only one move per turn
- a player wins if the opponent has only one piece left (cannot capture with only one piece) or the opponent is immobilized (cannot move or capture anymore)

## How to run the game
<u>*Option 1*</u>: 
    Clone the repository and open the project in your preferred IDE. Make sure you have [Python](https://www.python.org/downloads/) installed. Run the `main.py` file to start the game.

<u>*Option 2*</u> (for Windows):
    Download the `FourFieldKono-Windows-exe.zip` file, unzip it and run the `main.exe` file.

## Screenshots
<p align="center">
    <img src="/screenshots/window_title.png" width="50%"/>
    <img src="/screenshots/window_rules.png" width="50%"/>
    <img src="/screenshots/window_levels.png" width="50%"/>
    <br>
    <img src="/screenshots/window_player_starts.png" width="25%"/>
    <img src="/screenshots/window_computer_starts.png" width="25%"/>
    <br>
    <img src="/screenshots/banner_winner.png" width="25%"/>
    <img src="/screenshots/banner_loser.png" width="25%"/>
</p>
