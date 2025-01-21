import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk  # For background image support

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("1000x800+300+0")
        self.root.resizable(False, False)

        # Load and set background image
        self.bg_image = Image.open("a5.png")  # Ensure "a5.png" is in the same folder
        self.bg_image = self.bg_image.resize((1000, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create canvas for text overlay
        self.canvas = tk.Canvas(root, width=1000, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Title
        self.canvas.create_text(500, 50, text="TIC TAC TOE", font=("Helvetica", 50, "bold"), fill="#FFD700")

        # Players' names input
        self.canvas.create_text(100, 115, text="Player X:", font=("Helvetica",20), fill="white")
        self.player_x_entry = tk.Entry(root, font=("Helvetica", 20), bd=2, relief="solid", justify="center", bg="#0F3460", fg="#00F0FF")
        self.player_x_entry.place(x=200, y=105, width=250, height=25)

        self.canvas.create_text(100, 160, text="Player O:", font=("Helvetica",20), fill="white")
        self.player_o_entry = tk.Entry(root, font=("Helvetica", 20), bd=2, relief="solid", justify="center", bg="#0F3460", fg="#FF0050")
        self.player_o_entry.place(x=200, y=145, width=250, height=25)

        # Date and time display
        self.date_time_text = self.canvas.create_text(700, 115, text="", font=("Helvetica", 15), fill="white")
        self.update_date_time()

        # Scoreboard
        self.score_text = self.canvas.create_text(710, 160, text="Score: X - 0 | O - 0", font=("Helvetica", 24), fill="#00FF00")

        # Game board frame
        self.board_frame = tk.Frame(root, bg="black")  # Dark background
        self.board_frame.place(x=210, y=185)

        self.buttons = []
        for i in range(9):
            button = tk.Button(
                self.board_frame, text="", font=("Helvetica", 35, "bold"), width=5, height=2,
                command=lambda i=i: self.on_button_click(i), relief="flat",
                bg="#0F3460", fg="white",  # Dark background with white text
                activebackground="#16213E",  # Slightly different hover color
                borderwidth=5, highlightthickness=0
            )
            button.grid(row=i // 3, column=i % 3, padx=15, pady=15)
            self.buttons.append(button)

        # Reset button
        self.reset_button = tk.Button(root, text="Restart Game", font=("Helvetica",18),bd=7, bg="blue", fg="white", command=self.reset_game)
        self.reset_button.place(x=390, y=742, width=190, height=40)

        # Game state variables
        self.current_player = "X"
        self.board = [""] * 9
        self.score_x = 0
        self.score_o = 0

    def update_date_time(self):
        """Update the date and time display every second."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.canvas.itemconfig(self.date_time_text, text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_date_time)

    def on_button_click(self, index):
        """Handles button clicks for the game logic."""
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.animate_button(index)
            if self.check_winner():
                self.update_score()
                messagebox.showinfo("Game Over", f"{self.get_current_player_name()} wins!")
                self.reset_game()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.switch_player()

    def get_current_player_name(self):
        """Returns the name of the current player."""
        player_x = self.player_x_entry.get().strip() or "Player X"
        player_o = self.player_o_entry.get().strip() or "Player O"
        return player_x if self.current_player == "X" else player_o

    def update_score(self):
        """Update the score when a player wins."""
        if self.current_player == "X":
            self.score_x += 1
        else:
            self.score_o += 1
        self.canvas.itemconfig(self.score_text, text=f"Score: X - {self.score_x} | O - {self.score_o}")

    def animate_button(self, index):
        """Animate button press with color change and glow effect."""
        if self.current_player == "X":
            color = "#00F0FF"  # Neon blue for X
            glow_effect = ("Helvetica", 35, "bold")
        else:
            color = "#FF0050"  # Neon red for O
            glow_effect = ("Helvetica", 35, "bold")

        self.buttons[index].config(
            text=self.current_player,
            font=glow_effect,
            fg=color,
            bg="#1a1a2e",  # Dark grid background
        )

    def switch_player(self):
        """Switch the current player."""
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Check if there's a winner."""
        win_patterns = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for pattern in win_patterns:
            if self.board[pattern[0]] == self.board[pattern[1]] == self.board[pattern[2]] != "":
                return True
        return False

    def reset_game(self):
        """Reset the game board and prepare for a new game."""
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="", bg="#0F3460")
        self.current_player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
