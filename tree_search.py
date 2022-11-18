"""
Authors:
Rafael Gonçalves (102534)
André Butuc (103530)
"""

from time import time

class Matrix:
    def __init__(self, grid, action=[], parent=None):
        if " " in grid:
            self.grid = grid.split(" ")[1]
        else:
            self.grid = grid
        self.n = int(len(grid)**(1/2))
        self.parent = parent
        # Flyweight pattern
        if parent is not None:
            self.pieces = parent.pieces.copy() #copy by value
            self.horizontal_pieces = parent.horizontal_pieces #copy by reference
            self.vertical_pieces = parent.vertical_pieces #copy by reference
            self.path = parent.path + action
            return
        self.pieces = {}
        self.horizontal_pieces = []
        self.vertical_pieces = []
        self.path = action
        for x in range(self.n):
            for y in range(self.n):
                idx = y*self.n+x
                char = self.grid[idx]
                if char in self.pieces:
                    minx, maxx, miny, maxy = self.pieces[char]
                    self.pieces[char] = (min(minx, x), max(maxx, x), min(miny, y), max(maxy, y))
                else:
                    if char not in ["o", "x"]:
                        self.pieces[char] = (x, x, y, y)
                        if x < self.n-1:
                            next_by_x = self.grid[idx + 1]
                            if next_by_x == char:
                                self.horizontal_pieces.append(char)
                                continue    
                        self.vertical_pieces.append(char)

    def get(self, x, y):
        return self.grid[y*self.n+x]

    def set_bounds(self, piece, bounds):
        self.pieces[piece] = bounds

    def set_specific_bound(self, piece, bound, value):
        if bound == "minx":
            self.pieces[piece][0] = value
        elif bound == "maxx":
            self.pieces[piece][1] = value
        elif bound == "miny":
            self.pieces[piece][2] = value
        elif bound == "maxy":
            self.pieces[piece][3] = value

    def is_horizontal(self, piece):
        return piece in self.horizontal_pieces

    def is_vertical(self, piece):
        return piece in self.vertical_pieces

    def __repr__(self):
        output = ""
        for y in range(self.n):
            for x in range(self.n):
                output += self.grid[y*self.n+x] + " "
            output += "\n"
        return output


class AI:
    def copy(grid):
        return (grid + " ")[:-1]

    def replace_char(s, index, newchar):
        return s[:index] + newchar + s[index+1:]

    def actions(state: Matrix):
        actions = []
        for char, bounds in state.pieces.items():
            minx, maxx, miny, maxy = bounds
            if state.is_horizontal(char):
                if minx > 0 and state.get(minx-1, miny) == "o": # miny = maxy
                    actions.append((char, "a"))
                if maxx < state.n-1 and state.get(maxx+1, miny) == "o": # miny = maxy
                    actions.append((char, "d"))
            if state.is_vertical(char):
                if miny > 0 and state.get(minx, miny-1) == "o": # minx = maxx
                    actions.append((char, "w"))
                if maxy < state.n-1 and state.get(minx, maxy+1) == "o": # minx = maxx
                    actions.append((char, "s"))
        return actions

    def result(state: Matrix, action):
        char, direction = action
        (minx, maxx, miny, maxy) = state.pieces[char]
        newgrid = AI.copy(state.grid)
        n = state.n
        if direction == "a":
            newgrid = AI.replace_char(newgrid, miny*n+maxx, "o") # miny = maxy
            newgrid = AI.replace_char(newgrid, miny*n+minx-1, char) # miny = maxy
            minx -= 1
            maxx -= 1
        elif direction == "d":
            newgrid = AI.replace_char(newgrid, miny*n+minx, "o") # miny = maxy
            newgrid = AI.replace_char(newgrid, miny*n+maxx+1, char) # miny = maxy
            minx += 1
            maxx += 1
        elif direction == "w":
            newgrid = AI.replace_char(newgrid, maxy*n+minx, "o") # minx = maxx
            newgrid = AI.replace_char(newgrid, (miny-1)*n+minx, char) # minx = maxx
            miny -= 1
            maxy -= 1
        elif direction == "s":
            newgrid = AI.replace_char(newgrid, miny*n+minx, "o") # minx = maxx
            newgrid = AI.replace_char(newgrid, (maxy+1)*n+minx, char) # minx = maxx
            miny += 1
            maxy += 1
        bounds = (minx, maxx, miny, maxy)
        return newgrid, bounds

    def goal_test(state: Matrix):
        return state.pieces["A"][1] == state.n-1 # maxx de A == n-1


class SearchTree:
    def __init__(self, root: Matrix, strategy='breadth'):
        self.root = root
        self.open_nodes = [root]
        self.grids_visited = {root.grid}
        self.strategy = strategy
        self.solution = None

    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if AI.goal_test(node):
                self.solution = node
                return node.path
            lnewnodes = []
            for a in AI.actions(node):
                newgrid, bounds = AI.result(node, a)
                if newgrid not in self.grids_visited:
                    newnode = Matrix(newgrid, [a], node)
                    newnode.set_bounds(a[0], bounds)
                    lnewnodes.append(newnode)
                    self.grids_visited.add(newgrid)
            self.add_to_open(lnewnodes)
        return None

    def add_to_open(self, lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes

def main():
    with open("levels.txt", "r") as f:
        levels = f.readlines()
        total_time = 0.0
        for i in range(57):
            matrix = Matrix(levels[i])
            t = SearchTree(matrix, "breadth")
            start = time()
            result = t.search()
            total_time += time() - start
            #print("{:4f} segundos, {} movimentações".format(time() - start, len(result)))
        print("{:4f} segundos".format(total_time))

if __name__ == "__main__":
    main()
