
from functools import reduce


def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def pad_rows(input: list[str]) -> list[str]:
    max_length = max([len(row) for row in input])
    return [row.ljust(max_length) for row in input]


def find_whitespace_columns(input: list[str]) -> list[int]:
    row_length = len(input[0])
    result = []
    for i in range(row_length):
        if all([row[i] == " " for row in input]):
            result.append(i)

    return result


def split_line_by_columns(line: str, columns: list[int]) -> list[str]:
    result = [line[:columns[0]]]
    for i, _ in enumerate(columns):
        f = columns[i] + 1 # to get rid of sperator whitespace
        t = len(line)-1 if i == len(columns)-1 else columns[i+1] # line end has newline
        result.append(line[f:t])
    return result


def turn_into_columns(input: list[str]) -> list[tuple[str]]:
    # return list(zip(*[line.split() for line in input])) # we cannot loose the whitespace info for b
    whitespace_columns = find_whitespace_columns(input)
    return list(zip(*[split_line_by_columns(line, whitespace_columns) for line in input]))


def extract_numbers_from_cephalopod_column(column: list[str]) -> list[int]:
    result = []
    for i in reversed(range(len(column[0]))):
        column_num = ""
        for cell in column:
            column_num += cell[i]
        result.append(int(column_num))

    return result


def calculate_column_result(column: tuple[str], cephalopod_math: bool) -> int:
    numbers: list[int]

    if cephalopod_math:
        numbers = extract_numbers_from_cephalopod_column(list(column[:-1]))
    else:
        numbers = [int(num) for num in column[:-1]]

    print(f"{numbers=}")

    operator = column[-1].strip()
    if operator == "*":
        return reduce(lambda a,b: a*b, numbers, 1)
    elif operator == "+":
        return reduce(lambda a,b: a+b, numbers, 0)
    else:
        raise ValueError("Operator not supported: " + operator)


def caclulate_grand_total(columns: list[tuple[str]], cephalopod_math: bool) -> int:
    sum = 0
    for col in columns:
        sum += calculate_column_result(col, cephalopod_math)
    return sum


def main():
    input = load_input()
    columns = turn_into_columns(pad_rows(input))
    print(f"{columns=}")
    grand_total = caclulate_grand_total(columns, True)
    print(f"{grand_total=}")


if __name__ == "__main__":
    main()
