from pathlib import Path
import time
import itertools
import LL

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


class Region:
    def __init__(self, crop, coords):
        self.crop = crop
        self.coords = [coords]
        self.sides = set()


def prettyPrint(aMap):
    for line in aMap:
        printableLine = " ".join([str(char) for char in line])
        print(printableLine)


def isAdjacent(x1, y1, x2, y2):
    if abs(x1 - x2) == 1 and y1 == y2 or abs(y1 - y2) == 1 and x1 == x2:
        return True
    return False


def isOrthogonallyAdjacent(coords1, coords2, dir):
    if dir == "N" or dir == "S":
        if abs(coords1[0] - coords2[0]) == 1 and coords1[1] - coords2[1] == 0:
            return True
        else:
            return False
    else:
        if abs(coords1[1] - coords2[1]) == 1 and coords1[0] - coords2[0] == 0:
            return True
        else:
            return False


def getCoords(x, y, dir):
    return (all_dirs[dir][0] + x, all_dirs[dir][1] + y)


def isValid(x, y, gardens):
    if x < 0 or y < 0:
        return False
    if x >= len(gardens[0]):
        return False
    if y >= len(gardens):
        return False
    return True


def increaseSide(node, dir):
    regions = crops[node.label]
    for region in regions:
        if node.coords in region.coords:
            region.sides.add((node.coords, dir))
            if node.label == "C":
                print(f"{region.sides}")


start_time = time.perf_counter()

filepath = Path(__file__).parent / "input.txt"
gardens = []
with filepath.open() as file:
    for line in file.readlines():
        gardenLine = []
        for char in line.strip():
            gardenLine.append(char)
        gardens.append(gardenLine)
prettyPrint(gardens)

crops = {}
rows = []
for y, row in enumerate(gardens):
    rowDLL = LL.DLL()
    for x, crop in enumerate(row):
        node = LL.Node((x, y), crop)
        rowDLL.append(node)
        if crop not in crops.keys():
            # crops[crop] = [[(x, y)]]
            crops[crop] = [Region(crop, (x, y))]
        else:
            previousRegion = None
            for region in crops[crop]:
                for garden in region.coords:
                    if isAdjacent(garden[0], garden[1], x, y):
                        if not previousRegion:
                            region.coords.append((x, y))
                            previousRegion = region
                        else:
                            previousRegion.coords.extend(region.coords)
                            if region in crops[crop]:
                                crops[crop].remove(region)
                        break
            if not previousRegion:
                crops[crop].append(Region(crop, (x, y)))
    rows.append(rowDLL)

cols = []
for i in range(len(rows)):
    col = LL.DLL()
    for row in rows:
        node = row.head
        for j in range(i):
            node = node.next
        node = node.copy()
        node.next = None
        col.append(node)
    cols.append(col)

for row in rows:
    row.display()
    node = row.head
    while node:
        if not node.next or node.next.label != node.label:
            # orthogonalCoords = getCoords(*node.coords, "N")
            # if (
            #     not isValid(*orthogonalCoords, gardens)
            #     or gardens[orthogonalCoords[1]][orthogonalCoords[0]] != node.label
            # ):
            increaseSide(node, "E")
        # aboveCoords = getCoords(*node.coords, "W")
        # if not isValid(*aboveCoords, gardens) or node.label != node.prev.label:
        #     if gardens[aboveCoords[1]][aboveCoords[0]] != node.label:
        #         increaseSide(node)
        node = node.next

for row in reversed(rows):
    row.display()
    node = row.tail
    while node:
        if not node.prev or node.prev.label != node.label:
            # orthogonalCoords = getCoords(*node.coords, "S")
            # if (
            #     not isValid(*orthogonalCoords, gardens)
            #     or gardens[orthogonalCoords[1]][orthogonalCoords[0]] != node.label
            # ):
            increaseSide(node, "W")
        # belowCoords = getCoords(*node.coords, "E")
        # if not isValid(*belowCoords, gardens):
        #     increaseSide(node)
        # elif node.label != node.next.label:
        #     if gardens[belowCoords[1]][belowCoords[0]] != node.label:
        #         increaseSide(node)
        node = node.prev

for col in cols:
    col.display()
    node = col.head
    while node:
        if not node.next or node.next.label != node.label:
            # orthogonalCoords = getCoords(*node.coords, "E")
            # if (
            #     not isValid(*orthogonalCoords, gardens)
            #     or gardens[orthogonalCoords[1]][orthogonalCoords[0]] != node.label
            # ):
            increaseSide(node, "S")
        # leftCoords = getCoords(*node.coords, "N")
        # if not isValid(*leftCoords, gardens) or node.label != node.prev.label:
        #     if gardens[leftCoords[1]][leftCoords[0]] != node.label:
        #         increaseSide(node)
        node = node.next

for col in reversed(cols):
    col.display()
    node = col.tail
    while node:
        if not node.prev or node.prev.label != node.label:
            # orthogonalCoords = getCoords(*node.coords, "W")
            # if (
            #     not isValid(*orthogonalCoords, gardens)
            #     or gardens[orthogonalCoords[1]][orthogonalCoords[0]] != node.label
            # ):
            increaseSide(node, "N")
        # rightCoords = getCoords(*node.coords, "S")
        # if not isValid(*rightCoords, gardens):
        #     increaseSide(node)
        # elif node.label != node.next.label:
        #     if gardens[rightCoords[1]][rightCoords[0]] != node.label:
        #         increaseSide(node)
        node = node.prev

for regions in crops.values():
    for region in regions:
        sidesToRemove = set()
        for dir in all_dirs:
            sameSideSides = [side[0] for side in region.sides if side[1] == dir]
            for pair in itertools.combinations(sameSideSides, 2):
                if isOrthogonallyAdjacent(*pair, dir):
                    if dir == "N" or dir == "S":
                        if pair[0][0] < pair[1][0]:
                            sidesToRemove.add((pair[1], dir))
                        else:
                            sidesToRemove.add((pair[0], dir))
                    else:
                        if pair[0][1] < pair[1][1]:
                            sidesToRemove.add((pair[1], dir))
                        else:
                            sidesToRemove.add((pair[0], dir))
        for side in sidesToRemove:
            print(f"for region {region.crop}: removing {side}")
            region.sides.remove(side)


# for crop, regions in crops.items():
#     print(f"{crop}: {regions}")
totalPrice = 0
for crop, regions in crops.items():
    regionString = ""
    for region in regions:
        area = len(region.coords)
        # adjacentPairs = 0
        # for pair in itertools.permutations(region.coords, 2):
        #     if isAdjacent(*pair[0], *pair[1]):
        #         adjacentPairs += 1
        regionString += f"\nArea = {area}, Sides = {len(region.sides)}, Price = {area * len(region.sides)}"
        totalPrice += area * len(region.sides)
    print(f"Crop {crop}: {regionString}")
end_time = time.perf_counter()
print(f"The total price of the needed fence is: {totalPrice}")  # 893676
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")

# import file data
# make map
# go through map, link adjacents together (E and S are next, W and N or prev)
# make regions of nodes like we did coords previously
# for each node check adjacents
# for each direction
# if adjacent is not the same crop then it's a side
# unless there is another, previous, orthogonal adjacent that has already counted that as a side
# another way to think of it might be go down the line, add 1 side to each region the first time you see that region
# and only remeber the last garden
# any gap would mean a corner which would mean a new side so only need to go back one to check
# store side count in region, not crop level, but any adjacent crop would be the same region so that helps
# do new price math Price = Area * Sides

# misc
# could store regions as a LL, it would make displaying them possible
# not sure it's efficient
# not sure it's necessary
