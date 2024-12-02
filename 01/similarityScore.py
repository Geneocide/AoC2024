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
for num in left_col:
    matches = right_col.count(num)
    score = matches * num
    total += score

print(f"The similarity score is: {total}")
