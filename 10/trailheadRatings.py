from pathlib import Path
import time
import copy
import LL

filepath = Path(__file__).parent / "input.txt"

all_dirs = {
    "N": (0, -1),
    # "NE": (1, -1),
    "E": (1, 0),
    # "SE": (1, 1),
    "S": (0, 1),
    # "SW": (-1, 1),
    "W": (-1, 0),
    # "NW": (-1, -1),
}


def explore(x, y, previousNode: LL.Node = None):
    if x < 0 or y < 0 or x >= len(nMap[0]) or y >= len(nMap):
        return
    if isinstance(nMap[y][x], int):
        node = LL.Node((x, y), nMap[y][x])
        nMap[y][x] = node
    elif isinstance(nMap[y][x], LL.Node):
        node = nMap[y][x]
    if previousNode and node in previousNode.links:
        return
    if previousNode and node.elevation - 1 != previousNode.elevation:
        return
    else:
        if previousNode:
            previousNode.links.append(node)
        for direction in all_dirs:
            new_x = all_dirs[direction][0] + x
            new_y = all_dirs[direction][1] + y
            explore(new_x, new_y, node)


memo = {}
oMap = []


def findTrails(x=None, y=None, trail=None):
    validTrails = []
    if not trail:
        node = nMap[y][x]
        if node.elevation == 0:
            trail = LL.Trail()
            trail.append(node)
    else:
        if trail.tail.coords in memo:
            return memo[trail.tail.coords]
        node = trail.tail
    for link in node.links:
        trail.append(link)
        if trail.tail.elevation == 9:
            validTrails.append(copy.deepcopy(trail))
        else:
            validTrails += findTrails(trail=trail)
    if node.coords in memo:
        memo[node.coords] += validTrails
    else:
        memo[node.coords] = validTrails
    return validTrails


def prettyPrint(aMap):
    for line in aMap:
        printableLine = " ".join([str(char) for char in line])
        print(printableLine)
    print(" ")


start_time = time.perf_counter()


with filepath.open() as file:
    for line in file:
        oMap.append([int(char) for char in line.strip()])

prettyPrint(oMap)

nMap = copy.deepcopy(oMap)
tempMap = copy.deepcopy(oMap)
trailheads = []
for y, line in enumerate(oMap):
    for x, char in enumerate(line):
        if char == 0:
            explore(x, y)
            trailheads.append((x, y))

total = 0
for x, y in trailheads:
    trails = findTrails(x, y)
    peaks = {}
    for trail in trails:
        if trail.tail.coords in peaks:
            peaks[trail.tail.coords] += 1
        else:
            peaks[trail.tail.coords] = 1

    trailheadTotal = 0
    for peakCoords, count in peaks.items():
        trailheadTotal += count
        # print(
        #     f"Found trails for trailhead at ({x, y}) to {count} peaks at {peakCoords}"
        # )
    print(f"Trailhead at {x, y} has a rating of: {trailheadTotal}")
    total += trailheadTotal
print(f"The sum of scores for all trailheads is: {total}")  # 1086
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
