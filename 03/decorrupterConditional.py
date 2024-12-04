from pathlib import Path
import re

filepath = Path(__file__).parent / "input.txt"
decorrupt_pattern = r"mul\(\d{1,3},\d{1,3}\)"
extract_pattern = r"(\d+),(\d+)"

with filepath.open() as file:
    memory = file.read()

dont_chunks = memory.split("don't()")
do_chunks = (
    []
)  # saving pieces that need to be interpretted as a array. Could do 1 string, not sure if better
for i, chunk in enumerate(dont_chunks):
    if i == 0:  # first part of the file is to be interpreted
        do_chunks.append(chunk)
    if (
        i > 0
    ):  # for each chunk that starts with "dont() split on the first do() and save after that"
        if chunk.__contains__("do()"):
            dont, do = chunk.split("do()", 1)
            do_chunks.append(do)

total = 0
for chunk in do_chunks:
    decorrupted = re.findall(decorrupt_pattern, chunk)
    for command in decorrupted:
        x, y = map(int, re.search(extract_pattern, command).groups())
        total += x * y

print(f"The total is: {total}")  # 70478672
