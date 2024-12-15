from pathlib import Path
import time

filepath = Path(__file__).parent / "input.txt"
start_time = time.perf_counter()
with filepath.open() as file:
    lines = [line.rstrip() for line in file]

x_bound = len(lines[0]) * 2
aMap = dict()
all_dirs = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}
moves = []
robot = tuple()
switch = False
for y, this_line in enumerate(lines):
    if this_line == "":
        y_bound = y
        switch = True
    if not switch:
        for x, this_char in enumerate(this_line):
            if this_char == "@":
                robot = (x * 2, y)
                aMap[(x * 2, y)] = "@"
                aMap[(x * 2 + 1, y)] = "."
            elif this_char == "O":
                aMap[(x * 2, y)] = "["
                aMap[(x * 2 + 1, y)] = "]"
            else:
                aMap[(x * 2, y)] = this_char
                aMap[(x * 2 + 1, y)] = this_char
    else:
        for this_char in this_line:
            moves.append(this_char)


def prettyPrint(aMap: dict):
    print()
    for py in range(y_bound):
        print_line = ""
        for px in range(x_bound):
            c = aMap[(px, py)]
            if c == "#":
                c = "🟫"
            elif c == ".":
                c = "⬛"
            elif c in "O[":
                c = "📦"
            elif c == "]":
                c = "📦"
            elif c == "@":
                c = "🤖"
            print_line += c
        print(print_line)
    print()


for move in moves:
    dx, dy = all_dirs[move]  # Get the direction we're moving in
    move_possible = True  # If we hit a wall, this will turn False
    movers = {
        robot: aMap[robot]
    }  # Things that will move if move_possible is still True at the end
    rx, ry = robot
    to_check = [(rx, ry)]
    # Since we could potentially be moving lots of stuff at once, we'll keep a queue of things we're going to move
    # that we need to check we have room for. When moving horizontally, we'll only add the far side of a box to this
    # queue, since that's the side that could potentially hit a wall. When moving vertically, we'll add both sides of
    # each box to the queue since either side could hit a wall (or a new box).
    while to_check:
        cx, cy = to_check.pop()  # My actual location
        mx, my = cx + dx, cy + dy  # The location I want to move to
        if move in "<>":
            if aMap[(mx, my)] in "[]":
                # We are moving horizontally and we found the side of the box. Add it and the other side to the movers
                # dictionary and then add the far side of the box to the queue to make sure it has room to move
                movers[(mx, my)] = aMap[(mx, my)]
                movers[(mx + dx, my)] = aMap[(mx + dx, my)]
                to_check.append((mx + dx, my))
            elif aMap[(mx, my)] == "#":
                # We found a wall. No move is possible. Stop checking.
                move_possible = False
                break
        elif move in "^v":
            if aMap[(mx, my)] == "[":
                # We are moving vertically and we found the left side of a box. Add it and the right side to the
                # movers dictionary and then add both sides to the queue to make sure it has room to move
                movers[(mx, my)] = aMap[(mx, my)]
                movers[(mx + 1, my)] = aMap[(mx + 1, my)]
                to_check.extend([(mx, my), (mx + 1, my)])
            elif aMap[(mx, my)] == "]":
                # We are moving vertically and we found the right side of a box. Add it and the left side to the movers
                # dictionary and then add both sides tot he queue to make sure it has room to move
                movers[(mx, my)] = aMap[(mx, my)]
                movers[(mx - 1, my)] = aMap[(mx - 1, my)]
                to_check.extend([(mx, my), (mx - 1, my)])
            elif aMap[(mx, my)] == "#":
                # We found a wall. No move is possible. Stop checking.
                move_possible = False
                break

    if move_possible:
        # Set all the original locations to '.' in the warehouse_map
        for this_loc in movers:
            aMap[this_loc] = "."
        # Move everyone to their new location
        for this_mover in movers:
            mx, my = this_mover
            aMap[(mx + dx, my + dy)] = movers[this_mover]
        robot = (rx + dx, ry + dy)
        aMap[robot] = "@"

    # prettyPrint(aMap)

totalGPS = 0
for coord in aMap:
    cx, cy = coord
    if aMap[coord] == "[":
        totalGPS += cx + 100 * cy
prettyPrint(aMap)
print(f"The total GPS coordinates is: {totalGPS}")  # 1472235

end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
