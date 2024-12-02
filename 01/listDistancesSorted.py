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

start_time = time.perf_counter()

left_col.sort()
right_col.sort()

total = 0
for i in range(len(left_col)):
    dif = abs(left_col[i] - right_col[i])
    total += dif

end_time = time.perf_counter()

print(f"The total distance is: {total}")  # 2815556

print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
