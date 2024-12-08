from pathlib import Path
import time
import itertools
import numpy as np

filepath = Path(__file__).parent / "input.txt"


def generatePermutations(options):
    for permutation in itertools.permutations(options, 2):
        yield permutation


def prettyPrint(aMap):
    for line in aMap:
        printableLine = " ".join(line)
        print(printableLine)


def find_antinodes(p1, p2):
    directionVector = p2 - p1
    print(directionVector)

    while True:
        antinode = p1 + directionVector
        has_non_integer_coords = np.any(np.abs(antinode - np.round(antinode)) > 1e-10)
        is_outside_array = (
            antinode[0] < 0
            or antinode[0] >= aMap.shape[1]
            or antinode[1] < 0
            or antinode[1] >= aMap.shape[0]
        )
        if not has_non_integer_coords and not is_outside_array:
            print(f"Antinode at: {antinode}")
            antinodes.add(tuple(antinode))
            p1 += np.array(directionVector)
        else:
            break

    return antinodes


start_time = time.perf_counter()
aMap = []
antennas = {}
with filepath.open() as file:
    for y, line in enumerate(file):
        line = line.strip()
        for x, char in enumerate(line):
            char = char.strip()
            if char != ".":
                existing_antenae = antennas.get(char, [])
                existing_antenae.append((x, y))
                antennas[char] = existing_antenae
        aMap.append([char.strip() for char in line])

aMap = np.array(aMap)

antinodes = set()
for frequency, locations in antennas.items():
    for p1, p2 in generatePermutations(locations):
        p1 = np.array(p1)
        p2 = np.array(p2)
        distance = round(np.linalg.norm(p2 - p1))
        print(f"the distance calculate between {p1} and {p2} is {distance}")
        antinodes = find_antinodes(p1, p2)
        np.set_printoptions(precision=2, suppress=True)

for antinode in antinodes:
    aMap[int(antinode[1]), int(antinode[0])] = "#"


end_time = time.perf_counter()
prettyPrint(aMap)
print(antennas)
print(f"The number of distance antinodes in range is: {len(antinodes)}")  # 1339
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
