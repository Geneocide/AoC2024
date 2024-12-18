from pathlib import Path
import time
import heapq
from itertools import count


class Trail:
    def __init__(self, positions=None, facings=None, cost=0):
        self.positions = positions if positions else []
        self.facings = facings if facings else []
        # self.steps = steps if steps else []
        self.cost = cost

    def handleMove(self, facing):
        if facing == self.facings[-1]:
            self.facings.append(facing)
            self.cost += 1
        else:
            self.cost += 1001
            self.facings.append(facing)

    def merge(self, branch: "Trail"):
        self.positions.extend(branch.positions)
        self.steps.extend(branch.steps)
        self.cost += branch.cost


def prettyPrint(aMap: dict, trail=None):
    print()
    for py in range(Y_MAX):
        print_line = ""
        for px in range(X_MAX):
            c = aMap[(px, py)]
            if trail:
                if isinstance(trail, Trail):
                    if (px, py) in trail.positions:
                        c = "S"
                elif isinstance(trail, set):
                    if (px, py) in trail:
                        c = "S"
            if c == "#":
                c = "⛄"
            elif c == ".":
                c = "⬛"
            elif c == "E":
                c = "🏁"
            elif c == "S":
                c = "🦌"
            print_line += c
        print(print_line)
    print()


def getOpenPaths(position, facing):
    openPositions = []
    for dir in all_dirs:
        dx, dy = all_dirs[dir]
        if (
            dx + all_dirs[facing][0] != 0 or dy + all_dirs[facing][1] != 0
        ):  # never turn around 180
            checking = mazeDict.get((dx + position[0], dy + position[1]))
            if checking and checking != "#":
                openPositions.append((dx + position[0], dy + position[1]))
    return openPositions


def getSteps(position, facing, target):
    dx = target[0] - position[0]
    dy = target[1] - position[1]

    if all_dirs[facing] == (dx, dy):
        return facing
    else:
        for key, value in all_dirs.items():
            if value == (dx, dy):
                return key
    print("ERROR")
    return None


def moveOneStep(path, segment: Trail):
    # if path in segment.positions:
    #     print(f"Been to {path} before. Skipping.")
    #     return False  # been here before
    # if validTrails and segment.cost > min([t.cost for t in validTrails]):
    #     print(f"Costing too much. Skipping.")
    #     return False  # too costly already
    facing = getSteps(segment.positions[-1], segment.facings[-1], path)
    segment.handleMove(facing)
    segment.positions.append(path)
    return True


def heuristic(pos, goal):
    # Use Manhattan distance as a heuristic
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def followPaths(current_trail: Trail):
    counter = count()
    heap = [
        (
            current_trail.cost,
            next(counter),
            current_trail,
        )
    ]
    visited = (
        {}
    )  # Dictionary to store the minimum cost to reach each position with a specific facing
    while heap:
        current_cost, _, current_trail = heapq.heappop(heap)
        current_position = current_trail.positions[-1]
        current_facing = current_trail.facings[-1]
        # prettyPrint(mazeDict, current_trail)
        # Check if we have already visited this state with a lower cost
        if (
            (current_position, current_facing) in visited
            and visited[(current_position, current_facing)] < current_cost
            or current_cost > validTrails[0].cost
        ):
            continue

        # Update the visited dictionary with the current cost
        visited[(current_position, current_facing)] = current_cost
        if goal == current_trail.positions[-1]:  # made it to the end
            print(f"Found a solution with a cost of {current_trail.cost}")
            validTrails.append(current_trail)
            continue
        paths = getOpenPaths(current_position, current_facing)

        # while len(paths) == 1:
        #     if moveOneStep(paths[0], trail):
        #         paths = getOpenPaths(*trail.positions[-1])
        #         if goal == trail.positions[-1][0]:  # made it to the end
        #             validTrails.append(trail)
        #             return trail
        #     else:
        #         return None
        # if not paths:
        #     return None  # dead end
        for path in paths:
            if path in trail.positions:
                continue
            # newSegment = copy.deepcopy(trail)
            new_trail = Trail(
                current_trail.positions[:], current_trail.facings[:], current_trail.cost
            )
            if moveOneStep(path, new_trail):
                heapq.heappush(heap, (new_trail.cost, next(counter), new_trail))
    return validTrails


def followPathsAStar(start_trail: Trail):
    counter = count()
    heap = [
        (
            start_trail.cost + heuristic(start_trail.positions[-1], goal),
            next(counter),
            start_trail,
        )
    ]
    visited = set()  # To keep track of visited nodes

    while heap:
        _, _, current_trail = heapq.heappop(heap)
        # prettyPrint(mazeDict, current_trail)

        if current_trail.positions[-1] in visited:
            continue

        visited.add(current_trail.positions[-1])

        if goal == current_trail.positions[-1]:  # Reached the goal
            print(f"Found a solution with a cost of {current_trail.cost}")
            validTrails.append(current_trail)
            continue

        paths = getOpenPaths(current_trail.positions[-1], current_trail.facings[-1])
        for path in paths:
            new_trail = Trail(
                current_trail.positions[:], current_trail.facings[:], current_trail.cost
            )
            if moveOneStep(path, new_trail):
                # Calculate the total cost (g(n) + h(n))
                total_cost = new_trail.cost + heuristic(new_trail.positions[-1], goal)
                heapq.heappush(heap, (total_cost, next(counter), new_trail))

    return validTrails


start_time = time.perf_counter()

filepath = Path(__file__).parent / "input.txt"
with filepath.open() as file:
    lines = [line.rstrip() for line in file]

X_MAX = len(lines[0])
mazeDict = {}
validTrails = []
all_dirs = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}
for y, line in enumerate(lines):
    Y_MAX = y + 1
    for x, char in enumerate(line):
        if char == "S":
            trail = Trail([(x, y)], [">"])
            start = Trail([(x, y)], [">"])
        if char == "E":
            goal = (x, y)
        mazeDict[(x, y)] = char

prettyPrint(mazeDict)


validTrails = followPathsAStar(trail)
validTrails.extend(followPaths(start))

minimumCostTrail = 1e20
for trail in validTrails:
    if trail.cost < minimumCostTrail:
        minimumCostTrail = trail.cost
    prettyPrint(mazeDict, trail)

gestalt = set()
for trail in validTrails:
    gestalt.update([position for position in trail.positions])
prettyPrint(mazeDict, gestalt)

print(f"The minimum cost trail costs {minimumCostTrail}")  # 107512
print(f"The number of tiles along a good path is {len(gestalt)}")
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
