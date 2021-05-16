from gridgraph import GridGraph
import sys


if __name__ == "__main__":
    graph = GridGraph("input", 8, 0, 0, 2)
    graph.preprocess()

    parent = [-1 for i in range(0, graph.V)]
    start_vertice = int(sys.argv[1])
    parent[start_vertice] = start_vertice

    active_in = []
    active_vertices = 1
    active_out = []
    active_out.append(start_vertice)

    def get_active_vertice(data, parent=parent):
        if parent[int(data["target"])] != -1:
            return 0
        parent[int(data["target"])] = int(data["target"])
        active_out.append(data["target"])
        return 1

    iteration = 1

    while active_vertices != 0:
        print("iteration: ", iteration)
        iteration += 1
        active_in, active_out = active_out, active_in
        active_out = []
        active_vertices = graph.streamEdge(get_active_vertice, active_in)
        new_vertice = ""
        for i in active_out:
            new_vertice = new_vertice + str(i) + ' '
        print("new discovered vertices: ", new_vertice)

    discovered_vertice = 0
    for d in parent:
        if d != -1:
            discovered_vertice += 1

    print("discovered ", discovered_vertice, " vertices")
