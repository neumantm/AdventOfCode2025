from math import ceil

def load_input() -> str:
    with open("input.txt") as f:
        return f.read()


def split_into_ranges(input: str) -> list[tuple[int, int]]:
    def turn_into_range(inputrange: str) -> tuple[int, int]:
        parts = inputrange.split("-", 1)
        return (int(parts[0]), int(parts[1]))

    return [turn_into_range(inputrange) for inputrange in input.split(",")]


def is_invalid_repated_many_times(int) -> bool:
    num_string = str(int)
    if len(num_string) < 2:
        return False
    for check_len in range(1, ceil(len(num_string) / 2) + 1):
        if len(num_string) % check_len != 0:
            continue
        first = num_string[:check_len]
        mistake = False
        for pos in range(0, len(num_string), check_len):
            if num_string[pos:pos+check_len] != first:
                mistake = True
                break
        if not mistake:
            return True
    return False


def is_invalid_repeated_twice(int) -> bool:
    num_string = str(int)
    if len(num_string) % 2 != 0:
        return False
    first_half = num_string[:ceil(len(num_string) / 2)]
    second_half = num_string[ceil(len(num_string) / 2):]

    return first_half == second_half


def find_invalid(range_to_check: tuple[int, int]) -> list[int]:
    result = []
    for i in range(range_to_check[0], range_to_check[1]+1):
        if is_invalid_repated_many_times(i):
            result.append(i)
    return result


def main():
    input = load_input()
    ranges = split_into_ranges(input)
    print(f"{ranges=}")
    sum = 0
    for range_to_check in ranges:
        invalids = find_invalid(range_to_check)
        print(f"{invalids=}")
        for invalid in invalids:
            sum += invalid

    print(sum)


if __name__ == "__main__":
    main()
