from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"

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
    def __init__(self, map, location=None, facing="N"):
        self.map = map
        self.facing = facing
        self.travelled = []
        self.location = location
        if not self.location:
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
            if movingToChar in "#":
                self.getNextFacing()
                check_coords = self.move()
            self.location = check_coords
            self.travelled.append(self.location)
            return check_coords
        except IndexError:
            self.location = None
            return None

    def runMap(self):
        tf = []
        while self.location:
            tf.append((self.location, self.facing))
            if len(tf) != len(set(tf)):
                return True
            self.move()
        return False

    def getStart(self):
        for y, row in enumerate(self.map):
            if "^" in row:
                loc = (row.find("^"), y)
                self.travelled.append(loc)
                return loc


# def oneStepBack(location, facing):
#     scalar = (all_dirs[facing][0], all_dirs[facing][1])
#     check_coords = (location[0] - scalar[0], location[1] - scalar[1])
#     if check_coords[0] < 0 or check_coords[1] < 0:
#         return None
#     return check_coords

guard = Guard(areaMap)
guardLocation = guard.location
guard.runMap()

travelledSet = set(guard.travelled)
travelledMap = []
for y, line in enumerate(areaMap):
    for x, char in enumerate(line):
        if (x, y) in travelledSet:
            line = line[:x] + "X" + line[x + 1 :]
    travelledMap.append(line)

for line in travelledMap:
    print(line)

print(f"The guard moved to {len(travelledSet)} distinct locations")

loopsCreated = 0
for i, location in enumerate(guard.travelled):
    if i == 0:
        continue
    prev_location = guard.travelled[i - 1]
    alteredMap = areaMap.copy()
    x0, y0 = prev_location
    x, y = location
    if x0 - x == 1:
        facing = "W"
    elif x0 - x == -1:
        facing == "E"
    elif y0 - y == 1:
        facing = "N"
    elif y0 - y == -1:
        facing = "S"
    alteredMap[y] = alteredMap[y][:x] + "#" + alteredMap[y][x + 1 :]
    varientGuard = Guard(alteredMap, prev_location, facing)
    loopFound = varientGuard.runMap()
    if loopFound:
        loopsCreated += 1
        print(f"Loop created when blocking at {(y, x)}")

print(f"A total of {loopsCreated} possible loops were found.")  # 1909

# could possible speed things up by keeping travelled locations in a list. Then we could skip most of the travelled in some cases
# when testing possible loops
# would need to figure out facing direction by keeping track of corners hit
# technically doesn't need to be set in this problem cause we're not counting distinct visited.
