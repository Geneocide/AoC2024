from pathlib import Path
import time

filepath = Path(__file__).parent / "input.txt"

with filepath.open() as file:
    reports = [[int(char) for char in line.split()] for line in file]


def pairChecker(left, right, isAscending):
    if (
        abs(left - right) > 3  # max delta is 3
        or left == right  # min delta is 1
        or (left < right) != isAscending  # must continue ascending or descending
    ):  # unsafe
        return False
    return True


def reportChecker(report):
    isAscending = report[0] < report[1]  # determines ascending or descending
    for i in range(len(report) - 1):
        left = report[i]
        right = report[i + 1]
        isPairSafe = pairChecker(left, right, isAscending)
        if not isPairSafe:
            return i
    return None


def dampen(report, unsafeIndex):
    mod1 = report[:unsafeIndex] + report[(unsafeIndex + 1) :]
    mod2 = report[: (unsafeIndex + 1)] + report[(unsafeIndex + 2) :]
    modFirst = (
        None  # this is to allow a report to switch directions if that would fix it
    )
    if unsafeIndex > 0:
        modFirst = report[1:]
    unsafeIndex = reportChecker(mod1)
    if unsafeIndex is None:
        return None
    unsafeIndex = reportChecker(mod2)
    if unsafeIndex is None:
        return None
    if modFirst is not None:
        unsafeIndex = reportChecker(modFirst)
    return unsafeIndex


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
