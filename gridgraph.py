import threading


# get vertex in partition location
# source: source vertex
# target: target vertex
# partition: partition number
# return the vertex in which partition
def getP(source, target, partition):
    row = source / partition
    column = target / partition
    return int(row), int(column)


# get source and target vertex from file input
# fileInput: input from vertex file like 2,0 means edge from vertex 2 to vertex 0
# return the source and target vertex
def getVFromFileInput(fileInput):
    vertexPair = fileInput.split(',')
    return int(vertexPair[0]), int(vertexPair[1])


# process edge
# start: start line of the vertex file
# end: end line of the vertex file
class EdgeWorker(threading.Thread):
    def __init__(self, name, queue, partition, bufferSize):
        super(EdgeWorker, self).__init__()
        self.queue = queue
        self.name = name
        self.partition = partition
        self.bufferSize = bufferSize
        self.data = [[[] for j in range(0, self.partition)] for i in range(0, self.partition)]

    def run(self):
        while True:
            if len(self.queue) > 0:
                if self.queue[0] == "end":
                    for r in range(0, self.partition):
                        for c in range(0, self.partition):
                            self.writeFile(r, c)
                    return

                source, target = getVFromFileInput(self.queue[0])
                row, column = getP(source, target, self.partition)
                self.data[row][column].append(str(source) + ',' + str(target))

                if (len(self.data[row][column]) > self.bufferSize):
                    self.writeFile(row, column)
                    self.data[row][column] = []

                self.queue = self.queue[1:]

    def writeFile(self, row, column):
        edgeData = self.data[row][column]
        filename = str(row) + '-' + str(column)
        fo = open("blocks/" + filename, "a")
        for d in edgeData:
            fo.write(d + '\n')
        fo.flush()
        fo.close()


# gridgraph class
# vertexFilename: file with vertex input first line is the vertex number followings are the edges with the pattern like
# 2,0 which means edge joint vertex 2 and vertex 0
# partition: partition number
# cacheSize: cache Size
# edgeWorkerNumber: workder number
class GridGraph():
    def __init__(self, vertexFilename, partition, cacheSize, edgeWorderNumber, Q):
        self.filename = vertexFilename
        self.partition = partition
        self.V = 0
        self.E = 0
        self.T = "unweighted"
        self.Q = Q
        pass

    def preprocess(self):
        queue = [[], []]
        vertexFile = open(self.filename, "r")
        line = vertexFile.readline()
        self.V = int(line.strip())
        line = vertexFile.readline()

        worker0 = EdgeWorker("worker0", queue[0], self.partition, 20)
        worker1 = EdgeWorker("worker1", queue[1], self.partition, 20)
        worker0.start()
        worker1.start()

        currentWorkerIndex = 0

        while line is not None and line != '':
            line = line.replace('\n', '')
            queue[currentWorkerIndex].append(line)
            currentWorkerIndex = currentWorkerIndex ^ 1
            line = vertexFile.readline()
            self.E += 1

        for item in queue:
            item.append("end")

        self.generateMetadata(self.V, self.E, self.partition, self.T)

    def generateMetadata(self, V, E, P, T):
        fo = open("metadata", "w")
        fo.write("vertice number:" + str(V) + '\n')
        fo.write("edge number:" + str(E) + '\n')
        fo.write("partition number:" + str(P) + '\n')
        fo.write("type:" + T + '\n')
        fo.flush()
        fo.close()

    def streamVertice(self, process):
        sum = 0
        for i in range(0, self.V):
            sum += process(i)
        return sum

    # streamEdge
    # process: process function
    # vertice: active_vertice set
    # update_mode: 1 source oriented update 2 target oriented update
    def streamEdge(self, process, vertice, update_mode=1):
        sum = 0
        if update_mode == 1:
            for Qrow in range(0, self.Q):
                for Qcolumn in range(0, self.Q):
                    for Prow in range(0, int(self.partition / self.Q)):
                        for Pcolumn in range(0, int(self.partition / self.Q)):
                            row = Prow + Qrow * int(self.partition / self.Q)
                            column = Pcolumn + Qcolumn * int(self.partition / self.Q)
                            sourceList = self.getPartitionSourceVertices(row, column)
                            for v in sourceList:
                                if v in vertice:
                                    try:
                                        data = self.readVertices(row, column)
                                        for d in data:
                                            if int(d["source"]) in vertice:
                                                sum += process(d)
                                    except FileNotFoundError:
                                        continue
                                    continue
        elif update_mode == 0:
            for Qcolumn in range(0, self.Q):
                for Qrow in range(0, self.Q):
                    for Pcolumn in range(0, int(self.partition / self.Q)):
                        for Prow in range(0, int(self.partition / self.Q)):
                            row = Prow + Qrow * int(self.partition / self.Q)
                            column = Pcolumn + Qcolumn * int(self.partition / self.Q)
                            sourceList = self.getPartitionSourceVertices(row, column)
                            for v in sourceList:
                                if v in vertice:
                                    try:
                                        data = self.readVertices(row, column)
                                        for d in data:
                                            if int(d["source"]) in vertice:
                                                sum += process(d)
                                    except FileNotFoundError:
                                        continue
                                    continue
        return sum

    def readVertices(self, row, column):
        f = open("blocks/" + str(row) + "-" + str(column), "r")
        line = f.readline().replace('\n', '')
        data = []
        while line is not None and line != '':
            source = int(line.split(',')[0])
            target = int(line.split(',')[1])
            data.append({"source": source, "target": target})
            line = f.readline().replace('\n', '')
        f.close()
        return data

    def getEdgeIndex(self, source, target):
        pass

    def getPartitionSourceVertices(self, row, column):
        return [i for i in range(row * self.partition, (row + 1) * self.partition)]

    def getPartitionTargetVertices(self, row, column):
        return [i for i in range(column * self.partition, (column + 1) * self.partition)]
