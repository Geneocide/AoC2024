from pathlib import Path
import time

filepath = Path(__file__).parent / "inputTest2.txt"


def doOperation(terms, operator):
    answer = eval(f"{terms[0]} {operator} {terms[1]}")
    # print(f"{terms[0]} {operator} {terms[1]} = {answer}")
    return answer


def checkPossibilities(terms, operators, answer, depth=0, memo={}):
    if len(terms) == 1:
        return [terms[0]]

    if tuple(terms) in memo:
        return memo[tuple(terms)]

    evaluations = set()
    for i in range(1, len(terms)):
        left = checkPossibilities(terms[:i], operators, answer, depth + 1, memo)
        right = checkPossibilities(terms[i:], operators, answer, depth + 1, memo)
        for l in left:
            for r in right:
                for op in operators:
                    evaluation = doOperation([l, r], op)
                    if evaluation <= answer:
                        evaluations.add(evaluation)
                        if depth == 0 and evaluation == answer:
                            return evaluations
                    elif op == "+":
                        break
    memo[tuple(terms)] = evaluations
    return evaluations


start_time = time.perf_counter()
with filepath.open() as file:
    total = 0

    operators = ["+", "*"]
    for line in file:
        isPossible = None
        answer, numbers = line.split(":")
        answer = int(answer)
        terms = [int(num.strip()) for num in numbers.split()]
        possibilities = checkPossibilities(terms, operators, answer)
        if answer in possibilities:
            total += answer
end_time = time.perf_counter()

print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
print(f"The sum of possible calibrations is {total}")  # 1399219475222 too high
