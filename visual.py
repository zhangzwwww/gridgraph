import numpy as np
import cv2


class Visual():
    def __init__(self, sizeV, sizeCache, sizeMemory, P, Q):
        self.width = 2000
        self.height = 1000
        self.canvas = np.ones((self.width, self.height, 3), np.uint8)
        self.P = P
        self.Q = Q
        self.top_buffer = 100
        self.left_buffer = 100

        self.block_width = 80

        self.recovery()

        cv2.waitKey()

    def recovery(self):
        self.canvas = np.ones((self.width, self.height, 3), np.uint8)
        for i in range(0, self.P):
            for j in range(0, self.P):
                cv2.rectangle(self.canvas,
                              (self.top_buffer + self.block_width * i,
                               self.left_buffer + self.block_width * j),
                              (self.block_width * (i + 1) + self.top_buffer,
                               self.left_buffer + self.block_width * (j + 1)),
                              (0, 255, 0), 3)
                cv2.imshow('rect', self.canvas)

    def highlight(self, row, column):
        row_interval = int(row / 4)
        column_interval = int(column / 4)
        cv2.rectangle(self.canvas,
                      (self.top_buffer + self.block_width * column_interval * 4,
                       self.left_buffer + self.block_width * row_interval * 4),
                      (self.block_width * (column_interval + 1) * 4 + self.top_buffer,
                       self.left_buffer + self.block_width * (row_interval + 1) * 4),
                      (0, 0, 255), 3)
        cv2.imshow('rect', self.canvas)

        cv2.rectangle(self.canvas,
                      (self.top_buffer + self.block_width * column, self.top_buffer + self.block_width * row),
                      (self.top_buffer + self.block_width * (column + 1),
                       self.left_buffer + self.block_width * (row + 1)),
                      (255, 0, 0), -1)
        cv2.imshow('rect', self.canvas)
        cv2.waitKey(0)

    def drawCurrentState(self, data):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = "current block data: \n"
        for d in data:
            text = text + str(d) + '\n'
        height = 900
        for i, txt in enumerate(text.split('\n')):
            height = height + 20
            cv2.putText(self.canvas, txt, (10, height), font, .6, (255, 255, 255), 1, 2)
        cv2.imshow('show', self.canvas)
        cv2.waitKey(0)

    def destroy(self):
        cv2.destroyAllWindows()


# if __name__ == "__main__":
    # vs = Visual(64, 64, 64, 8, 2)
    # vs.highlight(1, 2)
#     vs.destroy()
