import heapq
from pathlib import Path
import time

filepath = Path(__file__).parent / "input.txt"
MAX_SIZE = 6 if "Test" in str(filepath) else 70
FALL_TIME = 12 if "Test" in str(filepath) else 1024
all_dirs = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}

start_time = time.perf_counter()


def prettyPrint(coordinates, symbol, onMap=None, makeMap=False):
    aMap = {}
    for y in range(MAX_SIZE + 1):
        print_line = ""
        for x in range(MAX_SIZE + 1):
            if (x, y) in coordinates:
                c = symbol
            else:
                if onMap:
                    c = onMap[(x, y)]
                else:
                    c = "."
            if makeMap:
                aMap[(x, y)] = c
            print_line += c
        print(print_line)
    print()
    if makeMap:
        return aMap


def getOpenPaths(positions, coordinates):
    openPositions = []
    position = positions[-1]
    previousPosition = positions[-2] if len(positions) > 1 else None
    for dir in all_dirs:
        dx, dy = all_dirs[dir]
        if (
            dx + position[0],
            dy + position[1],
        ) != previousPosition:  # never turn around 180
            if (
                dx + position[0],
                dy + position[1],
            ) not in positions:  # never go back over trail
                if (
                    dx + position[0] <= MAX_SIZE and dy + position[1] <= MAX_SIZE
                ):  # never go outside the map
                    checking = coordinates.get((dx + position[0], dy + position[1]))
                    if checking and checking != "#":
                        openPositions.append((dx + position[0], dy + position[1]))
    return openPositions


def heuristic(pos, goal):
    # Use Manhattan distance as a heuristic
    return abs(pos[0] - MAX_SIZE) + abs(pos[1] - MAX_SIZE)


def followPathsAStar(start_trail, aMap):
    validTrails = []
    heap = [
        (
            len(start_trail) + heuristic(start_trail[-1], (MAX_SIZE, MAX_SIZE)),
            start_trail,
        )
    ]
    visited = set()  # To keep track of visited nodes

    while heap:
        _, current_trail = heapq.heappop(heap)
        # prettyPrint(mazeDict, current_trail)

        if current_trail[-1] in visited:
            continue

        visited.add(current_trail[-1])

        if (MAX_SIZE, MAX_SIZE) == current_trail[-1]:  # Reached the goal
            print(
                f"Found a solution with a cost of length {len(current_trail) - 1}"
            )  # starting location doesn't count
            validTrails.append(current_trail)
            continue

        paths = getOpenPaths(current_trail, aMap)
        for path in paths:
            new_trail = current_trail.copy()
            new_trail.append(path)
            heapq.heappush(heap, (len(new_trail), new_trail))

    return validTrails


coordinates = []
with filepath.open() as file:
    for line in file:
        coordinates.append(tuple([int(c) for c in line.strip().split(",")]))

aMap = prettyPrint(coordinates[:FALL_TIME], "#", makeMap=True)
validTrails = followPathsAStar([(0, 0)], aMap)
minimumTrailLength = 1e5
for trail in validTrails:
    prettyPrint(trail, "O", aMap)
    minimumTrailLength = (
        len(trail) if len(trail) < minimumTrailLength else minimumTrailLength
    )

print(
    f"The minimum trail length found is {minimumTrailLength-1}"  # 278
)  # starting location doesn't count
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
