from pathlib import Path
import time
from math import sqrt

filepath = Path(__file__).parent / "input.txt"
calibrationError = 10000000000000
# calibrationError = 0


class Machine:
    def __init__(self):
        self.A = None
        self.B = None
        self.prize = None
        self.solutions = []

    def __str__(self):
        return f"A: {self.A}\nB: {self.B}\nPrize: {self.prize}"

    def findSolutions(self):
        eq1, eq2 = zip(self.A, self.B, self.prize)
        x1, y1, z1 = eq1
        x2, y2, z2 = eq2

        determinant = x1 * y2 - x2 * y1
        if determinant == 0:
            return

        a = round((y2 * z1 - y1 * z2) / determinant)
        b = round((x1 * z2 - x2 * z1) / determinant)

        if a * x1 + b * y1 == z1 and a * x2 + b * y2 == z2:
            self.solutions.append((a, b))

        return


def factorize(n):
    factors = []
    for i in range(2, int(sqrt(n)) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return factors


def powerset_products(s):
    memo = set()
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1, 2**x):
        subset = [ss for mask, ss in zip(masks, s) if i & mask]
        product = 1
        for num in subset:
            product *= num
        if product in memo:
            continue
        else:
            memo.add(product)
            yield product


def processFactors(A, B, factors, target):
    solutions = []
    for factor in powerset_products(factors):
        # print(f"Direct: {factor}")
        # if factor % A == 0 or factor % B == 0:
        if A * factor < target and (target - (A * factor)) % B == 0:
            solutions.append((factor, (target - (A * factor)) / B))
            continue
        if B * factor < target and (target - (B * factor)) % A == 0:
            solutions.append(((target - (B * factor)) / A, factor))
            continue
        # if factor % A == B or factor % B == A:
        # print(f"Indirect: {factor}")
        if factor % A == B:
            AMultiple = int(factor / A)
            BMultiple = int((factor - (AMultiple * A)) / B)
            small = target / factor * BMultiple
            solutions.append(((AMultiple / BMultiple) * small, small))
            continue
        if factor % B == A:
            BMultiple = int(factor / B)
            AMultiple = int((factor - (BMultiple * B)) / A)
            small = target / factor * AMultiple
            solutions.append((small, (BMultiple / AMultiple) * small))
            continue

    return solutions


def force(A, B, target, factors):
    print("Trying force")
    factors.append(A)
    factors.append(B)
    solutions = []
    # if A > B:
    for i in range(2, max(int(target / A), int(target / B))):
        if not any([i % factor == 0 for factor in factors]):
            factors.append(i)
            if (target - (A * i)) % B == 0:
                solutions.append((i, (target - (A * i)) / B))
                continue
            if (target - (B * i)) % A == 0:
                solutions.append(((target - (B * i)) / A, i))
    # if A < B:
    #     for i in range(2, int(target / B)):
    #         if not any([i % factor == 0 for factor in factors]):
    #             if (target - (B * i)) % A == 0:
    #                 solutions.append(((target - (B * i)) / A, i))

    return solutions


start_time = time.perf_counter()

machines = []
with filepath.open() as file:
    machine = Machine()
    for line in file.readlines():
        if line.strip():
            label, data = line.strip().split(":")
            label = label.split(" ")[-1]
            data = data.split(", ")
            delta = []
            if label in "AB":
                for datum in data:
                    delta.append(int(datum.split("+")[-1]))
                if label == "A":
                    machine.A = (delta[0], delta[1])
                elif label == "B":
                    machine.B = (delta[0], delta[1])
            else:
                for datum in data:
                    delta.append(int(datum.split("=")[-1]))
                machine.prize = (
                    delta[0] + calibrationError,
                    delta[1] + calibrationError,
                )
        else:
            machines.append(machine)
            machine = Machine()
    machines.append(machine)

totalTokens = 0
for machine in machines:
    print(f"\n{machine}\n")
    prize = machine.prize

    machine.findSolutions()

    print(machine.solutions)
    if machine.solutions:
        tokens = 1e18
        for solution in machine.solutions:
            solutionTokens = 3 * solution[0] + solution[1]
            if solutionTokens < tokens:
                tokens = solutionTokens

        totalTokens += tokens

print(f"The total tokens to get max prizes is: {totalTokens}")  # 106228669504887
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
