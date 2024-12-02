# AI version seems to be slower

from pathlib import Path
import time

filepath = Path(__file__).parent / "input.txt"

with filepath.open() as file:
    reports = [[int(char) for char in line.split()] for line in file]


def pairChecker(left, right, isAscending):
    if abs(left - right) > 3 or left == right:  # unsafe
        return False
    if (left < right) != isAscending:  # unsafe, changed directions
        return False
    return True


# altered by the AI
# the zip creates every left right pair we want, it seems to match indexes of arrays, so if you create a second
# array that starts at the second element it works
# enumerate just is there for the i to funcation
def reportChecker(report):
    isAscending = report[0] < report[1]  # determines ascending or descending
    for i, (left, right) in enumerate(zip(report, report[1:])):
        isPairSafe = pairChecker(left, right, isAscending)
        if not isPairSafe:
            return i
    return None


# AI helped with this one a bit. Returning None when a safe report is found is efficient. I just didn't think
# of it though because of how I got to this solution
def dampen(report, unsafeIndex):
    mod1 = report[:unsafeIndex] + report[(unsafeIndex + 1) :]
    if reportChecker(mod1) is None:
        return None

    mod2 = report[: (unsafeIndex + 1)] + report[(unsafeIndex + 2) :]
    if reportChecker(mod2) is None:
        return None

    if unsafeIndex > 0:
        modFirst = report[1:]
        if reportChecker(modFirst) is None:
            return None

    return reportChecker(mod1)


start_time = time.perf_counter()
safeCount = 0
for report in reports:
    unsafeIndex = reportChecker(report)
    if unsafeIndex is not None:
        unsafeIndex = dampen(report, unsafeIndex)

    if unsafeIndex is None:
        safeCount += 1
        # print(f"{report} being added as safe")
    # else:
    # print(f"{report} is unsafe because of {report[unsafeIndex]}")
end_time = time.perf_counter()

print(f"Safe reports count: {safeCount}")  # 386
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
