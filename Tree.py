import logic
import Piece
from math import inf


class Node:
    def __init__(self, depth, max_depth, player, figures, positions, index, previous_move):
        self.depth = depth
        self.player = player
        self.index = index
        # if self.player == 1:
        #     self.value = inf
        # else:
        #     self.value = -inf
        self.best_child = 0
        self.previous_move = previous_move
        self.children = []

        if self.depth < max_depth:
            if len(positions) > 0:
                child_index = 0
                if len(figures[positions[0][0]][positions[0][1]].capturing_possibilities(figures)) > 0:
                    for position in positions:
                        for capture in figures[position[0]][position[1]].capturing_possibilities(figures):
                            new_figures = logic.simulate_capture(position[0], position[1],
                                                                 capture[0], capture[1],
                                                                 figures, player)[0]
                            new_positions = logic.capturing_figures(new_figures, -player)
                            if len(new_positions) == 0:
                                new_positions = logic.moving_figures(new_figures, -player)
                            self.children.append(Node(depth=depth + 1,
                                                      max_depth=max_depth,
                                                      player=-player,
                                                      figures=new_figures,
                                                      positions=new_positions,
                                                      index=child_index,
                                                      previous_move=Move(if_capture=True,
                                                                         x_start=position[0],
                                                                         y_start=position[1],
                                                                         x_target=capture[0],
                                                                         y_target=capture[1])
                                                      ))
                            child_index += 1
                else:
                    for position in positions:
                        for move in figures[position[0]][position[1]].possibilities(figures):
                            new_figures = logic.simulate_move(position[0], position[1],
                                                              move[0], move[1],
                                                              figures, player)
                            # for i in range(8):
                            #     print(f'{figures[i][0].colour} {figures[i][1].colour} {figures[i][2].colour} '
                            #           f'{figures[i][3].colour} {figures[i][4].colour} {figures[i][5].colour} '
                            #           f'{figures[i][6].colour} {figures[i][7].colour} ')
                            new_positions = logic.capturing_figures(new_figures, -player)
                            if len(new_positions) == 0:
                                new_positions = logic.moving_figures(new_figures, -player)
                            self.children.append(Node(depth=depth + 1,
                                                      max_depth=max_depth,
                                                      player=-player,
                                                      figures=new_figures,
                                                      positions=new_positions,
                                                      index=child_index,
                                                      previous_move=Move(if_capture=False,
                                                                         x_start=position[0],
                                                                         y_start=position[1],
                                                                         x_target=move[0],
                                                                         y_target=move[1])
                                                      ))
                            child_index += 1
                if self.player == 1:
                    self.value = self.children[0].value
                    for child in self.children:
                        if child.value > self.value:
                            self.value = child.value
                            self.best_child = child.index
                if self.player == -1:
                    self.value = self.children[0].value
                    for child in self.children:
                        if child.value < self.value:
                            self.value = child.value
                            self.best_child = child.index
        else:
            self.value = logic.evaluation(figures)


class Move:
    def __init__(self, if_capture, x_start, y_start, x_target, y_target):
        self.if_capture = if_capture
        self.x_start = x_start
        self.y_start = y_start
        self.x_target = x_target
        self.y_target = y_target
