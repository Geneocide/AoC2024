from pathlib import Path
import time
from itertools import chain
from math import log10
from functools import lru_cache


@lru_cache()
def blink(rock):
    if rock == 0:
        rock = 1
    elif (int(log10(rock)) + 1) % 2 == 0:
        rock = str(rock)
        midpoint = len(rock) // 2
        rock = [int(rock[:midpoint]), int(rock[midpoint:])]
    else:
        rock = rock * 2024
    return rock


def dictUpdate(dict, key, value):
    if key in dict:
        dict[key] += value
    else:
        dict[key] = value
    return dict


start_time = time.perf_counter()

filepath = Path(__file__).parent / "input.txt"
with filepath.open() as file:
    rocksArray = [int(rock) for rock in file.read().split()]

rocksDict = {}
for rock in rocksArray:
    rocksDict = dictUpdate(rocksDict, rock, 1)

for i in range(75):
    tempDict = {}
    for rock, count in rocksDict.items():
        rocksDict[rock] = 0
        results = blink(rock)
        if isinstance(results, list):
            for result in results:
                tempDict = dictUpdate(tempDict, result, count)
        else:
            tempDict = dictUpdate(tempDict, results, count)
    rocksDict = tempDict

print(f"Number of rocks: {sum(rocksDict.values())}")  # 240954878211138
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
