from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

all_dirs = {
    # "N": (0, -1),
    "NE": (1, -1),
    # "E": (1, 0),
    "SE": (1, 1),
    # "S": (0, 1),
    "SW": (-1, 1),
    # "W": (-1, 0),
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


def get_opposite(direction):
    return (
        direction.replace("S", "N")
        .replace("N", "S")
        .replace("E", "W")
        .replace("W", "E")
    )


search = []
with filepath.open() as file:
    for line in file:
        search.append(line.strip())

print(search)

found_count = 0
for y, line in enumerate(search):
    if y == 0 or y == len(search) - 1:  # skip edges
        continue
    for x, char in enumerate(line):
        if x == 0 or x == len(line) - 1:  # skip edges
            continue
        search_word = "MAS"
        if char == search_word[1]:
            search_word = search_word[:1] + search_word[2:]
            print(str(x) + ", " + str(y))
            dirs_to_search = list(all_dirs.keys())
            parts_found = 0
            for i in range(2):
                found_char = get_char((x, y), dirs_to_search[i], 1)
                if found_char in search_word:
                    opposite_found_char = get_char(
                        (x, y), dirs_to_search[i + 2], 1
                    )  # the +2 is getting the opposite directions of the first search because of the way the all_dirs dictionary is set up
                    if (
                        opposite_found_char != found_char
                        and opposite_found_char in search_word
                    ):
                        parts_found += 1
                    else:
                        break
            if parts_found == 2:
                print(f"Found match(es) for coords {(x, y)}")
                found_count += 1


print(f"Number of X's found: {found_count}")  # 1916
