# http://www.neocomputer.org/projects/eller.html
# http://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm

import random

class maze:

    def __init__(self, width):
        self.width = width
        self.row = [0] * width

    def __iter__(self):
        return self

    def fill_down(self):
        for n in range(1, width+1):
            indices = [z[0] for z in enumerate(self.prev) if z[1] == n]
            if len(indices) == 0:
                continue
            # Copy one element down
            # TODO: Copy more than one, only if not adjacent
            i = random.choice(indices)
            self.row[i] = self.prev[i]
        
    def fill_unused(self):
        # Fill in blank cells with unused numbers
        lowest = 1
        for i in range(width):
            if self.row[i] != 0:
                continue
            # Find the lowest unused number
            while lowest in self.row:
                lowest = lowest + 1
            self.row[i] = lowest

    def create_right_walls(self):
        for i in range(width-1):
            if random.random() < 0.5:
                # If the previous row is joined, do not join this one
                if self.prev[i] == self.prev[i+1]:
                    continue
                value = self.row[i]
                oldval = self.row[i+1]
                self.row[i+1] = value
                # Change the previous row too
                for j in range(i+1, width):
                    if self.prev[j] != oldval:
                        break
                    self.prev[j] = value

    def __next__(self):
        self.prev = self.row
        self.row = [0] * width
        self.fill_down()
        #print("".join(f'  { symbols[i] } ' for i in self.row))
        self.fill_unused()
        self.create_right_walls()
        return self.prev, self.row

width = 20
symbols = '!abcdefghijklmnopqrstuvwxyz0123456789'

def format(prev, row):
    for i in range(len(row)):
        yield '|' if i == 0 or row[i-1] != row[i] else ' '
        number = '   ' #f' {symbols[row[i]]} '
        if prev[i] != row[i]:
            number = "".join('\u0305' + c for c in number)
        yield number
    yield '|'

for prev, row in maze(width):
    print("".join(format(prev, row)))
