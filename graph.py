import matplotlib.pyplot as plt
import numpy as np
import os

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

def plot_linear_regression(xlist, ylist, labels):
    for i in range(len(xlist)):
        x = xlist[i]
        y = ylist[i]
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, [m * i + b for i in x], label=labels[i])

def show_graphs(LEVELS_PACK):
    # Gráfico com retas x = nível, y = tempo de execução, para cada strategy
    x1, y1 = linear_graph(f"benchmarks/{LEVELS_PACK}/depth.csv", "time")
    x2, y2 = linear_graph(f"benchmarks/{LEVELS_PACK}/breadth.csv", "time")
    x3, y3 = linear_graph(f"benchmarks/{LEVELS_PACK}/uniform.csv", "time")
    x4, y4 = linear_graph(f"benchmarks/{LEVELS_PACK}/greedy.csv", "time")
    x5, y5 = linear_graph(f"benchmarks/{LEVELS_PACK}/a*.csv", "time")

    plot_linear_regression([x1, x2, x3, x4, x5], [y1, y2, y3, y4, y5], ["Depth", "Breadth", "Uniform", "Greedy", "A*"])

    if len(x1) < 20:
        plt.xticks(np.arange(min(x1), max(x1) + 1, 1.0))

    axes = plt.gca()
    axes.set_xlim([0, None])
    axes.set_ylim([0, None])
    plt.xlabel("Level")
    plt.ylabel("Time (s)")
    plt.title(f"Linear regression of time per level ({LEVELS_PACK})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"graphs/{LEVELS_PACK}/time_graph.png")
    plt.show()

    # Gráfico com retas x = nível, y = número de nós expandidos, para cada strategy
    x1, y1 = linear_graph(f"benchmarks/{LEVELS_PACK}/depth.csv", "nodes")
    x2, y2 = linear_graph(f"benchmarks/{LEVELS_PACK}/breadth.csv", "nodes")
    x3, y3 = linear_graph(f"benchmarks/{LEVELS_PACK}/uniform.csv", "nodes")
    x4, y4 = linear_graph(f"benchmarks/{LEVELS_PACK}/greedy.csv", "nodes")
    x5, y5 = linear_graph(f"benchmarks/{LEVELS_PACK}/a*.csv", "nodes")

    plot_linear_regression([x1, x2, x3, x4, x5], [y1, y2, y3, y4, y5], ["Depth", "Breadth", "Uniform", "Greedy", "A*"])

    if len(x1) < 20:
        plt.xticks(np.arange(min(x1), max(x1) + 1, 1.0))

    axes = plt.gca()
    axes.set_xlim([0, None])
    axes.set_ylim([0, None])
    plt.xlabel("Level")
    plt.ylabel("Number of expanded nodes")
    plt.title(f"Linear regression of number of expanded nodes per level ({LEVELS_PACK})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"graphs/{LEVELS_PACK}/nodes_graph.png")
    plt.show()

    # Gráfico com retas x = nível, y = número de peças movidas, para cada strategy
    x1, y1 = linear_graph(f"benchmarks/{LEVELS_PACK}/depth.csv", "moves")
    x2, y2 = linear_graph(f"benchmarks/{LEVELS_PACK}/breadth.csv", "moves")
    x3, y3 = linear_graph(f"benchmarks/{LEVELS_PACK}/uniform.csv", "moves")
    x4, y4 = linear_graph(f"benchmarks/{LEVELS_PACK}/greedy.csv", "moves")
    x5, y5 = linear_graph(f"benchmarks/{LEVELS_PACK}/a*.csv", "moves")

    plot_linear_regression([x1, x2, x3, x4, x5], [y1, y2, y3, y4, y5], ["Depth", "Breadth", "Uniform", "Greedy", "A*"])

    if len(x1) < 20:
        plt.xticks(np.arange(min(x1), max(x1) + 1, 1.0))

    axes = plt.gca()
    axes.set_xlim([0, None])
    axes.set_ylim([0, None])
    plt.xlabel("Level")
    plt.ylabel("Number of moved pieces")
    plt.title(f"Linear regression of number of moved pieces per level ({LEVELS_PACK})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"graphs/{LEVELS_PACK}/moves_graph.png")
    plt.show()

if not os.path.exists("graphs"):
    os.mkdir("graphs")
if not os.path.exists("graphs/levels1"):
    os.mkdir("graphs/levels1")
if not os.path.exists("graphs/levels2"):
    os.mkdir("graphs/levels2")
if not os.path.exists("graphs/levels"):
    os.mkdir("graphs/levels")

"""
levels1.txt: pack de níveis 6x6 da entrega preliminar
 1) Breadth 488 640
 2) Uniform 489 739
 3) Greedy 487 299
 4) A* 489 576
"""

show_graphs("levels1")

# Gráfico de barras x = strategy, y = pontos 
x = ["Breadth", "Uniform", "Greedy", "A*"]
y = [488640, 489739, 487299, 489576]

plt.bar(x, y, color=["orange", "green", "red", "purple"])
plt.bar_label(plt.gca().containers[0], padding=3)
plt.xlabel("Strategy")
plt.ylabel("Points")
plt.title("Points per strategy (levels1)")
plt.ylim(487000, 490000)
plt.tight_layout()
plt.savefig("graphs/levels1/points_graph.png")
plt.show()

"""
 levels2.txt: pack de níveis 8x8
 1) Breadth 1 041 039
 2) Uniform 1 040 375
 3) Greedy 1 041 987
 4) A* 1 039 496
"""

show_graphs("levels2")

# Gráfico de barras x = strategy, y = pontos
x = ["Breadth", "Uniform", "Greedy", "A*"]
y = [1041039, 1040375, 1041987, 1039496]

plt.bar(x, y, color=["orange", "green", "red", "purple"])
plt.bar_label(plt.gca().containers[0], padding=3, fmt="%d")
plt.xlabel("Strategy")
plt.ylabel("Points")
plt.title("Points per strategy (levels2)")
plt.ylim(1039000, 1043000)
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig("graphs/levels2/points_graph.png")
plt.show()

"""
 levels.txt: pack definitivo para a entrega final
 1) Breadth 1 556 748
 2) Uniform 1 557 267
 3) Greedy 1 556 135
 4) A* 1 556 969
 5) Híbrido (Uniform para 6x6 + Greedy para 8x8) 1 558 015
"""

# # Gráfico com retas x = nível, y = tempo de execução, para cada strategy
# x1, y1 = linear_graph(f"benchmarks/levels/depth.csv", "time")
# x2, y2 = linear_graph(f"benchmarks/levels/breadth.csv", "time")
# x3, y3 = linear_graph(f"benchmarks/levels/uniform.csv", "time")
# x4, y4 = linear_graph(f"benchmarks/levels/greedy.csv", "time")
# x5, y5 = linear_graph(f"benchmarks/levels/a*.csv", "time")
# x6, y6 = linear_graph(f"benchmarks/levels/hybrid.csv", "time")

# plt.plot(x1, y1, label="Depth", color="orange")
# plt.plot(x2, y2, label="Breadth", color="green")
# plt.plot(x3, y3, label="Uniform", color="red")
# plt.plot(x4, y4, label="Greedy", color="purple")
# plt.plot(x5, y5, label="A*", color="blue")

# plt.xlabel("Level")
# plt.ylabel("Time (s)")
# plt.title("Time per level (levels)")
# plt.legend()
# #plt.show()

# # Gráfico com retas x = nível, y = número de nós expandidos, para cada strategy
# x1, y1 = linear_graph(f"benchmarks/levels/depth.csv", "nodes")
# x2, y2 = linear_graph(f"benchmarks/levels/breadth.csv", "nodes")
# x3, y3 = linear_graph(f"benchmarks/levels/uniform.csv", "nodes")
# x4, y4 = linear_graph(f"benchmarks/levels/greedy.csv", "nodes")
# x5, y5 = linear_graph(f"benchmarks/levels/a*.csv", "nodes")
# x6, y6 = linear_graph(f"benchmarks/levels/hybrid.csv", "nodes")

# plt.plot(x1, y1, label="Depth", color="orange")
# plt.plot(x2, y2, label="Breadth", color="green")
# plt.plot(x3, y3, label="Uniform", color="red")
# plt.plot(x4, y4, label="Greedy", color="purple")
# plt.plot(x5, y5, label="A*", color="blue")
# plt.plot(x6, y6, label="Hybrid", color="black")

# plt.xlabel("Level")
# plt.ylabel("Number of expanded nodes")
# plt.title("Expanded nodes per level (levels)")
# plt.legend()
# #plt.show()

# # Gráfico com retas x = nível, y = número de peças movidas, para cada strategy
# x1, y1 = linear_graph(f"benchmarks/levels/depth.csv", "moves")
# x2, y2 = linear_graph(f"benchmarks/levels/breadth.csv", "moves")
# x3, y3 = linear_graph(f"benchmarks/levels/uniform.csv", "moves")
# x4, y4 = linear_graph(f"benchmarks/levels/greedy.csv", "moves")
# x5, y5 = linear_graph(f"benchmarks/levels/a*.csv", "moves")
# x6, y6 = linear_graph(f"benchmarks/levels/hybrid.csv", "moves")

# plt.plot(x1, y1, label="Depth", color="orange")
# plt.plot(x2, y2, label="Breadth", color="green")
# plt.plot(x3, y3, label="Uniform", color="red")
# plt.plot(x4, y4, label="Greedy", color="purple")
# plt.plot(x5, y5, label="A*", color="blue")
# plt.plot(x6, y6, label="Hybrid", color="black")

# plt.xlabel("Level")
# plt.ylabel("Number of moved pieces")
# plt.title("Moved pieces per level (levels)")
# plt.legend()
# #plt.show()

# Gráfico de barras x = strategy, y = pontos

x = ["Breadth", "Uniform", "Greedy", "A*", "Hybrid"]
y = [1556748, 1557267, 1556135, 1556969, 1558015]

plt.bar(x, y, color=["orange", "green", "red", "purple", "blue"])
plt.bar_label(plt.gca().containers[0], padding=3, fmt="%d")
plt.xlabel("Strategy")
plt.ylabel("Points")
plt.title("Points per strategy (levels)")
plt.ylim(1555000, 1559000)
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig("graphs/levels/points_graph.png")
plt.show()