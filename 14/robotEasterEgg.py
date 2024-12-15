from pathlib import Path
import pygame
import time


class Robot:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __str__(self):
        return f"Position: {self.position}\tVelocity: {self.velocity}\tEnd: {self.endPosition}\tQuad: {self.quadrant}"

    def move(self, seconds):
        x, y = self.position
        dx, dy = self.velocity
        x = (x + dx * seconds) % WIDTH
        y = (y + dy * seconds) % HEIGHT
        self.position = (x, y)


def drawMap(robots):
    screen.fill(BLACK)
    for robot in robots:
        x, y = robot.position
        pygame.draw.rect(
            screen, ROBOT_COLOR, (x * SCALE, y * SCALE, 1 * SCALE, 1 * SCALE)
        )  # Draw robot as a 1x1 pixel
    pygame.display.flip()  # Update the display


filepath = Path(__file__).parent / "input.txt"

SCALE = 10
WIDTH = 101
HEIGHT = 103
SECONDS = 0
BLACK = (0, 0, 0)
ROBOT_COLOR = (7, 86, 0)  # Green for robots
if "Test" in str(filepath):
    WIDTH = 11
    HEIGHT = 7


pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Robot Simulation")

robots = []
quadrants = dict.fromkeys(["NW", "NE", "SE", "SW"], 0)
with filepath.open() as file:
    for line in file:
        p, v = line.split(None, 1)
        x, y = [int(i) for i in p.split("=", 1)[1].strip().split(",")]
        dx, dy = [int(i) for i in v.split("=", 1)[1].strip().split(",")]
        robots.append(Robot((x, y), (dx, dy)))

running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                paused = not paused
            elif event.button == 3:
                SECONDS += 1000
                for robot in robots:
                    robot.move(1000)
                pygame.display.set_caption(
                    f"Robot Simulation - after {SECONDS} seconds"
                )
                drawMap(robots)
        elif event.type == pygame.MOUSEWHEEL:
            SECONDS += event.y * 10
            for robot in robots:
                robot.move(event.y * 10)
            pygame.display.set_caption(f"Robot Simulation - after {SECONDS} seconds")
            drawMap(robots)

    if not paused:
        pygame.display.set_caption(f"Robot Simulation - after {SECONDS} seconds")
        drawMap(robots)

        for robot in robots:
            robot.move(1)
        SECONDS += 1
    time.sleep(0.1)

pygame.quit  # 6771
