from common import Coordinates

class SearchDomain:
    def __init__(self, m):
        self.m = m
    
    def actions(self, coord):
        (x, y) = coord
        actions = []
        if x > 0:
            actions.append("a")
        if x < self.m.grid_size - 1:
            actions.append("d")
        if y > 0:
            actions.append("w")
        if y < self.m.grid_size - 1:
            actions.append("s")
        return actions
    
    def result(self, coord, action):
        (x, y) = coord
        if action == "w":
            return (x, y-1)
        elif action == "a":
            return (x-1, y)
        elif action == "s":
            return (x, y+1)
        elif action == "d":
            return (x+1, y)

    def satisfies(self, coord, goal):
        return Coordinates(coord[0], coord[1]) in goal

class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state, self.goal)

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

class SearchTree:
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None

    def get_path(self,node):
        if node.parent == None:
            return []
        path = self.get_path(node.parent)
        (x2, y2) = node.state
        (x1, y1) = node.parent.state
        move = (x2-x1, y2-y1)
        if move == (-1, 0):
            path += ["a"]
        elif move == (1, 0):
            path += ["d"]
        elif move == (0, -1):
            path += ["w"]
        elif move == (0, 1):
            path += ["s"]
        return path

    def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                return self.get_path(node)
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if not node.in_parent(newstate):
                    newnode = SearchNode(newstate, node)
                    lnewnodes.append(newnode)
            self.add_to_open(lnewnodes)
        return None

    def add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)