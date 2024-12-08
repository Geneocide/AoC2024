from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

areaMap = []
with filepath.open() as file:
    for line in file:
        areaMap.append(line.strip())

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


class Guard:
    def __init__(self, map):
        self.map = map
        self.facing = "N"
        self.travelled = set()
        self.location = self.getStart()

    def getNextFacing(self):
        if self.facing == "N":
            self.facing = "E"
        elif self.facing == "E":
            self.facing = "S"
        elif self.facing == "S":
            self.facing = "W"
        elif self.facing == "W":
            self.facing = "N"

    def move(self):
        scalar = (all_dirs[self.facing][0], all_dirs[self.facing][1])
        check_coords = (self.location[0] + scalar[0], self.location[1] + scalar[1])
        if check_coords[0] < 0 or check_coords[1] < 0:
            self.location = None
            return None
        try:
            movingToChar = self.map[check_coords[1]][check_coords[0]]
            if movingToChar in "#O":
                self.getNextFacing()
                check_coords = self.move()
            self.location = check_coords
            self.travelled.add(self.location)
            return check_coords
        except IndexError:
            self.location = None
            return None

    def runMap(self):
        moveCount = 0
        movesSinceNewVisited = 0
        while self.location:
            if movesSinceNewVisited > len(self.travelled):
                return True
            distinctSpacesBefore = len(self.travelled)
            self.move()
            distinctSpacesAfter = len(self.travelled)
            if distinctSpacesAfter > distinctSpacesBefore:
                movesSinceNewVisited = 0
            movesSinceNewVisited += 1
            moveCount += 1
        return False

    def getStart(self):
        for y, row in enumerate(self.map):
            if "^" in row:
                loc = (row.find("^"), y)
                self.travelled.add(loc)
                return loc


guard = Guard(areaMap)
guardLocation = guard.location
guard.runMap()

print(guard.travelled)
travelledMap = []
for y, line in enumerate(areaMap):
    for x, char in enumerate(line):
        if (x, y) in guard.travelled:
            line = line[:x] + "X" + line[x + 1 :]
    travelledMap.append(line)

for line in travelledMap:
    print(line)

print(f"The guard moved to {len(guard.travelled)} distinct locations")

loopsCreated = 0
for location in guard.travelled:
    alteredMap = areaMap.copy()
    x, y = location
    alteredMap[y] = alteredMap[y][:x] + "O" + alteredMap[y][x + 1 :]
    varientGuard = Guard(alteredMap)
    loopFound = varientGuard.runMap()
    if loopFound:
        loopsCreated += 1
        print(f"Loop created when blocking at {(y, x)}")

print(f"A total of {loopsCreated} possible loops were found.")  # 1909

# could possible speed things up by keeping travelled locations in a list. Then we could skip most of the travelled in some cases
# when testing possible loops
# would need to figure out facing direction by keeping track of corners hit
# technically doesn't need to be set in this problem cause we're not counting distinct visited.
