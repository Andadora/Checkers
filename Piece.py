from PIL import Image


class Man:
    def __init__(self, colour, x, y):
        self.colour = colour
        self.position = [x, y]
        if colour == -1:
            self.icon = Image.open('dark_man.png')
        elif colour == 1:
            self.icon = Image.open('light_man.png')
        self.name = 'man'

    def possibilities(self, figures):
        possibilities = self.capturing_possibilities(figures)
        x = self.position[0]
        y = self.position[1]
        if len(possibilities) == 0:
            if figures[x][y].colour == 1:
                if x > 0 and y > 0:
                    if figures[x - 1][y - 1].colour == 0:
                        possibilities.append((x-1, y-1))
                if x > 0 and y < 7:
                    if figures[x - 1][y + 1].colour == 0:
                        possibilities.append((x-1, y+1))
            if figures[x][y].colour == -1:
                if x < 7 and y > 0:
                    if figures[x + 1][y - 1].colour == 0:
                        possibilities.append((x+1, y-1))
                if x < 7 and y < 7:
                    if figures[x + 1][y + 1].colour == 0:
                        possibilities.append((x+1, y+1))
        return possibilities

    def capturing_possibilities(self, figures):
        capturing_possibilities = []
        x = self.position[0]
        y = self.position[1]
        if x > 1 and y > 1:
            if figures[x - 1][y - 1].colour == -figures[x][y].colour:
                if figures[x - 2][y - 2].colour == 0:
                    capturing_possibilities.append((x-2, y-2))
        if x > 1 and y < 6:
            if figures[x - 1][y + 1].colour == -figures[x][y].colour:
                if figures[x - 2][y + 2].colour == 0:
                    capturing_possibilities.append((x-2, y+2))
        if x < 6 and y > 1:
            if figures[x + 1][y - 1].colour == -figures[x][y].colour:
                if figures[x + 2][y - 2].colour == 0:
                    capturing_possibilities.append((x+2, y-2))
        if x < 6 and y < 6:
            if figures[x + 1][y + 1].colour == -figures[x][y].colour:
                if figures[x + 2][y + 2].colour == 0:
                    capturing_possibilities.append((x+2, y+2))
        return capturing_possibilities


class Dame:
    def __init__(self, colour, x, y):
        self.colour = colour
        self.position = [x, y]
        if colour == -1:
            self.icon = Image.open('dark_dame.png')
        elif colour == 1:
            self.icon = Image.open('light_dame.png')
        self.name = 'dame'

    def possibilities(self, figures):
        possibilities = self.capturing_possibilities(figures)
        x = self.position[0]
        y = self.position[1]
        if len(possibilities) == 0:
            x_target = x - 1
            y_target = y - 1
            while x_target >= 0 and y_target >= 0:
                if figures[x_target][y_target].colour == figures[x][y].colour:
                    x_target = -1
                    y_target = -1
                elif figures[x_target][y_target].colour == 0:
                    possibilities.append((x_target, y_target))
                    x_target -= 1
                    y_target -= 1
                elif figures[x_target][y_target].colour == -figures[x][y].colour:
                    x_target = -1
                    y_target = -1

            x_target = x - 1
            y_target = y + 1
            while x_target >= 0 and y_target <= 7:
                if figures[x_target][y_target].colour == figures[x][y].colour:
                    x_target = -1
                    y_target = 8
                elif figures[x_target][y_target].colour == 0:
                    possibilities.append((x_target, y_target))
                    x_target -= 1
                    y_target += 1
                elif figures[x_target][y_target].colour == -figures[x][y].colour:
                    x_target = -1
                    y_target = 8

            x_target = x + 1
            y_target = y - 1
            while x_target <= 7 and y_target >= 0:
                if figures[x_target][y_target].colour == figures[x][y].colour:
                    x_target = 8
                    y_target = -1
                elif figures[x_target][y_target].colour == 0:
                    possibilities.append((x_target, y_target))
                    x_target += 1
                    y_target -= 1
                elif figures[x_target][y_target].colour == -figures[x][y].colour:
                    x_target = 8
                    y_target = -1

            x_target = x + 1
            y_target = y + 1
            while x_target <= 7 and y_target <= 7:
                if figures[x_target][y_target].colour == figures[x][y].colour:
                    x_target = 8
                    y_target = 8
                elif figures[x_target][y_target].colour == 0:
                    possibilities.append((x_target, y_target))
                    x_target += 1
                    y_target += 1
                elif figures[x_target][y_target].colour == -figures[x][y].colour:
                    x_target = 8
                    y_target = 8

        return possibilities

    def capturing_possibilities(self, figures):
        capturing_possibilities = []
        x = self.position[0]
        y = self.position[1]

        x_target = x-1
        y_target = y-1
        intruder = False
        while x_target >= 0 and y_target >= 0:
            if figures[x_target][y_target].colour == figures[x][y].colour:
                x_target = -1
                y_target = -1
            elif figures[x_target][y_target].colour == 0:
                if intruder:
                    capturing_possibilities.append((x_target, y_target))
                x_target -= 1
                y_target -= 1
            elif figures[x_target][y_target].colour == -figures[x][y].colour:
                if intruder:
                    x_target = -1
                    y_target = -1
                else:
                    intruder = True
                    x_target -= 1
                    y_target -= 1

        x_target = x - 1
        y_target = y + 1
        intruder = False
        while x_target >= 0 and y_target <= 7:
            if figures[x_target][y_target].colour == figures[x][y].colour:
                x_target = -1
                y_target = 8
            elif figures[x_target][y_target].colour == 0:
                if intruder:
                    capturing_possibilities.append((x_target, y_target))
                x_target -= 1
                y_target += 1
            elif figures[x_target][y_target].colour == -figures[x][y].colour:
                if intruder:
                    x_target = -1
                    y_target = 8
                else:
                    intruder = True
                    x_target -= 1
                    y_target += 1

        x_target = x + 1
        y_target = y - 1
        intruder = False
        while x_target <= 7 and y_target >= 0:
            if figures[x_target][y_target].colour == figures[x][y].colour:
                x_target = 8
                y_target = -1
            elif figures[x_target][y_target].colour == 0:
                if intruder:
                    capturing_possibilities.append((x_target, y_target))
                x_target += 1
                y_target -= 1
            elif figures[x_target][y_target].colour == -figures[x][y].colour:
                if intruder:
                    x_target = 8
                    y_target = -1
                else:
                    intruder = True
                    x_target += 1
                    y_target -= 1

        x_target = x + 1
        y_target = y + 1
        intruder = False
        while x_target <= 7 and y_target <= 7:
            if figures[x_target][y_target].colour == figures[x][y].colour:
                x_target = 8
                y_target = 8
            elif figures[x_target][y_target].colour == 0:
                if intruder:
                    capturing_possibilities.append((x_target, y_target))
                x_target += 1
                y_target += 1
            elif figures[x_target][y_target].colour == -figures[x][y].colour:
                if intruder:
                    x_target = 8
                    y_target = 8
                else:
                    intruder = True
                    x_target += 1
                    y_target += 1
        return capturing_possibilities


class NotPiece:
    def __init__(self, colour, x, y):
        self.colour = colour
        self.position = [x, y]
        self.icon = Image.open('none.png')
        self.name = 'none'
