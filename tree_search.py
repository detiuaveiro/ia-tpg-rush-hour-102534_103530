"""
Authors:
Rafael Gonçalves (102534)
André Butuc (103530)
"""

from time import time
import heapq
from auxiliary_functions import moveCursor

class Matrix:
    def __init__(self, grid, action=[], parent=None, cost=0, heuristic=0, cursor=[3, 3]):
        if " " in grid:
            self.grid = grid.split(" ")[1]
        else:
            self.grid = grid
        self.n = int(len(grid)**(1/2))
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.cursor = cursor
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

    def __lt__(self, other):
        return self.heuristic + self.cost < other.heuristic + other.cost

class MatrixForGreedy(Matrix):
    counter = 0

    def __init__(self, grid, action=[], parent=None, cost=0, heuristic=0, cursor=[3, 3], idx=0):
        super().__init__(grid, action, parent, cost, heuristic, cursor)
        MatrixForGreedy.counter += 1
        self.idx = MatrixForGreedy.counter

    def __lt__(self, other):
        return (self.heuristic, self.idx) < (other.heuristic, other.idx)

class AI:
    def copy(grid):
        return (grid + " ")[:-1]

    def replace_char(s, index, newchar):
        return s[:index] + newchar + s[index+1:]

    def cost(state: Matrix, action):
        return 1

    def heuristic(state: Matrix):
        _, maxx, miny, _ = state.pieces["A"]
        return sum(1 for x in range(maxx+1, state.n) if state.get(x, miny) != "o")

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
        self.total_costs = {root.grid: 0}
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

    def search2(self):
        while self.open_nodes != []:
            node = heapq.heappop(self.open_nodes)
            # node = self.open_nodes.pop(0)
            if AI.goal_test(node):
                self.solution = node
                return node.path
            lnewnodes = []
            for a in AI.actions(node):
                newgrid, bounds = AI.result(node, a)
                new_cost = node.cost + AI.cost(node, a)
                new_heuristic = AI.heuristic(node)
                newf = new_cost + new_heuristic
                if newgrid in self.grids_visited:
                    if newf >= self.total_costs[newgrid]:
                        continue
                else:
                    self.grids_visited.add(newgrid)
                newnode = MatrixForGreedy(newgrid, [a], node, new_cost, new_heuristic)
                newnode.set_bounds(a[0], bounds)
                # lnewnodes.append(newnode)
                heapq.heappush(self.open_nodes, newnode)
                self.total_costs[newgrid] = newf
            # self.add_to_open(lnewnodes)
        return None
    
    def search3(self):
        while self.open_nodes != []:
            node = heapq.heappop(self.open_nodes)
            if AI.goal_test(node):
                self.solution = node
                return node.path
            # lnewnodes = []
            for a in AI.actions(node):
                newgrid, bounds = AI.result(node, a)
                path, cursorx, cursory = moveCursor(node.cursor, node.pieces[a[0]])
                new_cost = node.cost + len(path) + 1

                if newgrid in self.grids_visited:
                    if new_cost >= self.total_costs[newgrid]:
                        continue
                else:
                    self.grids_visited.add(newgrid)
                newnode = Matrix(newgrid, [a], node, new_cost, cursor=[cursorx, cursory])
                newnode.set_bounds(a[0], bounds)
                # lnewnodes.append(newnode)
                self.total_costs[newgrid] = new_cost
                heapq.heappush(self.open_nodes, newnode)
            # self.add_to_open(lnewnodes)
        return None
    
    def search4(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if AI.goal_test(node):
                self.solution = node
                return node.path
            lnewnodes = []
            for a in AI.actions(node):
                newgrid, bounds = AI.result(node, a)
                path, cursorx, cursory = moveCursor(node.cursor, node.pieces[a[0]])
                new_cost = node.cost + len(path) + 1
                new_heuristic = AI.heuristic(node)
                newf = new_cost + new_heuristic
                if newgrid in self.grids_visited:
                    if newf >= self.total_costs[newgrid]:
                        continue
                else:
                    self.grids_visited.add(newgrid)

                newnode = Matrix(newgrid, [a], node, new_cost, new_heuristic, [cursorx, cursory])
                newnode.set_bounds(a[0], bounds)
                lnewnodes.append(newnode)
                self.total_costs[newgrid] = newf
            self.add_to_open(lnewnodes)
        return None

    def add_to_open(self, lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.cost + x.heuristic)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.heuristic)
        elif self.strategy == 'uniform':
            pass

def main():
    if False: # alternar entre breadth e a*
        with open("levels2.txt", "r") as f:
            levels = f.readlines()
            total_time = 0.0
            total_moves = 0
            for level in levels:
                matrix = Matrix(level)
                t = SearchTree(matrix, "breadth")
                start = time()
                result = t.search()
                total_time += time() - start
                total_moves += len(result)
                # print("{:4f} segundos, {} movimentações".format(time() - start, len(result)))
            print("{:4f} segundos, {} movimentações".format(total_time, total_moves))
    else:
        with open("levels2.txt", "r") as f:
            if True:
                levels = f.readlines()
                total_time = 0.0
                total_moves = 0
                for i, level in enumerate(levels):
                    matrix = Matrix(level)
                    if matrix.n > 6:
                        matrix = MatrixForGreedy(level)
                        t = SearchTree(matrix, "greedy")
                        start = time()
                        result = t.search2()
                        total_time += time() - start
                    else:
                        t = SearchTree(matrix, "uniform")
                        start = time()
                        result = t.search3()
                        total_time += time() - start
                        
                    total_moves += len(result)
                    #print("level: {}, {:4f} segundos, {} movimentações".format(i, time() - start, len(result)))
                print("{:4f} segundos, {} movimentações".format(total_time, total_moves))
            elif True:
                levels = f.readlines()
                total_time = 0.0
                total_moves = 0
                for i, level in enumerate(levels):
                    matrix = Matrix(level)
                    t = SearchTree(matrix, "a*")
                    start = time()
                    result = t.search4()
                    total_time += time() - start
                    total_moves += len(result)
                    print("level: {}, {:4f} segundos, {} movimentações".format(i, time() - start, len(result)))
                print("{:4f} segundos, {} movimentações".format(total_time, total_moves))


if __name__ == "__main__":
    main()