# it occurred to me later that this would probably be more efficient if I sorted the lists once instead of using min()
# so that is what listDistancesSorted.py is. It's about 33x faster

from pathlib import Path
import time

filepath = Path(__file__).parent / "input.txt"

with open(filepath, "r") as file:
    left_col = []
    right_col = []
    for line in file:
        left, right = line.split()
        left_col.append(int(left))
        right_col.append(int(right))

total = 0
start_time = time.perf_counter()
while len(left_col) > 0:
    left_smol = min(left_col)
    right_smol = min(right_col)
    dif = abs(left_smol - right_smol)
    total += dif
    left_col.remove(left_smol)
    right_col.remove(right_smol)
end_time = time.perf_counter()

print(f"The total distance is: {total}")  # 2815556
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
