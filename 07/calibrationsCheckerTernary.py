from pathlib import Path
import time
import itertools

filepath = Path(__file__).parent / "inputTest.txt"
firstOperators = ["*", "+"]
secondOperators = ["||", "*", "+"]


def generatePermutations(options, length):
    for permutation in itertools.product(options, repeat=length):
        yield permutation


def generatePermutationsRequired(options, length):
    for permutation in itertools.product(options, repeat=length):
        if "||" in permutation:
            yield permutation


def doOperation(terms, operation):
    if operation == "||":
        return int(str(terms[0]) + str(terms[1]))
    return eval(f"{terms[0]} {operation} {terms[1]}")
    # print(f"{terms[0]} {operator} {terms[1]} = {answer}")
    # return answer


def prettyPrint(terms, permutation, target):
    result = ""
    for i in range(len(terms)):
        result += str(terms[i])
        if i < len(terms) - 1:
            result += f" {permutation[i]} "
    result += f" = {target}"
    return result


def tryPermutations(target, terms, operators):
    isPossible = None
    permutationFunction = (
        generatePermutationsRequired if len(operators) == 3 else generatePermutations
    )
    for permutation in permutationFunction(operators, len(terms) - 1):
        result = 0
        if isPossible:
            return True
        for i in range(len(terms)):
            if i == len(terms) - 1:
                continue
            if result == 0:
                result = doOperation(terms[i : i + 2], permutation[i])
            else:
                result = doOperation([result, terms[i + 1]], permutation[i])
            if result > target:
                continue
            elif i == len(terms) - 2 and result == target:
                print(
                    f"Found match with permutation: {prettyPrint(terms, permutation, target)}"
                )
                return True
    return False


start_time = time.perf_counter()
tryAgain = []
with filepath.open() as file:
    total = 0

    for line in file:
        isPossible = None
        target, numbers = line.split(":")
        target = int(target)
        terms = [int(num.strip()) for num in numbers.split()]
        isPossible = tryPermutations(target, terms, firstOperators)
        if isPossible:
            total += target
        # for permutation in generatePermutations(operators, len(terms) - 1):
        #     result = 0
        #     if isPossible:
        #         break
        #     for i, term in enumerate(terms):
        #         if i == len(terms) - 1:
        #             continue
        #         if result == 0:
        #             result = doOperation(terms[i : i + 2], permutation[i])
        #         else:
        #             result = doOperation([result, terms[i + 1]], permutation[i])
        #         if result > target:
        #             continue
        #         elif i == len(terms) - 2 and result == target:
        #             print(
        #                 f"Found match with permutation: {prettyPrint(terms, permutation, target)}"
        #             )
        #             total += target
        #             isPossible = True
        #             break
        if not isPossible:
            tryAgain.append((target, terms))

end_time = time.perf_counter()

print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
print(f"The sum of possible calibrations is {total}")  # 1399219271639

start_time = time.perf_counter()

for calibration in tryAgain:
    target, terms = calibration
    isPossible = tryPermutations(target, terms, secondOperators)
    if isPossible:
        total += target

end_time = time.perf_counter()

print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
print(f"The sum of possible calibrations is {total}")  # 275791737999003
