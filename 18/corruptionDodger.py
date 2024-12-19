from pathlib import Path
import time

filepath = Path(__file__).parent / "inputTest.txt"
MAX_SIZE = 6 + 1

start_time = time.perf_counter()


def prettyPrint(coordinates):
    for y in range(MAX_SIZE):
        print_line = ""
        for x in range(MAX_SIZE):
            if (x, y) in coordinates:
                c = "#"
            else:
                c = "."
            print_line += c
        print(print_line)
    print()


coordinates = []
with filepath.open() as file:
    for line in file:
        coordinates.append(tuple([int(c) for c in line.strip().split(",")]))

prettyPrint(coordinates[:12])

end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
