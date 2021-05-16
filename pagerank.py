from gridgraph import GridGraph


if __name__ == "__main__":
    graph = GridGraph("input", 8, 0, 0, 2)
    graph.preprocess()

    pr = [1 for i in range(0, graph.V)]
    damping = 0.85
    converged = False
    deg = [0 for i in range(0, graph.V)]
    vert = [i for i in range(0, graph.V)]
    newpr = [0 for i in range(0, graph.V)]
    diff = 0

    def compute_deg(edge, deg=deg):
        deg[int(edge["source"])] += 1
        return 1

    graph.streamEdge(compute_deg, vert)
    print("deg of each verticie", deg)
    def contribute(edge):
        newpr[int(edge["target"])] += pr[int(edge["source"])] / deg[int(edge["source"])]
        return 1

    graph.streamEdge(compute_deg, vert)

    while converged is not True:
        diff = 0
        newpr = [0 for i in range(0, graph.V)]
        graph.streamEdge(contribute, vert)
        
        def compute(vertices, newpr=newpr, pr=pr, d=damping, diff=diff):
            newpr[int(vertices)] = 1 - d + d * newpr[int(vertices)]
            return abs(newpr[int(vertices)]-pr[int(vertices)])
        diff = graph.streamVertice(compute)
        print("current result of difference", diff/graph.V)
        newpr, pr = pr, newpr
        print("current result of pagerank: ", pr)
        converged = (diff/graph.V <= 0.001)

    print("final result of pagerank: ", pr)
