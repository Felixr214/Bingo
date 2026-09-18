import numpy as np
from copy import deepcopy
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import ASCII_ART

class Card:
    def __init__(self, values_, results, winner, moves, id):
        self.id = id
        np.random.seed(id)
        self.winner = winner
        self.all_values = deepcopy(values_)
        self.moves = moves
        np.random.shuffle(self.all_values)
        self.card_values = self.all_values[:25]
        if winner:
            while not self.isWinner(results):
                np.random.shuffle(self.all_values)
                self.card_values = self.all_values[:25]
        else:
            while self.isWinner(results):
                np.random.shuffle(self.all_values)
                self.card_values = self.all_values[:25]

    def isWinner(self, results):
        rows = {}
        columns = {}
        lr_diagonal = 0
        rl_diagonal = 0

        for a in range(5):
            rows[a] = 0
            columns[a] = 0
        i = 0
        matches = []
        for res in results:
            i += 1
            if res not in self.card_values:
                continue
            index = self.card_values.index(res)

            matches.append(int(res))
            row = index // 5
            col = index % 5

            if row == col:
                rl_diagonal += 1
            if 4 - col == row:
                lr_diagonal += 1

            rows[row] += 1
            columns[col] += 1

            if rows[row] == 5 or columns[col] == 5 or lr_diagonal == 5 or rl_diagonal == 5:
                if i != self.moves and self.winner:
                    return False
                if self.winner:
                    print(matches)
                    print(lr_diagonal)
                    print(rl_diagonal)
                    print(rows)
                    print(columns)
                return True

        return False

    def plot(self):
        for a in range(5):
            print(self.card_values[a*5: a*5+5])


    def draw_ascii_border(self, symbol, longest_number, size):
        return str(symbol)*((longest_number*(size+1)+2)*5+1)

    def draw_ascii_empty(self, symbol, longest_number, size):
        line = f"{symbol}" + (" "*longest_number*(1+size) + f" {symbol}")*5
        return line



    def get_longest_number(self):
        l = 0
        for a in range(25):
            l = max(l, len(str(self.card_values[a])))
        return l

    def ascii_draw(self):
        #font = ASCII_ART.hashtags
        font = ASCII_ART.seven_segment
        size = font["size"]
        vertical_symbol = "+"
        horizontal_symbol = "+"
        longest_number = self.get_longest_number()

        grid_size = longest_number * (1+size) + 1 + 6
        print(self.draw_ascii_border(horizontal_symbol, longest_number, size))

        for a in range(5):
            row = self.card_values[a*5: a*5+5]
            print(self.draw_ascii_empty(vertical_symbol, longest_number, size))
            for line_ in range(size):
                line = vertical_symbol
                for number in row:
                    offset = (longest_number - len(str(number)))*(size+1)
                    line += " "*int(offset/2)
                    for digit in str(number):
                        line += f" {font[digit].get_line(line_)}"
                    line += " "*int(np.ceil(offset / 2))
                    line += f" {vertical_symbol}"
                assert (longest_number*(size+1)+2)*5+1 == len(line)
                print(line)
            print(self.draw_ascii_empty(vertical_symbol, longest_number, size))
            print(self.draw_ascii_border(horizontal_symbol, longest_number, size))

    def save(self, font_):
        c = canvas.Canvas(f"Karten/Bingokarte_{self.id}.pdf", pagesize=landscape(A4))
        y = 500

        if font_ == "7":
            c.setFont("Courier", 10)
            line_height = 10
            font = ASCII_ART.seven_segment

        else:
            c.setFont("Courier", 6)
            line_height = 6
            font = ASCII_ART.hashtags

        size = font["size"]
        vertical_symbol = "+"
        horizontal_symbol = "+"
        longest_number = self.get_longest_number()

        grid_size = longest_number * (1 + size) + 1 + 6
        i = 0
        c.drawString(10, y - i * line_height, self.draw_ascii_border(horizontal_symbol, longest_number, size))
        i+=1

        for a in range(5):
            row = self.card_values[a * 5: a * 5 + 5]
            c.drawString(10, y - i * line_height, self.draw_ascii_empty(vertical_symbol, longest_number, size))
            i += 1
            for line_ in range(size):
                line = vertical_symbol
                for number in row:
                    offset = (longest_number - len(str(number))) * (size + 1)
                    line += " " * int(offset / 2)
                    for digit in str(number):
                        line += f" {font[digit].get_line(line_)}"
                    line += " " * int(np.ceil(offset / 2))
                    line += f" {vertical_symbol}"
                assert (longest_number * (size + 1) + 2) * 5 + 1 == len(line)
                c.drawString(10, y - i * line_height, line)
                i+=1

            c.drawString(10, y - i * line_height, self.draw_ascii_empty(vertical_symbol, longest_number, size))
            i += 1
            c.drawString(10, y - i * line_height, self.draw_ascii_border(horizontal_symbol, longest_number, size))
            i += 1

        c.save()



