# Tic Tac Toe 🎲

A feature-rich Tic Tac Toe game built with **Python (Tkinter + Pygame)**.  
This version goes beyond the classic 3x3 board with multiple options, sound effects, and logging.

## Features
- **Single-player** (vs AI) or **Two-player** mode
- **Difficulty levels**: Easy, Medium, Hard (AI logic with blocking and winning moves)
- **Board sizes**: 3x3, 4x4, 5x5
- **Sound effects** for clicks, wins, and draws (customizable volume sliders)
- **Animated highlights** for winning lines
- **Move logging**: All games are logged to `tictactoe_log.csv` with timestamp, moves, and result
- **Replay option**: Restart directly or return to settings menu

## Requirements
- Python 3.x
- [pygame](https://www.pygame.org/news)  
  Install with:
  ```bash
  pip install pygame
## How to Run
- Clone the repo and navigate into the Tic Tac Toe folder:

```bash
cd tictactoe
```
- Run the game:

```bash
python tictactoe.py
```
- Choose your settings in the Start Menu and start playing!

## Files
- tictactoe.py → Main game script
- sounds/ → Folder containing click.wav, win.wav, draw.wav
- tictactoe_log.csv → Auto-generated log file of all matches

## Example Gameplay
- Choose 1 Player / 2 Players
- Select difficulty (Easy / Medium / Hard)
- Pick board size (3x3 / 4x4 / 5x5)
- Adjust volume sliders
- Play and check your results in the CSV log

