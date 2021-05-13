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
    def __init__(self, vertexFilename, partition, cacheSize, edgeWorderNumber):
        self.filename = vertexFilename
        self.partition = partition
        self.V = 0
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

        for item in queue:
            item.append("end")

    def readVertices(self):
        pass

    def getEdgeIndex(self, source, target):
        pass


if __name__ == "__main__":
    gg = GridGraph("input", 8, 0, 0)
    gg.preprocess()
