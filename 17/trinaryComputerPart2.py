from pathlib import Path
import time
from itertools import product

filepath = Path(__file__).parent / "input.txt"


def getOperandValue(operand):
    if operand <= 3:
        return operand
    if operand == 4:
        return registers["A"]
    if operand == 5:
        return registers["B"]
    if operand == 6:
        return registers["C"]
    if operand == 7:
        print("ERROR")


start_time = time.perf_counter()

registers = {}
program = None
output = ""
values = 0
with filepath.open() as file:
    for line in file:
        if line.strip():
            label, value = line.split(":")
            if "Re" in label:
                registers[label.split()[1]] = 0
            else:
                program = [int(i) for i in value.split(",")]

print(registers)
print(program)


def simulation(registers, program):
    instructionPointer = 0
    output = []
    while instructionPointer < len(program):
        opcode = program[instructionPointer]
        operand = program[instructionPointer + 1]
        if opcode == 0:  # adv
            operandValue = getOperandValue(operand)
            registers["A"] = int(registers["A"] / 2**operandValue)
        elif opcode == 1:  # bxl
            registers["B"] = registers["B"] ^ operand
        elif opcode == 2:  # bst
            operandValue = getOperandValue(operand)
            registers["B"] = operandValue % 8
        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                instructionPointer = operand
                continue
        elif opcode == 4:  # bxc
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:  # out
            operandValue = getOperandValue(operand)
            output.append(str(operandValue % 8))
        elif opcode == 6:  # bdv
            operandValue = getOperandValue(operand)
            registers["B"] = int(registers["A"] / 2**operandValue)
        elif opcode == 7:  # cdv
            operandValue = getOperandValue(operand)
            registers["C"] = int(registers["A"] / 2**operandValue)

        instructionPointer += 2
    return output


def octal_to_decimal(octal_number):
    """
    Convert a number from base 8 to base 10.

    :param octal_number: A string representing the octal number.
    :return: An integer representing the decimal equivalent.
    """
    try:
        # Convert the octal number (string) to a decimal integer
        decimal_number = int(octal_number, 8)
        return decimal_number
    except ValueError:
        raise ValueError("Invalid octal number")


def getTriBit():
    for i in range(8):
        yield format(i, "03b")


analysis = []
programStr = [str(i) for i in program]
goodInputs = {}
minimumInput = 9e25

for i in reversed(range(len(program))):
    targetBit = str(program[i])
    # combos = list(product(*[v for v in goodInputs.values() if v]))
    # goodInputsStrings = ["".join(combo) for combo in combos]
    goodInputsList = goodInputs.get(i + 1, [""])
    for goodInput in goodInputsList:
        goodInputString = str(goodInput)
        for value in getTriBit():
            input = int(goodInputString + value, 2)
            registers["A"] = input
            registers["B"] = 0
            registers["C"] = 0
            output = simulation(registers, program)

            goodOutput = True
            if programStr[i:] == output:
                if goodInputs and i in goodInputs:
                    goodInputs[i].add(goodInputString + value)
                else:
                    goodInputs[i] = {goodInputString + value}
                if i == 0:
                    if int(goodInputString + value, 2) < minimumInput:
                        minimumInput = int(goodInputString + value, 2)

    # add logic for if we're doing the last bit and keeping track of smallest number

print(
    f"The miniminum input that reproduces the program is: {minimumInput}"
)  # 37221261688308
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
