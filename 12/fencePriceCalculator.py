from pathlib import Path
import time

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


class Crop:
    def __init__(self, label, regions=[]):
        self.label = label
        self.regions = regions

    def addRegion(self, region):
        self.regions.append(region)


class Region:
    def __init__(self, coords, crop):
        self.coords = [coords]
        self.crop = crop
        self.area = None
        self.perimeter = None

    def addGarden(self, coords):
        self.coords.append(coords)

    def display(self):
        print(f"{self.crop}: {self.coords}")


start_time = time.perf_counter()

filepath = Path(__file__).parent / "inputTest.txt"
gardens = []
with filepath.open() as file:
    for line in file.readlines():
        gardenLine = []
        for char in line.strip():
            gardenLine.append(char)
        gardens.append(gardenLine)


def prettyPrint(aMap):
    for line in aMap:
        printableLine = " ".join([str(char) for char in line])
        print(printableLine)


def assignRegion(coords, crops, gardens):
    newCrop = gardens[coords[1]][coords[0]]
    region = Region(coords, newCrop)
    if newCrop in crops:
        for existingRegions in crops.values():
            for existingRegion in existingRegions:
                for existingCoords in existingRegion.coords:
                    for dir in all_dirs:
                        new_x = all_dirs[dir][0] + existingCoords[1]
                        new_y = all_dirs[dir][1] + existingCoords[0]
                        if (new_x, new_y) == coords:
                            existingRegion.addGarden(coords)
                            return
        crops[newCrop].append(region)
    crops[newCrop] = [region]


crops = []
for y, row in enumerate(gardens):
    for x, garden in enumerate(row):
        assignRegion((x, y), crops, gardens)
        for regions in crops.values():
            for region in regions:
                region.display()


prettyPrint(gardens)
print(crops)
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
