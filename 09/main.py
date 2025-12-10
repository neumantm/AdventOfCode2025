
from statistics import median
from xmlrpc.client import Boolean


Coord = tuple[int, int]


def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def load_coordinates(input) -> list[Coord]:
    return [(int(line.split(",", 1)[0].strip()), int(line.split(",", 1)[1].strip())) for line in input]


def get_rect_area(corner1: Coord, corner2: Coord) -> int:
    x_size = abs(corner1[0] - corner2[0]) + 1  # inclusive
    y_size = abs(corner1[1] - corner2[1]) + 1  # inclusive
    return x_size * y_size


def find_larges_rect(coords: list[Coord], check_rect_against) -> int:
    largest_area: int = 0

    for i, c1 in enumerate(coords):
        print(f"checking {i} / {len(coords)}")
        for c2 in coords[i+1:]:
            area = get_rect_area(c1, c2)
            #print(f"{c1=}{c2=}{area=}")
            if area > largest_area:
                if check_rect_against(c1, c2):
                    largest_area = area

    return largest_area


def find_green_tile_border(red_tiles: list[Coord]) -> list[Coord]:
    result: list[Coord] = []
    for i in range(len(red_tiles)):
        j = len(red_tiles) - 1 if i == 0 else i - 1

        if red_tiles[i][0] == red_tiles[j][0]:
            if red_tiles[i][1] > red_tiles[j][1]:
                for y in range(red_tiles[j][1], red_tiles[i][1]):
                    result.append((red_tiles[i][0], y))
            else:
                for y in range(red_tiles[i][1], red_tiles[j][1]):
                    result.append((red_tiles[i][0], y))
        elif red_tiles[i][1] == red_tiles[j][1]:
            if red_tiles[i][0] > red_tiles[j][0]:
                for x in range(red_tiles[j][0], red_tiles[i][0]):
                    result.append((x, red_tiles[i][1]))
            else:
                for x in range(red_tiles[i][0], red_tiles[j][0]):
                    result.append((x, red_tiles[i][1]))
        else:
            raise ValueError(f"{red_tiles[i]=} and {red_tiles[j]=} not on same line for {i=} and {j=}")

    return result


def find_inside(red_tiles: list[Coord], full_border: list[Coord]) -> Coord:
    start_y = int(median([pos[1] for pos in red_tiles]))
    max_x = max([pos[0] for pos in red_tiles])
    current_pos = (-1, start_y)

    passed_borders = 0
    while current_pos[0] <= max_x:
        current_pos = (current_pos[0] + 1, current_pos[1])
        if current_pos in full_border:
            passed_borders += 1
        elif passed_borders % 2 == 1:
            # not on border due to el, not outside due to if
            return current_pos

    raise ValueError("Dod not find inside")


def debug_draw(red_tiles: list[Coord], green_border: list[Coord], fill: list[Coord]):
    for y in range(10):
        for x in range(14):
            if (x,y) in red_tiles:
                print("#", end="")
            elif (x,y) in green_border:
                print("X", end="")
            elif (x,y) in fill:
                print("+", end="")
            else:
                print(".", end="")
        print("")


def boundary_fill_4(full_border: list[Coord], pos: Coord, result_list: list[Coord]):
    # recursive variant fails due to recursion depth
    # if pos not in full_border and pos not in result_list:
    #     result_list.append(pos)
    #     boundary_fill_4(full_border, (pos[0]+1, pos[1]), result_list)
    #     boundary_fill_4(full_border, (pos[0], pos[1]+1), result_list)
    #     boundary_fill_4(full_border, (pos[0]-1, pos[1]), result_list)
    #     boundary_fill_4(full_border, (pos[0], pos[1]-1), result_list)

    to_do_list: list[Coord] = [pos]

    while len(to_do_list) > 0:
        to_check = to_do_list.pop()
        if to_check not in full_border and to_check not in result_list:
            result_list.append(to_check)
            to_do_list.append((pos[0]+1, pos[1]))
            to_do_list.append((pos[0], pos[1]+1))
            to_do_list.append((pos[0]-1, pos[1]))
            to_do_list.append((pos[0], pos[1]-1))


known_bad_coords: set[Coord] = set([])


def is_coord_in_rect(coord: Coord, smaller_x: int, smaller_y: int, larger_x: int, larger_y: int) -> Boolean:
    return coord[0] >= smaller_x and coord[0] <= larger_x and coord[1] >= smaller_y and coord[1] <= larger_y


def coord_is_inside(coord: Coord, full_border: set[Coord]) -> Boolean:
    if coord in full_border:
        return True
    if coord in known_bad_coords:
        return False
    border_crossings = 0
    on_border = False
    for x in range(0, coord[0] + 1):  # inclusive
        if (x, coord[1]) in full_border:
            on_border = True
        elif on_border:
            # just left border
            on_border = False
            border_crossings += 1
    inside = border_crossings % 2 == 1
    if not inside:
        known_bad_coords.add(coord)
    return inside


def rect_fully_in(c1: Coord, c2: Coord, full_border: set[Coord]) -> Boolean:
    if c1[0] > c2[0]:
        larger_x = c1[0]
        smaller_x = c2[0]
    else:
        larger_x = c2[0]
        smaller_x = c1[0]

    if c1[1] > c2[1]:
        larger_y = c1[1]
        smaller_y = c2[1]
    else:
        larger_y = c2[1]
        smaller_y = c1[1]

    c3 = (c1[0], c2[1])
    if not coord_is_inside(c3, full_border):
        return False
    c4 = (c2[0], c1[1])
    if not coord_is_inside(c4, full_border):
        return False

    for badc in known_bad_coords:
        if is_coord_in_rect(badc, smaller_x, smaller_y, larger_x, larger_y):
            return False

    on_boarder = False
    for x in range(smaller_x, larger_x + 1):
        to_check = (x, smaller_y)
        if to_check in full_border:
            on_boarder = True
        elif on_boarder:
            # just left border
            on_boarder = False
            if not coord_is_inside(to_check, full_border):
                return False

    on_boarder = False
    for x in range(smaller_x, larger_x + 1):
        to_check = (x, larger_y)
        if to_check in full_border:
            on_boarder = True
        elif on_boarder:
            # just left border
            on_boarder = False
            if not coord_is_inside(to_check, full_border):
                return False

    on_boarder = False
    for y in range(smaller_y, larger_y + 1):
        to_check = (smaller_x, y)
        if to_check in full_border:
            on_boarder = True
        elif on_boarder:
            # just left border
            on_boarder = False
            if not coord_is_inside(to_check, full_border):
                return False

    on_boarder = False
    for y in range(smaller_y, larger_y + 1):
        to_check = (larger_x, y)
        if to_check in full_border:
            on_boarder = True
        elif on_boarder:
            # just left border
            on_boarder = False
            if not coord_is_inside(to_check, full_border):
                return False

    # Brute force was to slow even with these optimizations.

    # for badc in known_bad_coords:
    #     if is_coord_in_rect(badc, smaller_x, smaller_y, larger_x, larger_y):
    #         return False

    # for y in range(smaller_y, larger_y + 1, 1 + abs(larger_y - smaller_y) // 100):
    #     for x in range(smaller_x, larger_x + 1, 1 + abs(larger_x - smaller_x) // 100):
    #         if (x, y) not in filled_area:
    #             known_bad_coords.add((x,y))
    #             return False

    # for y in range(smaller_y, larger_y + 1, 1 + abs(larger_y - smaller_y) // 1000):
    #     for x in range(smaller_x, larger_x + 1, 1 + abs(larger_x - smaller_x) // 1000):
    #         if (x, y) not in filled_area:
    #             known_bad_coords.add((x,y))
    #             return False

    # for y in range(smaller_y, larger_y + 1):
    #     for x in range(smaller_x, larger_x + 1):
    #         if (x, y) not in filled_area:
    #             known_bad_coords.add((x,y))
    #             return False

    return True


def main():
    input = load_input()
    red_tiles = load_coordinates(input)
    largest_area = find_larges_rect(red_tiles, lambda c1, c2: True)
    print(f"{largest_area=}")

    green_border = find_green_tile_border(red_tiles)

    print("Got Green Border")

    full_border = red_tiles + green_border
    full_border_set = set(full_border)

    # inside = find_inside(red_tiles, full_border)
    inside = (2220, 50092)

    print(f"Got Inside: {inside=}")

    # fill: list[Coord] = list()
    # boundary_fill_4(full_border, inside, fill)

    # print("Got Fill")

    # debug_draw(red_tiles, green_border, [inside])

    largest_area_without_other_color = find_larges_rect(red_tiles, lambda c1, c2: rect_fully_in(c1, c2, full_border_set))
    print(f"{largest_area_without_other_color=}")


if __name__ == "__main__":
    main()
