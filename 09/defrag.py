from pathlib import Path
import time
import numpy as np

filepath = Path(__file__).parent / "inputTest.txt"

start_time = time.perf_counter()

with filepath.open() as file:
    original = file.read().strip()

fileSizes = original[::2]
spaces = [int(char) for char in original[1::2]]

print(fileSizes)
print(spaces)

files = []
for i in range(len(fileSizes)):
    str_i = str(i)
    file = str_i * int(fileSizes[i])
    digits = len(str_i)
    file = [file[j : j + digits] for j in range(0, len(file), digits)]
    files.append(file)

print(files)

spaceFiles = {}
for i in range(len(files) - 1, 0, -1):
    if i > len(files):
        continue
    for j in range(len(spaces) - 1):
        if spaces[j] >= len(files[i]):
            if j in spaceFiles:
                spaceFiles[j] += files[i]
            else:
                spaceFiles[j] = files[i]
            spaces[j] -= len(files[i])
            if i < len(spaces):
                spaces[i] += len(files[i]) + spaces[i - 1]
                del spaces[i - 1]
            files[i] = []
            break

print(spaceFiles)
print(spaces)

expanded = np.array([])
for i, file in enumerate(files):
    expanded = np.append(expanded, files[i])
    if i in spaceFiles:
        expanded = np.append(expanded, spaceFiles[i])
    if i != len(spaces):
        if spaces[i] > 0:
            expanded = np.append(expanded, list("." * spaces[i]))

print(expanded)

checksum = 0
for i, fileIndex in enumerate(expanded):
    if fileIndex == ".":
        continue
    checksum += int(fileIndex) * i

end_time = time.perf_counter()
print(f"The calculated checksum is {checksum}")
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
