all_dirs = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


class Node:
    def __init__(self, data, link=None):
        self.data = data
        self.link = link
        self.next = None
        self.prev = None

    def setLink(self, node):
        self.link = node
        node.link = self

    def move(self, dir):
        Xs, Ys = zip(self.coords, all_dirs[dir])
        return (sum(Xs), sum(Ys))


class Chain:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, node):
        node.next = None
        node.prev = None
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def shift(self):
        robot = None
        cur = self.tail
        tempData = cur.data
        while cur.prev:
            cur.data = cur.prev.data
            if cur.data == "@":
                robot = cur
            cur = cur.prev
        cur.data = tempData
        return robot

    def display(self):
        cur = self.head
        while cur:
            print(cur.data, end=" -> ")
            cur = cur.next
        print("")

    def prettyPrint(self):
        cur = self.head
        toPrint = ""
        while cur:
            toPrint += f"{cur.data} "
            cur = cur.next
        print(toPrint)
