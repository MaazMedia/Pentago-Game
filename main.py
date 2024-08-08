import tkinter as tk
from tkinter import messagebox
from player import BoardGame as Player  # Assuming the game logic code is saved as board_game.py
from ai import BoardGame as AI
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Select Game Mode")
        self.root.configure(bg='#2e2e2e')

        self.title_label = tk.Label(self.root, text="Select Game Mode", font=('Helvetica', 20), bg='#2e2e2e', fg='#ffffff')
        self.title_label.pack(pady=20)

        self.pvp_button = tk.Button(self.root, text="Player vs Player", font=('Helvetica', 16), command=self.start_pvp, bg='#8B0000', fg='#ffffff')
        self.pvp_button.pack(pady=10, padx=20)

        self.pvc_button = tk.Button(self.root, text="Player vs CPU", font=('Helvetica', 16), command=self.start_pvc, bg='#8B0000', fg='#ffffff')
        self.pvc_button.pack(pady=10, padx=20)

    def start_pvp(self):
        self.root.destroy()  # Close the mode selection window
        root = tk.Tk()
        game = Player(root)
        root.mainloop()

    def start_pvc(self):
        self.root.destroy()  # Close the mode selection window
        root = tk.Tk()
        game = AI(root)
        root.mainloop()
    


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
