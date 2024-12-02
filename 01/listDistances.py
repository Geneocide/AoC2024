from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

with open(filepath, "r") as file:
    left_col = []
    right_col = []
    for line in file:
        left, right = line.split()
        left_col.append(int(left))
        right_col.append(int(right))

total = 0
while len(left_col) > 0:
    left_smol = min(left_col)
    right_smol = min(right_col)
    dif = abs(left_smol - right_smol)
    total += dif
    left_col.remove(left_smol)
    right_col.remove(right_smol)

print(f"The total distance is: {total}")
