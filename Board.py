import tkinter as tk
import logic
import Tree
from functools import partial
from math import inf
import time

from PIL import ImageTk

import Piece

LIGHT = 'white'
DARK = 'black'
MAX_DEPTH = 4
WIDTH = 8 * 64
HEIGHT = 8 * 64
SQUARE_WIDTH = 64
SQUARE_HEIGHT = 64


class Board:
    def __init__(self):
        self.player = 1
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=HEIGHT, width=WIDTH)
        self.canvas.pack()
        self.figures = []
        self.buttons = []
        self.images = []
        for x in range(8):
            self.figures.append([])
            self.buttons.append([])
            self.images.append([])

        for x in range(8):
            for y in range(8):
                if (x + y) % 2 == 0:  # jasne pole
                    colour = LIGHT
                    state = tk.DISABLED
                    piece = Piece.NotPiece(0, x, y)
                else:  # ciemne pole
                    colour = DARK
                    if x < 3:
                        state = tk.DISABLED
                        piece = Piece.Man(-1, x, y)
                    elif x > 4:
                        if x == 5:
                            state = tk.NORMAL
                        else:
                            state = tk.DISABLED
                        piece = Piece.Man(1, x, y)
                    else:
                        state = tk.DISABLED
                        piece = Piece.NotPiece(0, x, y)
                self.figures[x].append(piece)
                self.images[x].append(ImageTk.PhotoImage(image=self.figures[x][y].icon))
                self.buttons[x].append(tk.Button(self.canvas,
                                                 image=self.images[x][y],
                                                 bg=colour,
                                                 width=SQUARE_WIDTH,
                                                 height=SQUARE_HEIGHT,
                                                 state=state,
                                                 command=partial(self.choice, x, y)
                                                 ))
                self.buttons[x][y].grid(row=x, column=y)
        self.root.mainloop()

    def enable_player(self, player):
        capturing = False
        for i in range(8):
            for j in range(8):
                self.buttons[i][j].configure(state=tk.DISABLED)
        for position in logic.capturing_figures(self.figures, player):
            self.buttons[position[0]][position[1]].configure(
                state=tk.NORMAL,
                command=partial(self.choice, position[0], position[1])
            )
            capturing = True
        if not capturing:
            for position in logic.moving_figures(self.figures, player):
                self.buttons[position[0]][position[1]].configure(
                    state=tk.NORMAL,
                    command=partial(self.choice, position[0], position[1])
                )

    def choice(self, x, y):
        self.enable_player(self.player)
        # print(self.figures[x][y].possibilities(self.figures, self.player))
        # for i in range(8):
        #     print(f'{self.figures[i][0].colour} {self.figures[i][1].colour} {self.figures[i][2].colour} '
        #           f'{self.figures[i][3].colour} {self.figures[i][4].colour} {self.figures[i][5].colour} '
        #           f'{self.figures[i][6].colour} {self.figures[i][7].colour} ')
        capturing = False
        for capturing_possibility in self.figures[x][y].capturing_possibilities(self.figures):
            self.buttons[capturing_possibility[0]][capturing_possibility[1]].configure(
                state=tk.NORMAL,
                command=partial(self.capture, x, y, capturing_possibility[0], capturing_possibility[1])
            )
            capturing = True
        if not capturing:
            for possibility in self.figures[x][y].possibilities(self.figures):
                self.buttons[possibility[0]][possibility[1]].configure(
                    state=tk.NORMAL,
                    command=partial(self.move, x, y, possibility[0], possibility[1])
                )

    def convert_to_dame(self, x, y):
        self.figures[x][y] = Piece.Dame(self.figures[x][y].colour, x, y)
        self.images[x][y] = ImageTk.PhotoImage(image=self.figures[x][y].icon)
        self.buttons[x][y].configure(image=self.images[x][y])

    def move(self, x_start, y_start, x_target, y_target):
        if self.figures[x_start][y_start].name == 'man':
            self.figures[x_target][y_target] = Piece.Man(self.player, x_target, y_target)
        elif self.figures[x_start][y_start].name == 'dame':
            self.figures[x_target][y_target] = Piece.Dame(self.player, x_target, y_target)
        self.images[x_target][y_target] = ImageTk.PhotoImage(image=self.figures[x_target][y_target].icon)
        self.buttons[x_target][y_target].configure(image=self.images[x_target][y_target])

        self.figures[x_start][y_start] = Piece.NotPiece(0, x_start, y_start)
        self.images[x_start][y_start] = ImageTk.PhotoImage(image=self.figures[x_start][y_start].icon)
        self.buttons[x_start][y_start].configure(image=self.images[x_start][y_start])

        # convert to dame?
        if (self.player == 1 and x_target == 0) or (self.player == -1 and x_target == 7):
            self.convert_to_dame(x_target, y_target)

        self.dark_turn()
        self.enable_player(self.player)

    def dark_move(self, x_start, y_start, x_target, y_target):
        if self.figures[x_start][y_start].name == 'man':
            self.figures[x_target][y_target] = Piece.Man(-1, x_target, y_target)
        elif self.figures[x_start][y_start].name == 'dame':
            self.figures[x_target][y_target] = Piece.Dame(-1, x_target, y_target)
        self.images[x_target][y_target] = ImageTk.PhotoImage(image=self.figures[x_target][y_target].icon)
        self.buttons[x_target][y_target].configure(image=self.images[x_target][y_target])

        self.figures[x_start][y_start] = Piece.NotPiece(0, x_start, y_start)
        self.images[x_start][y_start] = ImageTk.PhotoImage(image=self.figures[x_start][y_start].icon)
        self.buttons[x_start][y_start].configure(image=self.images[x_start][y_start])

        # convert to dame?
        if x_target == 7:
            self.convert_to_dame(x_target, y_target)

        self.enable_player(1)

    def capture(self, x_start, y_start, x_target, y_target):
        if self.figures[x_start][y_start].name == 'man':
            self.figures[x_target][y_target] = Piece.Man(self.player, x_target, y_target)
        elif self.figures[x_start][y_start].name == 'dame':
            self.figures[x_target][y_target] = Piece.Dame(self.player, x_target, y_target)
        self.images[x_target][y_target] = ImageTk.PhotoImage(image=self.figures[x_target][y_target].icon)
        self.buttons[x_target][y_target].configure(image=self.images[x_target][y_target])

        for i in range(abs(x_target - x_start)):
            x_captured = int(x_start + i * (x_target - x_start) / abs(x_target - x_start))
            y_captured = int(y_start + i * (y_target - y_start) / abs(y_target - y_start))
            self.figures[x_captured][y_captured] = Piece.NotPiece(0, x_captured, y_captured)
            self.images[x_captured][y_captured] = ImageTk.PhotoImage(image=self.figures[x_captured][y_captured].icon)
            self.buttons[x_captured][y_captured].configure(image=self.images[x_captured][y_captured])

        if len(self.figures[x_target][y_target].capturing_possibilities(self.figures)) > 0:
            for i in range(8):
                for j in range(8):
                    self.buttons[i][j].configure(state=tk.DISABLED)
            self.buttons[x_target][y_target].configure(
                state=tk.NORMAL,
                command=partial(self.choice, x_target, y_target)
            )
            for possibility in self.figures[x_target][y_target].capturing_possibilities(self.figures):
                self.buttons[possibility[0]][possibility[1]].configure(
                    state=tk.NORMAL,
                    command=partial(self.capture, x_target, y_target, possibility[0], possibility[1])
                )
        else:
            if (self.player == 1 and x_target == 0) or (self.player == -1 and x_target == 7):
                self.convert_to_dame(x_target, y_target)
            if self.end_of_the_game() != 1:
                self.dark_turn()
                self.enable_player(self.player)

    def dark_capture(self, x_start, y_start, x_target, y_target):
        if self.figures[x_start][y_start].name == 'man':
            self.figures[x_target][y_target] = Piece.Man(-1, x_target, y_target)
        elif self.figures[x_start][y_start].name == 'dame':
            self.figures[x_target][y_target] = Piece.Dame(-1, x_target, y_target)
        self.images[x_target][y_target] = ImageTk.PhotoImage(image=self.figures[x_target][y_target].icon)
        self.buttons[x_target][y_target].configure(image=self.images[x_target][y_target])

        for i in range(abs(x_target - x_start)):
            x_captured = int(x_start + i * (x_target - x_start) / abs(x_target - x_start))
            y_captured = int(y_start + i * (y_target - y_start) / abs(y_target - y_start))
            self.figures[x_captured][y_captured] = Piece.NotPiece(0, x_captured, y_captured)
            self.images[x_captured][y_captured] = ImageTk.PhotoImage(image=self.figures[x_captured][y_captured].icon)
            self.buttons[x_captured][y_captured].configure(image=self.images[x_captured][y_captured])

        value = inf
        figures = self.figures.copy()
        if len(figures[x_target][y_target].capturing_possibilities(figures)) > 0:
            for possibility in figures[x_target][y_target].capturing_possibilities(figures):
                ev = logic.simulate_capture(x_target, y_target, possibility[0], possibility[1], figures, -1)[1]
                if ev < value:
                    value = ev
                    start_position = (x_target, y_target)
                    target_position = (possibility[0], possibility[1])
                    figures = logic.simulate_capture(x_target, y_target, possibility[0], possibility[1], figures, -1)[0]
            self.dark_capture(start_position[0], start_position[1], target_position[0], target_position[1])
        else:
            if x_target == 7:
                self.convert_to_dame(x_target, y_target)

            if self.end_of_the_game() != 1:
                self.enable_player(self.player)

    def end_of_the_game(self):
        black = 0
        white = 0
        for i in range(8):
            for j in range(8):
                if self.figures[i][j].colour == -1:
                    black += self.figures[i][j].colour
                if self.figures[i][j].colour == 1:
                    white += self.figures[i][j].colour
        if black == 0:
            message = tk.Message(text='Wygrałeś!')
            message.pack()
            return 1
        if white == 0:
            message = tk.Message(text='Przegrałeś ;<')
            message.pack()
            return 1

    def dark_turn(self):
        if len(logic.capturing_figures(self.figures, -1)) > 0 or len(logic.moving_figures(self.figures, -1)) > 0:
            if len(logic.capturing_figures(self.figures, -1)) > 0:
                start_node = Tree.Node(depth=0,
                                       max_depth=MAX_DEPTH,
                                       player=-1,
                                       figures=self.figures,
                                       positions=logic.capturing_figures(self.figures, -1),
                                       index=0,
                                       previous_move=Tree.Move(True, 0, 0, 0, 0)
                                       )
            else:
                start_node = Tree.Node(depth=0,
                                       max_depth=MAX_DEPTH,
                                       player=-1,
                                       figures=self.figures,
                                       positions=logic.moving_figures(self.figures, -1),
                                       index=0,
                                       previous_move=Tree.Move(True, 0, 0, 0, 0)
                                       )
            best_move = start_node.children[start_node.best_child].previous_move

            if best_move.if_capture:
                self.dark_capture(x_start=best_move.x_start,
                                  y_start=best_move.y_start,
                                  x_target=best_move.x_target,
                                  y_target=best_move.y_target
                                  )
            else:
                self.dark_move(x_start=best_move.x_start,
                               y_start=best_move.y_start,
                               x_target=best_move.x_target,
                               y_target=best_move.y_target
                               )
        else:
            message = tk.Message(text='Nie mogę się ruszyć, przegrałem')
            message.pack()
