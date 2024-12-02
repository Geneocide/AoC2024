from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

with filepath.open() as file:
    reports = [[int(char) for char in line.split()] for line in file]

safeCount = 0
for report in reports:
    isLeftSmaller = None
    isSafe = False
    for i in range(len(report) - 1):
        left = report[i]
        right = report[i + 1]
        if abs(left - right) > 3 or left == right:  # unsafe
            break
        if isLeftSmaller is None:
            isLeftSmaller = left < right
        if (left < right) != isLeftSmaller:  # unsafe, changed directions
            break
        if i == len(report) - 2:
            isSafe = True
    if isSafe:
        safeCount += 1
        print(f"{report} being added as safe")

print(f"Safe reports count: {safeCount}")  # 321
