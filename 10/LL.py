class Node:
    def __init__(self, coords, elevation):
        self.coords = coords
        self.elevation = elevation
        self.links = []
        self.next = None
        self.prev = None

    def copy(node):
        new_node = Node(node.coords, node.elevation)
        new_node.links = node.links
        new_node.next = node.next
        new_node.prev = node.prev
        return new_node


class Trail:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, node):
        new_node = node.copy()
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def displayOnMap(self, oMap):
        cur = self.head
        while cur:
            if cur.elevation == 0:
                oMap[cur.coords[1]][cur.coords[0]] = "⚐"
            elif cur.elevation == 9:
                oMap[cur.coords[1]][cur.coords[0]] = "⚑"
            else:
                # if cur.prev:
                dir1 = directions(cur.prev.coords, cur.coords)
                dir2 = directions(cur.coords, cur.next.coords)
                if dir1 == "N":
                    if dir2 == "N":
                        oMap[cur.coords[1]][cur.coords[0]] = "↑"
                    elif dir2 == "E":
                        oMap[cur.coords[1]][cur.coords[0]] = "↱"
                    elif dir2 == "W":
                        oMap[cur.coords[1]][cur.coords[0]] = "↰"
                elif dir1 == "S":
                    if dir2 == "S":
                        oMap[cur.coords[1]][cur.coords[0]] = "↓"
                    elif dir2 == "E":
                        oMap[cur.coords[1]][cur.coords[0]] = "↳"
                    elif dir2 == "W":
                        oMap[cur.coords[1]][cur.coords[0]] = "↵"
                elif dir1 == "E":
                    if dir2 == "N":
                        oMap[cur.coords[1]][cur.coords[0]] = "⬏"
                    elif dir2 == "E":
                        oMap[cur.coords[1]][cur.coords[0]] = "→"
                    elif dir2 == "S":
                        oMap[cur.coords[1]][cur.coords[0]] = "⬎"
                elif dir1 == "W":
                    if dir2 == "N":
                        oMap[cur.coords[1]][cur.coords[0]] = "⬑"
                    elif dir2 == "S":
                        oMap[cur.coords[1]][cur.coords[0]] = "⬐"
                    elif dir2 == "W":
                        oMap[cur.coords[1]][cur.coords[0]] = "←"
            cur = cur.next
        return oMap

    def display(self):
        cur = self.head
        while cur:
            print(cur.coords, end=" -> ")
            cur = cur.next
        print("")


def directions(before, after):
    deltaX = before[0] - after[0]
    deltaY = before[1] - after[1]
    if (deltaX, deltaY) == (0, 1):
        return "N"
    elif (deltaX, deltaY) == (0, -1):
        return "S"
    elif (deltaX, deltaY) == (1, 0):
        return "W"
    elif (deltaX, deltaY) == (-1, 0):
        return "E"
