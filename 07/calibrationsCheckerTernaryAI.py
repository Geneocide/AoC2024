from pathlib import Path
import time
import itertools
from functools import lru_cache
import concurrent.futures

filepath = Path(__file__).parent / "input.txt"
firstOperators = ["*", "+"]
secondOperators = ["||", "*", "+"]


@lru_cache(maxsize=None)
def doOperation(terms, operation):
    if operation == "||":
        return int(str(terms[0]) + str(terms[1]))
    elif operation == "*":
        return terms[0] * terms[1]
    elif operation == "+":
        return terms[0] + terms[1]


def prettyPrint(terms, permutation, target):
    result = ""
    for i in range(len(terms)):
        result += str(terms[i])
        if i < len(terms) - 1:
            result += f" {permutation[i]} "
    result += f" = {target}"
    return result


def tryPermutations(target, terms, operators):
    permutationFunction = (
        generatePermutationsRequired if len(operators) == 3 else generatePermutations
    )
    for permutation in permutationFunction(operators, len(terms) - 1):
        result = 0
        for i in range(len(terms) - 1):
            if result == 0:
                result = doOperation((terms[i], terms[i + 1]), permutation[i])
            else:
                result = doOperation((result, terms[i + 1]), permutation[i])
            if result > target:
                break
            elif i == len(terms) - 2 and result == target:
                print(
                    f"Found match with permutation: {prettyPrint(terms, permutation, target)}"
                )
                return target
    return False


def generatePermutations(options, length):
    return itertools.product(options, repeat=length)


def generatePermutationsRequired(options, length):
    return (p for p in itertools.product(options, repeat=length) if "||" in p)


def process_lines(lines):
    results = []
    for line in lines:
        target, numbers = line.split(":")
        target = int(target)
        terms = [int(num.strip()) for num in numbers.split()]
        if tryPermutations(target, terms, firstOperators):
            results.append(target)
        else:
            results.append((target, terms))
    return results


start_time = time.perf_counter()
tryAgain = []
total = 0

with filepath.open() as file:
    lines = file.readlines()

# Process lines in batches
batch_size = 10
with concurrent.futures.ThreadPoolExecutor() as executor:
    for batch_start in range(0, len(lines), batch_size):
        batch = lines[batch_start : batch_start + batch_size]
        batch_results = executor.submit(process_lines, batch).result()
        for result in batch_results:
            if isinstance(result, tuple):
                tryAgain.append(result)
            else:
                total += result

end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
print(f"The sum of possible calibrations is {total}")

start_time = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(tryPermutations, element[0], element[1], secondOperators)
        for element in tryAgain
    ]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if isinstance(result, int):
            total += result
    # for target, terms in tryAgain:
    #     if tryPermutations(target, terms, secondOperators):
    #         total += target

end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
print(f"The sum of possible calibrations is {total}")
