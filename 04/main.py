
def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def parse_input(input: list[str]) -> list[list[bool]]:
    return [[cell == "@" for cell in line] for line in input]


def count_rolls_in_eight_adjecent_positions(grid: list[list[bool]], y: int, x: int) -> int:
    count = 0
    for i in range(-1, 2):
        y_dash = y + i
        if y_dash < 0 or y_dash >= len(grid):
            continue
        for j in range(-1, 2):
            if i == 0 and j == 0:
                # don't count cell itself
                continue
            x_dash = x + j
            if x_dash < 0 or x_dash >= len(grid[0]):
                continue
            if grid[y_dash][x_dash]:
                count += 1

    print(f"Checking {y=}, {x=}, {count=}")

    return count


def count_accessible_rolls(grid: list[list[bool]]) -> int:
    count = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if not grid[y][x]:
                # not a roll
                continue
            if count_rolls_in_eight_adjecent_positions(grid, y, x) < 4:
                print(f"({y=}, {x=}) is accessible")
                count += 1

    return count


def count_accessible_rolls_with_removing(grid: list[list[bool]]) -> int:
    count = 0

    changes = True
    while changes:
        changes = False
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if not grid[y][x]:
                    # not a roll
                    continue
                if count_rolls_in_eight_adjecent_positions(grid, y, x) < 4:
                    print(f"({y=}, {x=}) is accessible")
                    count += 1
                    grid[y][x] = False
                    changes = True

    return count


def main():
    input_raw = load_input()
    grid = parse_input(input_raw)
    count = count_accessible_rolls_with_removing(grid)
    print(f"{count=}")


if __name__ == "__main__":
    main()
