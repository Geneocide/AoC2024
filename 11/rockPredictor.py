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


start_time = time.perf_counter()

filepath = Path(__file__).parent / "input.txt"
with filepath.open() as file:
    rocks = [int(rock) for rock in file.read().split()]

print("Initial arrangement:")
print(rocks)
for i in range(25):
    for j, rock in enumerate(rocks):
        rocks[j] = blink(rock)

    rocks = list(
        chain.from_iterable(
            [[rock] if not isinstance(rock, list) else rock for rock in rocks]
        )
    )
    # print(f"after {i+1} blinks:")
    # print(rocks)

print(f"Number of rocks: {len(rocks)}")  # 203609
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
