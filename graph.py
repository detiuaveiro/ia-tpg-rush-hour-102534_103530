import matplotlib.pyplot as plt

def linear_graph(filename, type_):
    x = []
    y = []
    with open(filename, "r") as f:
        for line in f:
            line = line.split(",")
            x.append(int(line[0]))
            if type_ == "time":
                y.append(float(line[1]))
            elif type_ == "nodes":
                y.append(int(line[2]))
            elif type_ == "moves":
                y.append(int(line[3]))
    return x, y

def bar_graph(filename):
    x = []
    y = []
    with open(filename, "r") as f:
        for line in f:
            line = line.split(",")
            x.append(line[0])
            y.append(int(line[1]))
    return x, y

"""
levels1.txt: pack de níveis 6x6 da entrega preliminar
 1) Breadth
 2) Uniform
 3) Greedy
 4) A*
"""

# Gráfico com retas x = nível, y = tempo de execução, para cada strategy
# Gráfico com retas x = nível, y = número de nós expandidos, para cada strategy
# Gráfico com retas x = nível, y = número de peças movidas, para cada strategy
# Gráfico de barras x = strategy, y = pontos 

"""
 levels2.txt: pack de níveis 8x8
 1) Breadth
 2) Uniform
 3) Greedy
 4) A*
"""

# Gráfico com retas x = nível, y = tempo de execução, para cada strategy
# Gráfico com retas x = nível, y = número de nós expandidos, para cada strategy
# Gráfico com retas x = nível, y = número de peças movidas, para cada strategy
# Gráfico de barras x = strategy, y = pontos 

"""
 levels.txt: pack definitivo para a entrega final
 1) Breadth
 2) Uniform
 3) Greedy
 4) A*
 5) Híbrido (Uniform para 6x6 + Greedy para 8x8)
"""

# Gráfico com retas x = nível, y = tempo de execução, para cada strategy
# Gráfico com retas x = nível, y = número de nós expandidos, para cada strategy
# Gráfico com retas x = nível, y = número de peças movidas, para cada strategy
# Gráfico de barras x = strategy, y = pontos
