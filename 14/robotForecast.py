from pathlib import Path
import time


class Robot:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.endPosition = None
        self.quadrant = None

    def __str__(self):
        return f"Position: {self.position}\tVelocity: {self.velocity}\tEnd: {self.endPosition}\tQuad: {self.quadrant}"

    def move(self, seconds):
        x, y = self.position
        dx, dy = self.velocity
        x = (x + dx * seconds) % width
        y = (y + dy * seconds) % height
        self.endPosition = (x, y)

    def setQuadrant(self):
        x, y = self.endPosition
        xHalf = width // 2
        yHalf = height // 2
        if x == xHalf or y == yHalf:
            return
        if x < xHalf:
            if y < yHalf:
                self.quadrant = "NW"
                return
            if y > yHalf:
                self.quadrant = "SW"
                return
        else:
            if y < yHalf:
                self.quadrant = "NE"
                return
            if y > yHalf:
                self.quadrant = "SE"


filepath = Path(__file__).parent / "input.txt"

width = 101
height = 103
seconds = 100
if "Test" in str(filepath):
    width = 11
    height = 7

start_time = time.perf_counter()

robots = []
quadrants = dict.fromkeys(["NW", "NE", "SE", "SW"], 0)
with filepath.open() as file:
    for line in file:
        p, v = line.split(None, 1)
        x, y = [int(i) for i in p.split("=", 1)[1].strip().split(",")]
        dx, dy = [int(i) for i in v.split("=", 1)[1].strip().split(",")]
        robots.append(Robot((x, y), (dx, dy)))

print(f"room: {width} x {height}")
for robot in robots:
    robot.move(seconds)
    robot.setQuadrant()
    print(robot)
    for quadrant in quadrants:
        if robot.quadrant == quadrant:
            quadrants[quadrant] += 1

print(quadrants)
safetyFactor = 1
for value in quadrants.values():
    safetyFactor *= value
print(f"The safety factor is {safetyFactor}")  # 231221760


end_time = time.perf_counter()
print(f"Elapsed time: {(end_time - start_time):.6f} seconds")
