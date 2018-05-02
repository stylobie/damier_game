import os
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk

from .constants import Couleur, TypePiece
from .board import Board
from .constants import Couleur, Direction
from .position_damier import PositionsDamier


class BoardUI(tk.Frame):
    color1 = "white"
    color2 = "grey"
    pad = 4
    squareSize = 64

    @staticmethod
    def getImgDir():
        fileName = __file__
        return os.path.join(os.path.dirname(fileName), "img")

    @property
    def boardSize(self):
        return 10 * self.squareSize

    def __init__(self, parent, squareSize=72):
        self.photos = {}
        for p in TypePiece.all:
            for c in Couleur.all:
                key = "{}_{}".format(p, c)
                imgFileName = os.path.join(BoardUI.getImgDir(), key + ".png")
                self.photos[key] = ImageTk.PhotoImage(file=imgFileName)
        self.font = tkFont.Font(family='Helvetica', size=8, weight='bold')
        self.squareSize = squareSize
        self.parent = parent
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self, width=self.boardSize + self.pad,
                                height=self.boardSize + self.pad, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        self.board = Board(self)

        self.drawBoard()

        self.canvas.bind("<Button-1>", self.click)

        self.statusbar = tk.Frame(self, height=64)

        self.button_quit = tk.Button(self.statusbar, text="New", fg="black")

        self.button_quit.pack(side=tk.LEFT, in_=self.statusbar)

        self.label_status = tk.Label(
            self.statusbar, text="   White's turn  ", fg="black")

        self.label_status.pack(side=tk.LEFT, expand=0, in_=self.statusbar)

        self.button_quit = tk.Button(
            self.statusbar, text="Quit", fg="black", command=self.parent.destroy)

        self.button_quit.pack(side=tk.RIGHT, in_=self.statusbar)

        self.statusbar.pack(expand=False, fill="x", side='bottom')

    def drawSquares(self):
        self.canvas.delete("square")
        self.canvas.delete("text")
        color = self.color2
        for row in range(self.board.boardSize):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.board.boardSize):
                x1 = (col * self.squareSize) + self.pad
                y1 = (row * self.squareSize) + self.pad
                x2 = x1 + self.squareSize
                y2 = y1 + self.squareSize
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, outline="black", fill=color, tags="square")
                
                position = PositionsDamier.getPositionManoury(row, col)
                if position > 0:
                    text = str(position)
                    self.canvas.create_text(
                        x2 - 6, y2 - 6, text=text, font=self.font, anchor="c", tag="text")

                color = self.color1 if color == self.color2 else self.color2

    def drawPieces(self):
        self.canvas.delete("piece")
        pieces = self.board.pieces
        if pieces is None:
            return
        for p in pieces:
            self.drawPiece(p)

    def drawStart(self):
        self.canvas.delete("start")
        start = self.board.start
        if start is None:
            return
        (ligne, colonne) = PositionsDamier.getCoords(start)
        self.drawSelection(ligne, colonne, "magenta", "start")

    def drawTrace(self):
        self.canvas.delete("trace")
        if self.board.trace is None:
            return
        for trace in self.board.trace:
            (ligne, colonne) = PositionsDamier.getCoords(trace)
            self.drawSelection(ligne, colonne, "black", "trace")

    def drawHints(self):
        self.canvas.delete("hint")
        if(self.board.hints is None):
            return
        for hint in self.board.hints:
            (ligne, colonne) = PositionsDamier.getCoords(hint)
            self.drawSelection(ligne, colonne, "chartreuse", "hint")

    def drawBoard(self, init=True):

        if init:
            self.drawSquares()
        self.drawPieces()
        self.drawStart()
        self.drawTrace()
        self.drawHints()
        self.setOrder()

    def setOrder(self):
        self.canvas.tag_lower("text")
        self.canvas.tag_lower("hint")
        self.canvas.tag_lower("start")
        self.canvas.tag_lower("trace")
        self.canvas.tag_lower("piece")
        self.canvas.tag_lower("square")

    def drawSelection(self, r, c, color, tag):
        x1 = self.pad + c * self.squareSize + 2
        x2 = x1 + self.squareSize - 1 - 3
        y1 = self.pad + r * self.squareSize + 2
        y2 = y1 + self.squareSize - 1 - 3
        self.canvas.create_line(x1, y1, x2, y1, x2, y2,
                                x1, y2, x1, y1, width=3, fill=color, tags=tag)

    def drawPiece(self, p):
        coords = p.coords
        if coords is None:
            return
        (ligne, column) = coords
        photo = self.photos[p.img]
        # photo = self.photos["DAME_" + p.couleur]
        x1 = self.pad + column * self.squareSize + self.squareSize // 2
        y1 = self.pad + ligne * self.squareSize + self.squareSize // 2
        self.canvas.create_image(x1, y1, image=photo, tags="piece", anchor="c")

    def dessinerMessage(self, msg):
        self.label_status.config(text=msg)

    def click(self, event):
        # Figure out which square we've clicked
        col_size = row_size = self.squareSize
        colonne = (event.x-self.pad) // col_size
        ligne = (event.y - self.pad) // row_size
        self.board.click(ligne, colonne)
