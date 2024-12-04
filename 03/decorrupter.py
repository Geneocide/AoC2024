from pathlib import Path
import re

filepath = Path(__file__).parent / "input.txt"
decorrupt_pattern = r"mul\(\d{1,3},\d{1,3}\)"
extract_pattern = r"(\d+),(\d+)"

with filepath.open() as file:
    decorrupted = re.findall(decorrupt_pattern, file.read())

total = 0
for command in decorrupted:
    x, y = map(int, re.search(extract_pattern, command).groups())
    total += x * y

print(f"The total is: {total}")  # 164730528
