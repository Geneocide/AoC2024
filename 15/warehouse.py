from pathlib import Path
import time
import LL

filepath = Path(__file__).parent / "input.txt"


def prettyPrint(aMap):
    for line in aMap:
        printableLine = " ".join([str(node.data) for node in line])
        print(printableLine)


start_time = time.perf_counter()

map = []
moves = []
with filepath.open() as file:
    isLastLine = False
    for y, line in enumerate(file):
        if isLastLine:
            [moves.append(char) for char in line.strip()]
        else:
            if not line.strip():
                isLastLine = True
            else:
                map.append(
                    [LL.Node((x, y), char) for x, char in enumerate(line.strip())]
                )

prettyPrint(map)
print(moves)

robot = None
for row in map:
    if not robot:
        for node in row:
            if node.data == "@":
                robot = node
                break

for move in moves:
    chain = LL.Chain()
    chain.append(robot)

    while True:
        intendedCoords = chain.tail.move(move)
        chain.append(map[intendedCoords[1]][intendedCoords[0]])
        if chain.tail.data == "#":
            break
        if chain.tail.data == ".":
            robot = chain.shift()
            break
        if chain.tail.data == "O":
            continue

prettyPrint(map)

totalGPSCoordinates = 0
for row in map:
    for node in row:
        if node.data == "O":
            totalGPSCoordinates += node.coords[1] * 100 + node.coords[0]

print(f"The total GPS coordinates is: {totalGPSCoordinates}")  # 1448589
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
