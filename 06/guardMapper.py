from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

areaMap = []
travelled = set()
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
    def __init__(self, location, facing):
        self.location = location
        self.facing = facing

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
            return None
        try:
            movingToChar = areaMap[check_coords[1]][check_coords[0]]
            if movingToChar == "#":
                self.getNextFacing()
                check_coords = self.move()
            self.location = check_coords
            return check_coords
        except IndexError:
            return None


def getStart():
    for y, row in enumerate(areaMap):
        if "^" in row:
            loc = (row.find("^"), y)
            travelled.add(loc)
            return loc


# move guard according to the rules
# moves one space in the direction facing, unless obstructed. If obstructed, turn right and move.
# def moveGuard(location, facing):
#    scalar = (all_dirs[facing][0], all_dirs[facing][1])
#    check_coords = (location[0] + scalar[0], location[1] + scalar[1])
#    if check_coords[0] < 0 or check_coords[1] < 0:
#        return None
#    try:
#        movingToChar = areaMap[check_coords[1]][check_coords[0]]
#        if movingToChar == "#":
#            facing = getNextDir(facing)
#            check_coords = moveGuard(location, facing)
#        return check_coords
#    except IndexError:
#        return None

guard = Guard(getStart(), "N")
guardLocation = guard.location
while guardLocation:
    guardLocation = guard.move()
    travelled.add(guardLocation)

travelled.remove(None)
print(travelled)
travelledMap = []
for y, line in enumerate(areaMap):
    for x, char in enumerate(line):
        if (x, y) in travelled:
            line = line[:x] + "X" + line[x + 1 :]
    travelledMap.append(line)


for line in travelledMap:
    print(line)

print(f"The guard moved to {len(travelled)} distinct locations")  # 5162
