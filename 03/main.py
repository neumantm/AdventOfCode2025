
def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def get_bank_joltage_part_one(bank: str) -> int:
    first_digit = ""
    for i in reversed(range(10)):
        # do not look at last digit
        if str(i) in bank[:-1]:
            first_digit = str(i)
            break

    remaining_bank = bank.split(first_digit, 1)[1]

    second_digit = ""
    for i in reversed(range(10)):
        if str(i) in remaining_bank:
            second_digit = str(i)
            break

    return int(first_digit + second_digit)


def get_bank_joltage_part_two(bank: str) -> int:
    DIGITS = 12
    found_digits = ""
    remaining_bank = bank

    for n in reversed(range(DIGITS)):
        found_digit = ""
        for i in reversed(range(10)):
            # keep n digits after
            str_to_search_in = remaining_bank[:-n] if n > 0 else remaining_bank
            if str(i) in str_to_search_in:
                found_digit = str(i)
                break
        found_digits += found_digit
        remaining_bank = remaining_bank.split(found_digit, 1)[1]

    return int(found_digits)


def main():
    banks = [b.strip() for b in load_input()]
    sum = 0
    for bank in banks:
        joltage = get_bank_joltage_part_two(bank)
        print(f"{bank=}; {joltage=}")
        sum += joltage

    print(sum)


if __name__ == "__main__":
    main()
