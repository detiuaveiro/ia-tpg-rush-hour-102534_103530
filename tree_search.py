class Matrix:
    def __init__(self, grid, action=[], parent=None):
        if " " in grid:
            self.grid = grid.split(" ")[1]
        else:
            self.grid = grid
        self.n = int(len(grid)**(1/2))
        self.parent = parent
        if parent is not None:
            self.pieces = parent.pieces
            self.horizontal_pieces = parent.horizontal_pieces
            self.vertical_pieces = parent.vertical_pieces
            self.path = parent.path + action
            return
        self.pieces = {}
        self.horizontal_pieces = []
        self.vertical_pieces = []
        self.path = action
        if len(self.pieces) != 0:
            return
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

    def get(self, x: int, y: int) -> str:
        return self.grid[y*self.n+x]

    def set_bounds(self, piece: str, bounds: tuple):
        self.pieces[piece] = bounds

    def is_horizontal(self, piece: str) -> bool:
        return piece in self.horizontal_pieces

    def is_vertical(self, piece: str) -> bool:
        return piece in self.vertical_pieces

    def in_parent(self, grid):
        if self.parent == None:
            return False
        if self.parent.grid == grid:
            return True
        return self.parent.in_parent(grid) 

    def __repr__(self) -> str:
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
            if char == "C":
                print(bounds)
                print(state)
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

"""
# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self, state, parent): 
        self.state = state
        self.parent = parent

    def __str__(self):
        return str(self.state)
    
    def __repr__(self):
        return str(self)

    def in_parent(self, state):
        if self.parent == None:
            return False
        if self.parent.state == state:
            return True
        return self.parent.in_parent(state)
"""

class SearchTree:
    def __init__(self, root: Matrix, strategy='breadth'): 
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None

    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            print()
            print("PATH", node.path)
            if AI.goal_test(node):
                self.solution = node
                print(node)
                return node.path
            lnewnodes = []
            for a in AI.actions(node):
                newgrid, bounds = AI.result(node, a)
                if not node.in_parent(newgrid):
                    print(a)
                    newnode = Matrix(newgrid, [a], node)
                    newnode.set_bounds(a[0], bounds)
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    def add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)

matrix = Matrix("03 ooBoooooBooCAABooCoooooooooooooooooo 62")

# A DESLOCAÇÃO FUNCIONA
# print(matrix.pieces["B"])
# print(matrix)
# newgrid, bounds = AI.result(matrix, ("B", "s"))
# matrix2 = Matrix(newgrid, [("B", "s")], matrix)
# matrix2.set_bounds("B", bounds)
# print(matrix2.pieces["B"])
# print(matrix2)
# newgrid, bounds = AI.result(matrix2, ("B", "w"))
# matrix3 = Matrix(newgrid, [("B", "w")], matrix2)
# matrix3.set_bounds("B", bounds)
# print(matrix3.pieces["B"])
# print(matrix3)

# A DESLOCAÇÃO FUNCIONA
#matrix = Matrix("03 ooBoooooBooCAABooCooooooooDDDooooooo 62")
# print(matrix.pieces["D"])
# print(matrix)
# newgrid, bounds = AI.result(matrix, ("D", "d"))
# matrix4 = Matrix(newgrid, [("D", "d")], matrix)
# matrix4.set_bounds("D", bounds)
# print(matrix4.pieces["D"])
# print(matrix4)
# newgrid, bounds = AI.result(matrix4, ("D", "a"))
# matrix5 = Matrix(newgrid, [("D", "a")], matrix4)
# matrix5.set_bounds("D", bounds)
# print(matrix5.pieces["D"])
# print(matrix5)

# HÁ UM PROBLEMA EM ALGUMAS DESLOCAÇĨES
t = SearchTree(matrix, "breadth")
print(t.search())