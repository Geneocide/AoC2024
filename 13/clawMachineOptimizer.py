from pathlib import Path
import time

filepath = Path(__file__).parent / "input.txt"


class Machine:
    def __init__(self):
        self.A = None
        self.B = None
        self.prize = None

    def __str__(self):
        return f"A: {self.A}\nB: {self.B}\nPrize: {self.prize}"


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
                machine.prize = (delta[0], delta[1])
        else:
            machines.append(machine)
            machine = Machine()
    machines.append(machine)

totalTokens = 0
for machine in machines:
    # print(machine)
    prize = machine.prize
    A = machine.A
    B = machine.B
    maxA = min(int(prize[0] / A[0]), int(prize[1] / A[1]))
    maxB = min(int(prize[0] / B[0]), int(prize[1] / B[1]))
    # print(maxA)
    # print(maxB)

    solutions = []
    for i in range(100):
        for j in range(100):
            if i * A[0] + j * B[0] == prize[0] and i * A[1] + j * B[1] == prize[1]:
                solutions.append((i, j))
    # print(solutions)
    # if not solutions:
    #     print("NO SOLUTION FOUND!")
    for solution in solutions:
        tokens = 3 * solution[0] + solution[1]
        # print(f"Solution costs: {tokens}")
        totalTokens += tokens

print(f"The total tokens to get max prizes is: {totalTokens}")  # 26411 too low, 26599
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
