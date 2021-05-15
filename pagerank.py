from gridgraph import GridGraph
import sys


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

    graph.streamEdge(compute_deg,vert)

    def contribute(edge,newpr=newpr,pr=pr):
        newpr[int(edge["target"])] += pr[int(edge["source"])] / deg[int(edge["source"])]
        return 1

    def compute(vertices, newpr=newpr, pr=pr,d=damping,diff=diff):
        newpr[vertices] = 1 - d + d * newpr[vertices]
        diff += abs(newpr[vertices] - pr[vertices])
        return 1

    graph.streamEdge(compute_deg, vert)

    while converged != True :
        diff = 0
        newpr = [0 for i in range(0, graph.V)]
        graph.streamEdge(contribute,vert)
        graph.streamVertice(compute)
        newpr,pr = pr,newpr
        converged = (diff/graph.V <= 0.0001)
        

    print("final result of pagerank: ", pr)
