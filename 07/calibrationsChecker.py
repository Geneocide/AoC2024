from pathlib import Path
import time

filepath = Path(__file__).parent / "input.txt"
operators = ["*", "+"]


def generatePermutations(n):
    for i in range(2**n):
        yield bin(i)[2:].zfill(n)


def doOperation(terms, permutation):
    return eval(f"{terms[0]} {operators[int(permutation)]} {terms[1]}")
    # print(f"{terms[0]} {operator} {terms[1]} = {answer}")
    # return answer


start_time = time.perf_counter()
with filepath.open() as file:
    total = 0

    for line in file:
        isPossible = None
        target, numbers = line.split(":")
        target = int(target)
        terms = [int(num.strip()) for num in numbers.split()]
        for permutation in generatePermutations(len(terms) - 1):
            result = 0
            if isPossible:
                break
            for i, term in enumerate(terms):
                if i == len(terms) - 1:
                    continue
                if result == 0:
                    result = doOperation(terms[i : i + 2], permutation[i])
                else:
                    result = doOperation([result, terms[i + 1]], permutation[i])
                if result > target:
                    continue
                elif i == len(terms) - 2 and result == target:
                    print(f"Found match with permutation: {permutation}")
                    total += target
                    isPossible = True
                    break

end_time = time.perf_counter()

print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
print(f"The sum of possible calibrations is {total}")  # 1399219271639
