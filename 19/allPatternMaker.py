from pathlib import Path
import time
import copy

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
memo = {}

for design in designs:
    designPossible = None
    validPartials = {}
    for i in range(len(design)):
        if designPossible is not None:
            break
        for partial in validPartials.get(i - 1, [""]):
            if i > 0 and validPartials.get(i - 1, [""]) == [""]:
                break
            for pattern in patterns:
                attempt = "".join(partial) + pattern

                if attempt == design[: len(attempt)]:
                    if attempt in memo:
                        validPartials[i] = memo[attempt].copy()
                        continue
                    if partial:
                        newPartial = partial + [pattern]
                        if memo.get(attempt):
                            continue
                        else:
                            memo[attempt] = [newPartial[:]]
                    else:
                        newPartial = [pattern]
                    if i in validPartials:
                        validPartials[i].append(newPartial[:])
                    else:
                        validPartials[i] = [newPartial[:]]
    completeValidDesigns = []
    for partials in validPartials.values():
        for partial in partials:
            if "".join(partial) == design:
                completeValidDesigns.append(partial)
    if not completeValidDesigns:
        designPossibilities[False].append(design)
    else:
        designPossibilities[True].append((design, len(completeValidDesigns)))

print(
    f"These designs are possible: {designPossibilities[True]}\nThese designs are impossible: {designPossibilities[False]}"
)
print(f"There are {sum([x[1] for x in designPossibilities[True]])} possible designs.")
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
