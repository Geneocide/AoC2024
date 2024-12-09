from pathlib import Path
import time
import numpy as np

filepath = Path(__file__).parent / "input.txt"

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
expanded = np.array([])
for i in range(len(spaces)):
    if files:
        firstFile = files.pop(0)
        expanded = np.append(expanded, firstFile)
        while files and spaces[i] > len(files[-1]):
            file = files.pop()
            expanded = np.append(expanded, file)
            spaces[i] -= len(file)
        filler = []
        for j in range(spaces[i]):
            if files:
                filler.append(files[-1].pop())
            else:
                break
        expanded = np.append(expanded, filler)
    else:
        break

print(expanded)

checksum = 0
for i, fileIndex in enumerate(expanded):
    checksum += int(fileIndex) * i

end_time = time.perf_counter()
print(
    f"The calculated checksum is {checksum}"
)  # 90603226027 too low, 7393893855706 too high, 7393886108001 too high, 6385338159127
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
