from typing import Any

from math import log10, floor


def rotate_ac_90(matrix: list[list[Any]]) -> list[list[Any]]:
    return list(reversed([list(row) for row in zip(*matrix)]))


def rotate_cw_90(matrix: list[list[Any]]) -> list[list[Any]]:
    return [list(row) for row in zip(*reversed(matrix))]


def flip_vertical(matrix: list[list[Any]]) -> list[list[Any]]:
    return list(reversed(matrix))


def flip_horizontal(matrix: list[list[Any]]) -> list[list[Any]]:
    return [list(reversed(row)) for row in matrix]


def print_matrix(matrix: list[list[Any]]):
    longest_cell = max([len(str(cell)) for row in matrix for cell in row])

    longest_cell = max(longest_cell, floor(log10(len(matrix))) + 1, floor(log10(len(matrix[0]))) + 1)

    def print_cell(cell: Any):
        justified = str(cell).rjust(longest_cell)
        print(f"{justified} | ", end="")

    def print_row(row: list[Any]):
        for cell in row:
            print_cell(cell)
        print("")

    print("---")

    print_row([""] + list(range(0, len(matrix[0]))))

    for i, row in enumerate(matrix):
        print_row([i] + row)


if __name__ == "__main__":
    test_matrix = [[1,2,3],
                   [4,5,6],
                   [7,8,9]]

    print_matrix(flip_horizontal(test_matrix))
    # print_matrix(test_matrix)
    # print_matrix(rotate_ac_90(test_matrix))
    # print_matrix(rotate_cw_90(test_matrix))
