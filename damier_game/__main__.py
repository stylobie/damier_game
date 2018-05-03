import tkinter as tk
from .damier import Damier
from .board_ui import BoardUI

def display():
    root = tk.Tk()
    root.title("Dames")

    gui = BoardUI(root)
    gui.pack(side="top", fill="both", expand="true",
             padx=gui.pad, pady=gui.pad)
    gui.board.nouveauJeu()
    # root.resizable(0,0)
    root.mainloop()

display()
