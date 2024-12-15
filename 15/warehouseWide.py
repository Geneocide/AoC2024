from pathlib import Path
import time
import LLnew

filepath = Path(__file__).parent / "inputTest2.txt"


def prettyPrint(rows):
    for line in rows:
        line.prettyPrint()


start_time = time.perf_counter()

rows = []
cols = []
moves = []
robot = None
with filepath.open() as file:
    isLastLine = False
    for y, line in enumerate(file):
        row = LLnew.Chain()
        if isLastLine:
            [moves.append(char) for char in line.strip()]
        else:
            if not line.strip():
                isLastLine = True
            else:
                for x, char in enumerate(line.strip()):
                    if y == 0:
                        cols.append(LLnew.Chain())
                        cols.append(LLnew.Chain())
                    if char == "O":
                        leftNode = LLnew.Node("[")
                        rightNode = LLnew.Node("]")
                        leftNode.setLink(rightNode)
                        row.append(leftNode)
                        row.append(rightNode)
                        cols[x].append(leftNode)
                        cols[x + 1].append(rightNode)
                    elif char == "@":
                        robot = LLnew.Node(char)
                        row.append(robot)
                        row.append(LLnew.Node("."))
                        cols[x].append(robot)
                        cols[x + 1].append(LLnew.Node("."))
                    else:
                        row.append(LLnew.Node(char))
                        row.append(LLnew.Node(char))
                        cols[x].append(LLnew.Node(char))
                        cols[x + 1].append(LLnew.Node(char))
                rows.append(row)

prettyPrint(rows)
print(moves)

for dir in moves:
    chain = LLnew.Chain()
    chain.append(robot)

    print(dir)
    prettyPrint(rows)

    while True:
        intendedCoordsArray = chain.tail.move(dir)

        intendedNodes = []
        for intendedCoords in intendedCoordsArray:
            intendedNodes.append(rows[intendedCoords[1]][intendedCoords[0]])
        if len(intendedNodes) > 1:
            chain.append(LLnew.Object(intendedNodes))
        else:
            chain.append(intendedNodes[0])
        if "#" in chain.tail.getData():
            break
        if all(data == "." for data in chain.tail.getData()):
            robot = chain.shift()
            break


prettyPrint(rows)

totalGPSCoordinates = 0
for row in rows:
    for node in row:
        if node.data == "O":
            totalGPSCoordinates += node.coords[1] * 100 + node.coords[0]

print(f"The total GPS coordinates is: {totalGPSCoordinates}")  # 1448589
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
