class Node:
    def __init__(self, data, isSpace, moved=False):
        self.data = data
        self.isSpace = isSpace
        self.moved = moved
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, data, isSpace, moved=False):
        new_node = Node(data, isSpace, moved)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1

    def insert(self, node, data, isSpace, moved):
        new_node = Node(data, isSpace, moved)
        new_node.prev = node
        new_node.next = node.next

        if node.next:
            node.next.prev = new_node

        node.next = new_node

    def clean(self, node):
        if node != self.head:
            cur = node.prev
        else:
            cur = node
        if node.next:
            stop = node.next
        else:
            stop = node
        while cur and cur != stop:
            if cur.data == []:
                tmp = cur
                cur.prev.next = tmp.next
                cur.next.prev = tmp.prev
                cur = tmp.next
            else:
                cur = cur.next

        if node != self.head:
            cur = node.prev
        else:
            cur = node
        while cur and cur != stop:
            if cur != self.tail and "." in cur.data and "." in cur.next.data:
                cur.data = cur.data + cur.next.data
                tmp = cur.next
                cur.next = tmp.next
                tmp.prev = cur
                if tmp == self.tail:
                    self.tail = cur
            cur = cur.next

    # def prepend(self, data):
    #     new_node = Node(data)
    #     new_node.next = self.head
    #     if self.head is not None:
    #         self.head.prev = new_node
    #     self.head = new_node
    #     self.length += 1

    def display(self):
        cur = self.head
        while cur:
            print(cur.data, end=" <-> ")
            cur = cur.next
        print("None")
