import Piece
import copy
from math import inf


def capturing_figures(figures, player):
    capturing_figures_list = []
    for x in range(8):
        for y in range(8):
            if figures[x][y].colour == player:
                if len(figures[x][y].capturing_possibilities(figures)) > 0:
                    capturing_figures_list.append((x, y))
    return capturing_figures_list


# def capturing_count(figures, player, counter=0):
#     figures_copy = [[] for i in range(8)]
#     for x in range(8):
#         for y in range(8):
#             figures_copy[x].append(copy.copy(figures[x][y]))
#
#     for x in range(8):
#         for y in range(8):
#             if figures_copy[x][y].colour == player:
#                 for capture in figures_copy[x][y].capturing_possibilities(figures):
#                     counter++


def moving_figures(figures, player):
    moving_figures_list = []
    for x in range(8):
        for y in range(8):
            if figures[x][y].colour == player:
                if len(figures[x][y].possibilities(figures)) > 0:
                    moving_figures_list.append((x, y))
    return moving_figures_list


def evaluation(figures):
    value = 0
    for x in range(8):
        for y in range(8):
            if figures[x][y].name == 'man':
                value += 5 * figures[x][y].colour
            if figures[x][y].name == 'dame':
                value += 50 * figures[x][y].colour

            if x == 0 or x == 7 or y == 0 or y == 7:
                value += 2 * figures[x][y].colour
            elif x == 1 or x == 6 or y == 1 or y == 6:
                value += figures[x][y].colour

            if figures[x][y].name == 'man':
                if figures[x][y].colour == -1 and 1 < x < 4:
                    value += -1
                if figures[x][y].colour == -1 and 3 < x < 6:
                    value += -3
                if figures[x][y].colour == -1 and x > 5:
                    value += -20
                if figures[x][y].colour == 1 and x < 2:
                    value += 20
                if figures[x][y].colour == 1 and 1 < x < 4:
                    value += 3
                if figures[x][y].colour == 1 and 3 < x < 6:
                    value += 1
            for i in capturing_figures(figures, -1):
                value += -30
            for i in capturing_figures(figures, 1):
                value += 30
    return value


def simulate_move(x_start, y_start, x_target, y_target, figures, player):
    figures_copy = [[] for i in range(8)]
    for x in range(8):
        for y in range(8):
            figures_copy[x].append(copy.copy(figures[x][y]))

    if figures_copy[x_start][y_start].name == 'man':
        figures_copy[x_target][y_target] = Piece.Man(player, x_target, y_target)
    elif figures_copy[x_start][y_start].name == 'dame':
        figures_copy[x_target][y_target] = Piece.Dame(player, x_target, y_target)

    figures_copy[x_start][y_start] = Piece.NotPiece(0, x_start, y_start)

    # convert to dame?
    if (player == 1 and x_target == 0) or (player == -1 and x_target == 7):
        figures_copy[x_target][y_target] = Piece.Dame(player, x_target, y_target)
    return figures_copy


def simulate_capture(x_start, y_start, x_target, y_target, figures, player):
    figures_copy = [[] for i in range(8)]
    for x in range(8):
        for y in range(8):
            figures_copy[x].append(copy.copy(figures[x][y]))

    if figures_copy[x_start][y_start].name == 'man':
        figures_copy[x_target][y_target] = Piece.Man(player, x_target, y_target)
    elif figures_copy[x_start][y_start].name == 'dame':
        figures_copy[x_target][y_target] = Piece.Dame(player, x_target, y_target)

    for i in range(abs(x_target - x_start)):
        x_captured = int(x_start + i * (x_target - x_start) / abs(x_target - x_start))
        y_captured = int(y_start + i * (y_target - y_start) / abs(y_target - y_start))
        figures_copy[x_captured][y_captured] = Piece.NotPiece(0, x_captured, y_captured)

    value = evaluation(figures_copy)
    temp_value = -inf*player
    temp_figures = figures_copy

    if len(figures_copy[x_target][y_target].capturing_possibilities(figures_copy)) > 0:
        for possibility in figures_copy[x_target][y_target].capturing_possibilities(figures_copy):
            ev = simulate_capture(x_target, y_target, possibility[0], possibility[1], figures_copy, player)[1]
            if ev < temp_value and player == -1:
                temp_value = ev
                temp_figures = simulate_capture(x_target, y_target, possibility[0], possibility[1], figures_copy, player)[0]
            if ev > temp_value and player == 1:
                temp_value = ev
                temp_figures = simulate_capture(x_target, y_target, possibility[0], possibility[1], figures_copy, player)[0]
        figures_copy = temp_figures
    else:
        if (player == 1 and x_target == 0) or (player == -1 and x_target == 7):
            figures_copy[x_target][y_target] = Piece.Dame(player, x_target, y_target)
    if temp_value != inf and temp_value != -inf:
        value = temp_value
    return figures_copy, value
