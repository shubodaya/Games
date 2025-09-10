import tkinter as tk
from tkinter import messagebox
import random
import pygame
import threading
import time
import csv
import os
from datetime import datetime

pygame.mixer.init()

# Load sounds
sound_files = {"click": "sounds/click.wav",
               "win": "sounds/win.wav",
               "draw": "sounds/draw.wav"}

sounds = {}
for key, file in sound_files.items():
    sounds[key] = pygame.mixer.Sound(file)

volumes = {"click": 0.5, "win": 0.7, "draw": 0.6}
for key in sounds:
    sounds[key].set_volume(volumes[key])

sound_enabled = True
LOG_FILE = "tictactoe_log.csv"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Player", "Row", "Col", "Result"])

class StartMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe Settings")

        tk.Label(master, text="Select Number of Players:").pack()
        self.player_var = tk.IntVar(value=1)
        tk.Radiobutton(master, text="1 Player", variable=self.player_var, value=1).pack()
        tk.Radiobutton(master, text="2 Players", variable=self.player_var, value=2).pack()

        tk.Label(master, text="Select Difficulty:").pack()
        self.diff_var = tk.StringVar(value="medium")
        tk.Radiobutton(master, text="Easy", variable=self.diff_var, value="easy").pack()
        tk.Radiobutton(master, text="Medium", variable=self.diff_var, value="medium").pack()
        tk.Radiobutton(master, text="Hard", variable=self.diff_var, value="hard").pack()

        tk.Label(master, text="Select Board Size:").pack()
        self.size_var = tk.IntVar(value=3)
        tk.Radiobutton(master, text="3x3", variable=self.size_var, value=3).pack()
        tk.Radiobutton(master, text="4x4", variable=self.size_var, value=4).pack()
        tk.Radiobutton(master, text="5x5", variable=self.size_var, value=5).pack()

        tk.Label(master, text="Adjust Volumes:").pack()
        self.vol_sliders = {}
        for key in ["click", "win", "draw"]:
            frame = tk.Frame(master)
            tk.Label(frame, text=key).pack(side=tk.LEFT)
            slider = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
            slider.set(volumes[key])
            slider.pack(side=tk.LEFT)
            frame.pack()
            self.vol_sliders[key] = slider

        tk.Button(master, text="Start Game", command=self.start_game).pack(pady=10)

    def start_game(self):
        global PLAYER_COUNT, DIFFICULTY, BOARD_SIZE, volumes
        PLAYER_COUNT = self.player_var.get()
        DIFFICULTY = self.diff_var.get()
        BOARD_SIZE = self.size_var.get()
        for key in self.vol_sliders:
            volumes[key] = self.vol_sliders[key].get()
            sounds[key].set_volume(volumes[key])
        self.master.destroy()
        GameWindow()

class GameWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = "X"
        self.create_board()
        self.status_label = tk.Label(self.root, text=f"{self.turn}'s turn", font=("Helvetica", 14))
        self.status_label.pack(pady=5)
        self.root.mainloop()

    def create_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.board_frame, text="", font=("Helvetica", 32),
                                width=5, height=2,
                                command=lambda row=r, col=c: self.click_cell(row, col))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def click_cell(self, row, col):
        if self.board[row][col] == "":
            self.make_move(row, col, self.turn)
            if self.check_winner():
                return
            self.turn = "O" if self.turn == "X" else "X"
            self.status_label.config(text=f"{self.turn}'s turn")
            if PLAYER_COUNT == 1 and self.turn == "O":
                self.root.after(400, self.bot_move)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].config(text=player, fg="red" if player=="X" else "blue")
        self.play_sound("click")
        self.log_move(player, row, col)

    def bot_move(self):
        if DIFFICULTY == "easy":
            empty = [(r,c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] == ""]
            r,c = random.choice(empty)
        elif DIFFICULTY == "medium":
            # block or win one step ahead
            r,c = self.medium_ai("O")
        else:
            r,c = self.minimax_best_move()
        self.make_move(r, c, "O")
        if self.check_winner():
            return
        self.turn = "X"
        self.status_label.config(text=f"{self.turn}'s turn")

    def medium_ai(self, player):
        opponent = "X"
        # Try to win
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == "":
                    self.board[r][c] = player
                    if self.check_winner_sim(player):
                        self.board[r][c] = ""
                        return r,c
                    self.board[r][c] = ""
        # Try to block opponent
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] == "":
                    self.board[r][c] = opponent
                    if self.check_winner_sim(opponent):
                        self.board[r][c] = ""
                        return r,c
                    self.board[r][c] = ""
        # else random
        empty = [(r,c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] == ""]
        return random.choice(empty)

    def minimax_best_move(self):
        # Placeholder: medium AI
        return self.medium_ai("O")

    def check_winner_sim(self, player):
        lines = []
        for r in range(BOARD_SIZE):
            lines.append([(r, c) for c in range(BOARD_SIZE)])
        for c in range(BOARD_SIZE):
            lines.append([(r, c) for r in range(BOARD_SIZE)])
        lines.append([(i, i) for i in range(BOARD_SIZE)])
        lines.append([(i, BOARD_SIZE-1-i) for i in range(BOARD_SIZE)])
        for line in lines:
            values = [self.board[r][c] for r,c in line]
            if values.count(player) == BOARD_SIZE:
                return True
        return False

    def check_winner(self):
        lines = []
        for r in range(BOARD_SIZE):
            lines.append([(r, c) for c in range(BOARD_SIZE)])
        for c in range(BOARD_SIZE):
            lines.append([(r, c) for r in range(BOARD_SIZE)])
        lines.append([(i, i) for i in range(BOARD_SIZE)])
        lines.append([(i, BOARD_SIZE-1-i) for i in range(BOARD_SIZE)])

        for line in lines:
            values = [self.board[r][c] for r,c in line]
            if values.count(values[0]) == BOARD_SIZE and values[0] != "":
                self.highlight_line(line)
                self.play_sound("win")
                messagebox.showinfo("Winner", f"{values[0]} wins!")
                self.log_result(values[0])
                self.ask_new_game()
                return True
        if all(self.board[r][c] != "" for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
            self.play_sound("draw")
            messagebox.showinfo("Draw", "It's a tie!")
            self.log_result("Draw")
            self.ask_new_game()
            return True
        return False

    def highlight_line(self, coords):
        def flash():
            for _ in range(6):
                for r,c in coords:
                    self.buttons[r][c].config(bg="yellow")
                self.root.update()
                time.sleep(0.2)
                for r,c in coords:
                    self.buttons[r][c].config(bg="white")
                self.root.update()
                time.sleep(0.2)
        threading.Thread(target=flash).start()

    def play_sound(self, key):
        if sound_enabled:
            sounds[key].play()

    def log_move(self, player, row, col):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, player, row, col, ""])

    def log_result(self, result):
        rows = []
        with open(LOG_FILE, "r", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
        for i in range(len(rows)-1, 0, -1):
            if rows[i][4] == "":
                rows[i][4] = result
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def ask_new_game(self):
        answer = messagebox.askyesno("Play Again?", "Do you want to play another round?")
        if answer:
            self.reset_game()
        else:
            self.root.destroy()
            root = tk.Tk()
            StartMenu(root)
            root.mainloop()

    def reset_game(self):
        # Clear the board data
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
        # Get default button background
        default_bg = self.root.cget("bg")
    
        # Reset all buttons
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c]['text'] = ""
                self.buttons[r][c]['state'] = tk.NORMAL
                self.buttons[r][c]['bg'] = default_bg
    
        # Reset current turn
        self.turn = "X"
        self.status_label.config(text=f"{self.turn}'s turn")





def main():
    root = tk.Tk()
    StartMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()

