from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

all_dirs = {
    "N": (0, -1),
    "NE": (1, -1),
    "E": (1, 0),
    "SE": (1, 1),
    "S": (0, 1),
    "SW": (-1, 1),
    "W": (-1, 0),
    "NW": (-1, -1),
}


def get_char(base_coords, direction, distance):
    scalar = (all_dirs[direction][0] * distance, all_dirs[direction][1] * distance)
    check_coords = (base_coords[0] + scalar[0], base_coords[1] + scalar[1])
    if check_coords[0] < 0 or check_coords[1] < 0:
        return None
    try:
        return search[check_coords[1]][check_coords[0]]
    except IndexError:
        return None


search = []
with filepath.open() as file:
    for line in file:
        search.append(line.strip())

print(search)

found_count = 0
search_word = "XMAS"
for y, line in enumerate(search):
    for x, char in enumerate(line):
        if char == search_word[0]:
            dirs_to_search = list(all_dirs.keys())
            print(str(x) + ", " + str(y))
            # could increase efficiency by eliminating directions that would go out of scope early somehow
            for i, next_char in enumerate(search_word[1:], 1):
                for j in range(
                    len(dirs_to_search) - 1, -1, -1
                ):  # iterate backward to avoid weirdness when removing direction
                    direction = dirs_to_search[j]
                    found_char = get_char((x, y), direction, i)
                    if found_char != next_char:
                        dirs_to_search.remove(direction)
            print(f"Found match(es) for coords {(x, y)} in {dirs_to_search}")
            found_count += len(dirs_to_search)

print(f"Number of {search_word} found: {found_count}")  # 2554
