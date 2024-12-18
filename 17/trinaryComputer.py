from pathlib import Path
import time

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
with filepath.open() as file:
    for line in file:
        if line.strip():
            label, value = line.split(":")
            if "Re" in label:
                registers[label.split()[1]] = int(value)
            else:
                program = [int(i) for i in value.split(",")]

print(registers)
print(program)

instructionPointer = 0
output = []
while instructionPointer in range(len(program)):
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

print(f"Device output is {','.join(output)}")  # 1,7,2,1,4,1,5,4,0
end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
