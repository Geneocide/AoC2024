from pathlib import Path
import time

filepath = Path(__file__).parent / "inputTest.txt"

start_time = time.perf_counter()

patterns = []
designs = []
with filepath.open() as file:
    inputSwitch = False
    for line in file:
        if line.strip() == "":
            inputSwitch = True
            continue
        if not inputSwitch:
            patterns += [i.strip() for i in line.split(",")]
        else:
            designs.append(line.strip())

print(patterns)
print(designs)

designPossibilities = {True: [], False: []}

for design in designs:
    designPossible = None
    validPartials = {}
    for i in range(len(design)):
        if designPossible != None:
            break
        for partial in validPartials.get(i - 1, [""]):
            if i > 0 and validPartials.get(i - 1, [""]) == [""]:
                break
            for pattern in patterns:
                attempt = partial + pattern
                if attempt == design[: len(attempt)]:
                    if validPartials and i in validPartials:
                        # need to store as arrays to capture different combos
                        validPartials[i].add(partial + pattern)
                    else:
                        validPartials[i] = {partial + pattern}
    completeValidDesigns = []
    for partials in validPartials.values():
        for partial in partials:
            if partial == design:
                completeValidDesigns.append(partial)
    if not completeValidDesigns:
        designPossibilities[False].append(design)
    else:
        designPossibilities[True].append((design, len(completeValidDesigns)))

print(
    f"These designs are possible: {designPossibilities[True]}\nThese designs are impossible: {designPossibilities[False]}"
)
print(f"Overall there are {len(designPossibilities[True])} possible designs.")  # 333
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
