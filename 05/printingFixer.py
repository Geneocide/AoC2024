from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

cantBeBefore = {}
with filepath.open() as file:
    rules, printsTemp = file.read().split("\n\n")
    rules = rules.split("\n")
    printsTemp = printsTemp.split("\n")
    prints = []
    for printing in printsTemp:
        prints.append([int(num) for num in printing.split(",")])
    for rule in rules:
        left, right = [int(num) for num in rule.split("|")]
        if right in cantBeBefore.keys():
            cantBeBefore[right].add(left)
        else:
            cantBeBefore[right] = {left}


def getMiddle(print):
    return print[int((len(print) - 1) / 2)]


invalidPrints = []
for printing in prints:
    isValid = True
    for i, page in enumerate(printing):
        pagesThisPageIsAfter = printing[:i]
        pagesThisPageIsBefore = printing[i + 1 :]
        if page in cantBeBefore.keys():
            if cantBeBefore[page].intersection(set(pagesThisPageIsBefore)):
                isValid = False
                break
    if not isValid:
        invalidPrints.append(printing)


def getMaxIndex(original, subset):
    max_index = 100000000
    for value in subset:
        index = original.index(value)
        if max_index == 100000000 or index > max_index:
            max_index = index

    return max_index


for printing in invalidPrints:
    isValid = False
    while not isValid:
        for i, page in enumerate(printing):
            pagesThisPageIsAfter = printing[:i]
            pagesThisPageIsBefore = printing[i + 1 :]
            if page in cantBeBefore.keys():
                intersection = cantBeBefore[page].intersection(
                    set(pagesThisPageIsBefore)
                )
                if intersection:
                    moving_to_index = getMaxIndex(printing, intersection)
                    movingPage = printing.pop(i)
                    printing.insert(moving_to_index, movingPage)
                    break
            if i == len(printing) - 1:
                isValid = True


total = 0
for printing in invalidPrints:
    total += getMiddle(printing)

print(f"The sum of the middle page in the valid prints is {total}")  # 6305
