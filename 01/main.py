
from math import floor


DIAL_START = 50
DIAL_MAX = 99


def rotate_by(current_number: int, amount: int) -> tuple[int, int]:
    """
    returns new number and amount of zero-passes
    """
    print()
    print(f"{amount=}")

    modulo_num = DIAL_MAX + 1

    before_mod = (current_number + amount)
    new_number = before_mod % modulo_num

    zero_passes = floor(abs(before_mod) / modulo_num)

    print(zero_passes)

    if amount < 0 and current_number < new_number and current_number != 0:
        zero_passes += 1
        print("add for going through zero from right")

    if amount < 0 and new_number == 0:
        zero_passes += 1
        print("add for landing at zero from right")

    print(zero_passes)

    return new_number, zero_passes

def rotate_by_brute_force(current_number: int, amount: int) -> tuple[int, int]:
    """
    returns new number and amount of zero-passes
    """

    num = current_number
    zero_passes = 0

    for i in range(abs(amount)):
        if amount > 0:
            num += 1
        else:
            num -= 1
        if num > DIAL_MAX:
            num = 0
        if num < 0:
            num = DIAL_MAX
        if num == 0:
            zero_passes += 1

    return num, zero_passes


def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def turn_instruction_into_offset(instruction: str) -> int:
    if instruction[0] == "L":
        return -1 * int(instruction[1:])
    elif instruction[0] == "R":
        return int(instruction[1:])
    else:
        raise ValueError("Instructions needs to start with L or R")


def main():
    instrucions = load_input()

    offsets = [turn_instruction_into_offset(instruction) for instruction in instrucions]

    dial_pos = DIAL_START
    zero_count = 0
    for offset in offsets:
        dial_pos, zero_passes = rotate_by_brute_force(dial_pos, offset)
        print(f"{dial_pos=}, {zero_passes=}")
        zero_count += zero_passes

    print(zero_count)


if __name__ == "__main__":
    main()
