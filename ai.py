import random
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
class Player:
    def __init__(self, player_id):
        self.player_id = player_id

class CPUPlayer(Player):
    def __init__(self):
        super().__init__(2)  # CPU is always Player 2

    def get_move(self, quadrants):
        available_moves = []
        for qr in range(2):
            for qc in range(2):
                for r in range(3):
                    for c in range(3):
                        if not quadrants[qr][qc]['circles'][r][c].clicked:
                            available_moves.append((r, c, qr, qc))
        return random.choice(available_moves) if available_moves else None

class BoardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pentago Game")
        self.root.configure(bg='#2e2e2e')  # Darker background for the root window
        self.show_rotation = False
        self.current_player = 1
        self.quadrants = [[None, None], [None, None]]
        self.cpu_player = CPUPlayer()

        # Create frames for layout
        self.board_frame = tk.Frame(self.root, bg='#2e2e2e')
        self.board_frame.pack(pady=20)

        self.status_frame = tk.Frame(self.root, bg='#2e2e2e')
        self.status_frame.pack(pady=10)

        self.player_turn_label = tk.Label(self.status_frame, text="Player 1's Turn", font=('Helvetica', 16), bg='#2e2e2e', fg='#ffffff')
        self.player_turn_label.pack()

        self.create_board()
        self.start_game()

    def create_board(self):
        for row in range(2):
            row_frame = tk.Frame(self.board_frame, bg='#2e2e2e')
            row_frame.pack(side=tk.TOP)
            for col in range(2):
                quad_frame = tk.Frame(row_frame, width=150, height=150, bg='#8B0000', borderwidth=1, relief=tk.SOLID)
                quad_frame.grid(row=0, column=col, padx=10, pady=10)

                self.quadrants[row][col] = {
                    'frame': quad_frame,
                    'circles': [[None for _ in range(3)] for _ in range(3)],
                    'rotate_right_button': None,
                    'rotate_left_button': None
                }

                for r in range(3):
                    for c in range(3):
                        circle = tk.Button(quad_frame, width=6, height=3, bg='#98FB98', relief=tk.RAISED,
                                           command=lambda r=r, c=c, row=row, col=col: self.circle_click(r, c, row, col))
                        circle.grid(row=r, column=c, padx=5, pady=5)
                        self.quadrants[row][col]['circles'][r][c] = circle
                        
                        circle.clicked = False
                        circle.token_color = None

                        circle.bind("<Enter>", lambda e, circle=circle: self.hover_effect(circle))
                        circle.bind("<Leave>", lambda e, circle=circle: self.leave_effect(circle))

                rotate_right_button = tk.Button(quad_frame, text="Rotate Right", command=lambda row=row, col=col: self.rotate_quadrant(row, col, right=True))
                rotate_right_button.grid(row=3, column=1, pady=5)
                rotate_right_button.grid_remove()

                rotate_left_button = tk.Button(quad_frame, text="Rotate Left", command=lambda row=row, col=col: self.rotate_quadrant(row, col, right=False))
                rotate_left_button.grid(row=3, column=0, pady=5)
                rotate_left_button.grid_remove()

                self.quadrants[row][col]['rotate_right_button'] = rotate_right_button
                self.quadrants[row][col]['rotate_left_button'] = rotate_left_button

    def start_game(self):
        if self.current_player == 2:  # If CPU is the first player
            self.root.after(100, self.cpu_move)

    def circle_click(self, row, col, quad_row, quad_col):
        if self.show_rotation:
            return

        if not self.quadrants[quad_row][quad_col]['circles'][row][col].clicked:
            print(f"Circle at row {row}, column {col} clicked in quadrant ({quad_row}, {quad_col})!")
            self.quadrants[quad_row][quad_col]['circles'][row][col].clicked = True
            if self.current_player == 1:
                self.quadrants[quad_row][quad_col]['circles'][row][col].config(bg='#000000')
                self.quadrants[quad_row][quad_col]['circles'][row][col].token_color = '#000000'
            else:
                self.quadrants[quad_row][quad_col]['circles'][row][col].config(bg='#ff0000')
                self.quadrants[quad_row][quad_col]['circles'][row][col].token_color = '#ff0000'

            self.show_rotation_buttons()

            if self.check_winner():
                print(f"Player {self.current_player} wins!")
                messagebox.showinfo("Winner", f"Player {self.current_player} wins!")
                self.reset_board()
                return

            

    def cpu_move(self):
        print("CPU is making a move...")
        move = self.cpu_player.get_move(self.quadrants)
        r, c, qr, qc = move
        print(f"R : {r} C : {c} QR : {qr} QC : {qc}")
        if move:
            self.circle_click(r, c, qr, qc)
            self.rotate_quadrant(qr, qc, right=random.choice([False, True]))
        else:
            print("No available moves for CPU.")

    def show_rotation_buttons(self):
        self.show_rotation = True
        for row in range(2):
            for col in range(2):
                self.quadrants[row][col]['rotate_right_button'].grid()
                self.quadrants[row][col]['rotate_left_button'].grid()

    def hide_rotation_buttons(self):
        self.show_rotation = False
        for row in range(2):
            for col in range(2):
                self.quadrants[row][col]['rotate_right_button'].grid_remove()
                self.quadrants[row][col]['rotate_left_button'].grid_remove()

    def rotate_quadrant(self, row, col, right=True):
        quad = self.quadrants[row][col]
        circles = quad['circles']
        
        rotated_tokens = [[None for _ in range(3)] for _ in range(3)]
        rotated_clicked = [[False for _ in range(3)] for _ in range(3)]
        
        if right:
            for r in range(3):
                for c in range(3):
                    rotated_tokens[c][2-r] = circles[r][c].token_color
                    rotated_clicked[c][2-r] = circles[r][c].clicked
        else:
            for r in range(3):
                for c in range(3):
                    rotated_tokens[2-c][r] = circles[r][c].token_color
                    rotated_clicked[2-c][r] = circles[r][c].clicked

        for r in range(3):
            for c in range(3):
                color = rotated_tokens[r][c]
                clicked = rotated_clicked[r][c]
                circle = quad['circles'][r][c]
                circle.config(bg=color if color else '#98FB98')
                circle.token_color = color
                circle.clicked = clicked
        
        self.hide_rotation_buttons()

        self.current_player = 1 if self.current_player == 2 else 2
        self.player_turn_label.config(text=f"Player {self.current_player}'s Turn")
        
       
        if self.current_player == 2:
            self.root.after(100, self.cpu_move)

    def check_winner(self):
        def has_five_in_a_row(tokens):
            count = 0
            last_token = None
            for token in tokens:
                if token == last_token and token is not None:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 1
                    last_token = token
            return False

        def check_rows():
            for row in range(6):
                row_tokens = []
                for col in range(6):
                    quad_row = row // 3
                    quad_col = col // 3
                    r = row % 3
                    c = col % 3
                    row_tokens.append(self.quadrants[quad_row][quad_col]['circles'][r][c].token_color)
                if has_five_in_a_row(row_tokens):
                    return True
            return False

        def check_columns():
            for col in range(6):
                col_tokens = []
                for row in range(6):
                    quad_row = row // 3
                    quad_col = col // 3
                    r = row % 3
                    c = col % 3
                    col_tokens.append(self.quadrants[quad_row][quad_col]['circles'][r][c].token_color)
                if has_five_in_a_row(col_tokens):
                    return True
            return False

        def check_diagonals():
            for start in range(-2, 3):
                diag_tokens_lr = []
                diag_tokens_rl = []
                for offset in range(6):
                    if 0 <= start + offset < 6:
                        quad_row = (start + offset) // 3
                        quad_col = offset // 3
                        r = (start + offset) % 3
                        c = offset % 3
                        diag_tokens_lr.append(self.quadrants[quad_row][quad_col]['circles'][r][c].token_color)

                        quad_row = (start + offset) // 3
                        quad_col = (5 - offset) // 3
                        r = (start + offset) % 3
                        c = (5 - offset) % 3
                        diag_tokens_rl.append(self.quadrants[quad_row][quad_col]['circles'][r][c].token_color)
                        
                if has_five_in_a_row(diag_tokens_lr) or has_five_in_a_row(diag_tokens_rl):
                    return True
            return False

        return check_rows() or check_columns() or check_diagonals()

    def hover_effect(self, circle):
        if not circle.clicked:
            circle.config(bg='#87CEEB')

    def leave_effect(self, circle):
        if not circle.clicked:
            circle.config(bg='#98FB98')

    def reset_board(self):
        for row in range(2):
            for col in range(2):
                quad = self.quadrants[row][col]
                for r in range(3):
                    for c in range(3):
                        circle = quad['circles'][r][c]
                        circle.config(bg='#98FB98')
                        circle.clicked = False
                        circle.token_color = None
        self.hide_rotation_buttons()
        self.current_player = 1
        self.player_turn_label.config(text="Player 1's Turn")
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = BoardGame(root)
    root.mainloop()
