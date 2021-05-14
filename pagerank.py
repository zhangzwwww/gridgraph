from gridgraph import GridGraph
import sys


if __name__ == "__main__":
    graph = GridGraph("input", 8, 0, 0)
    graph.preprocess()

    def contribute(edge,pr,newpr):
        newpr[edge.target] += pr[edge.source]/count(edge.source)
        return newpr

    def compute(d,vertices,newpr,pr):
        newpr[vertices] = 1 - d + d * newpr[vertices]        
        return abs(newpr[vertices] - pr[vertices])

    pr = [1 for i in range(0, graph.V)]
    damping = 0.85
    converged = False

    while converged != True :
        newpr = [0 for i in range(0, graph.V)]
        newpr = graph.streamEdge(contribute())
        diff = graph.streamVertice(compute())
        newpr,pr = pr,newpr
        converged = (diff/graph.V <= 0.0001)
        

    print("final result of pagerank: ", pr)
