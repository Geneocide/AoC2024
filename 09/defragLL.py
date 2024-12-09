from pathlib import Path
import time
import numpy as np
import LL

filepath = Path(__file__).parent / "input.txt"

start_time = time.perf_counter()

with filepath.open() as file:
    original = file.read().strip()

fileSizes = original[::2]
spaces = [int(char) for char in original[1::2]]

print(fileSizes)
print(spaces)

files = []
for i in range(len(fileSizes)):
    str_i = str(i)
    file = str_i * int(fileSizes[i])
    digits = len(str_i)
    file = [file[j : j + digits] for j in range(0, len(file), digits)]
    files.append(file)

print(files)
dll = LL.DoublyLinkedList()
for i, file in enumerate(files):
    dll.append(file, False)
    if i < len(spaces):
        space = list("." * spaces[i])
        if space:
            dll.append(space, True)

dll.display()

backwards = dll.tail
while backwards.prev != dll.head:
    if backwards.isSpace or backwards.moved:
        backwards = backwards.prev
        continue
    forwards = dll.head
    while forwards.next != backwards:
        if forwards.isSpace and len(forwards.data) >= len(backwards.data):
            forwards.data = forwards.data[: -1 * len(backwards.data)]
            dll.insert(forwards.prev, backwards.data, False, True)
            backwards.data = list(len(backwards.data) * ".")
            dll.clean(forwards)
            dll.clean(backwards)
            break
        forwards = forwards.next
    # dll.display()
    backwards = backwards.prev

expanded = np.array([])
forwards = dll.head
while forwards.next:
    expanded = np.append(expanded, forwards.data)
    forwards = forwards.next

print(expanded)

checksum = 0
for i, fileIndex in enumerate(expanded):
    if fileIndex == ".":
        continue
    checksum += int(fileIndex) * i

end_time = time.perf_counter()
print(f"The calculated checksum is {checksum}")  # 6415163644414 too high
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
