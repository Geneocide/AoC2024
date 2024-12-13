from pathlib import Path
import time
import itertools

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


start_time = time.perf_counter()


def prettyPrint(aMap):
    for line in aMap:
        printableLine = " ".join([str(char) for char in line])
        print(printableLine)


def isAdjacent(x1, y1, x2, y2):
    if abs(x1 - x2) == 1 and y1 == y2 or abs(y1 - y2) == 1 and x1 == x2:
        return True
    return False


filepath = Path(__file__).parent / "input.txt"
gardens = []
with filepath.open() as file:
    for line in file.readlines():
        gardenLine = []
        for char in line.strip():
            gardenLine.append(char)
        gardens.append(gardenLine)
# prettyPrint(gardens)

crops = {}
for y, row in enumerate(gardens):
    for x, crop in enumerate(row):
        if crop not in crops.keys():
            crops[crop] = [[(x, y)]]
        else:
            previousRegion = None
            for region in crops[crop]:
                for garden in region:
                    if isAdjacent(*garden, x, y):
                        if not previousRegion:
                            region.append((x, y))
                            previousRegion = region
                        else:
                            previousRegion.extend(region)
                            if region in crops[crop]:
                                crops[crop].remove(region)
                        break
            if not previousRegion:
                crops[crop].append([(x, y)])


# for crop, regions in crops.items():
#     print(f"{crop}: {regions}")
totalPrice = 0
for crop, regions in crops.items():
    # regionString = ""
    for region in regions:
        area = len(region)
        adjacentPairs = 0
        for pair in itertools.permutations(region, 2):
            if isAdjacent(*pair[0], *pair[1]):
                adjacentPairs += 1
        perimeter = 4 * area - adjacentPairs
        # regionString += (
        #     f"\nArea = {area}, Perimeter = {perimeter}, Price = {area * perimeter}"
        # )
        totalPrice += area * perimeter
    # print(f"Crop {crop}: {regionString}")
end_time = time.perf_counter()
print(f"The total price of the needed fence is: {totalPrice}")  # 1494342
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
