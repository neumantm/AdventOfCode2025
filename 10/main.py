
from functools import cache
from itertools import product

import time
import operator

Indicators = tuple[bool, ...]
Button = frozenset[int]
Joltages = tuple[int, ...]
Machine = tuple[Indicators, frozenset[Button], Joltages]


def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def load_machine(input_line: str) -> Machine:
    first_cut = input_line.strip().split("]", 1)
    indicator_string = first_cut[0].strip("[ ")

    second_cut = first_cut[1].split("{", 1)
    buttons_string = second_cut[0]
    joltage_string = second_cut[1].strip("} ")

    indicators = tuple(c == "#" for c in indicator_string)
    buttons = frozenset(frozenset(int(num) for num in button.strip("() ").split(",")) for button in buttons_string.split())
    joltages = tuple(int(num) for num in joltage_string.split(","))

    return indicators, buttons, joltages


def btn_to_str(btn: Button) -> str:
    return f"({", ".join((str(num) for num in btn))})"


def btn_seq_to_str(btn_seq: tuple[Button, ...]) -> str:
    return " ->".join(btn_to_str(btn) for btn in btn_seq)


@cache
def apply_button_to_indicators(indicators: Indicators, button: Button) -> Indicators:
    return tuple(not state if i in button else state for i, state in enumerate(indicators))


@cache
def apply_button_sequence_to_indicators(indicators: Indicators, sequence: tuple[Button]) -> Indicators:
    work_var = indicators
    for button in sequence:
        work_var = apply_button_to_indicators(work_var, button)
    return work_var


def brute_force_indicators(machine: Machine) -> int:
    initial_indicators = tuple([False] * len(machine[0]))
    buttons = machine[1]

    button_presses = 0

    while True:
        button_presses += 1
        button_sequences = list(product(buttons, repeat=button_presses))
        print(f"{button_presses=}")
        for sequence in button_sequences:
            #print(btn_seq_to_str(sequence))
            changed_indicators = apply_button_sequence_to_indicators(initial_indicators, sequence)
            if changed_indicators == machine[0]:
                return button_presses


@cache
def apply_button_to_joltages(joltages: Joltages, button: Button) -> Joltages:
    return tuple(value + 1 if i in button else value for i, value in enumerate(joltages))


@cache
def apply_button_sequence_to_joltages(joltages: Joltages, sequence: tuple[Button, ...]) -> Joltages:
    work_var = apply_button_sequence_to_joltages(joltages, sequence[:-1])
    return apply_button_to_joltages(work_var, sequence[-1])


def apply_button_tuple_to_joltages(joltages: Joltages, buttonTpl: Joltages) -> Joltages:
    return tuple(map(operator.add, joltages, buttonTpl))


def heuristic(joltages: Joltages, target_joltages: Joltages, target_weights: tuple[int, ...]) -> int:
    #return - sum(map(operator.mul, map(operator.sub, target_joltages, joltages), target_weights))
    return - sum(map(operator.sub, target_joltages, joltages))

# NUMBER_TIMES_CHECKED = 0
# CHECK_TOOKS = []


# def check_a_gt_b(a, b) -> bool:
#     start = time.perf_counter()
#     global NUMBER_TIMES_CHECKED, CHECK_TOOKS
#     NUMBER_TIMES_CHECKED += 1
#     res = a>b
#     CHECK_TOOKS.append(time.perf_counter() - start)
#     return res


class SearchFailedExcpetion(Exception):
    pass

def recursively_apply_button_to_joltage_until_target(
    possible_input_joltages: frozenset[Joltages],
    button_tuples: frozenset[Joltages],
    target_joltages: Joltages,
    depth: int,
    target_weights: tuple[int, ...],
    keep_best: int,
) -> int:
    # global NUMBER_TIMES_CHECKED, CHECK_TOOKS

    print(f"{depth=}, {len(possible_input_joltages)=}, {len(button_tuples)=}")
    new_possible_input_joltages: set[Joltages] = set()
#    outer_loop_start = time.perf_counter()
#    inner_loop_tooks = []
    for input_joltages in possible_input_joltages:
        for button_tuple in button_tuples:
            # NUMBER_TIMES_CHECKED = 0
            # CHECK_TOOKS = []

            output_joltages = apply_button_tuple_to_joltages(input_joltages, button_tuple)
            if output_joltages == target_joltages:
                return depth
            inner_loop_start = time.perf_counter()

            if not any(a > b for a, b in zip(output_joltages, target_joltages)):
                new_possible_input_joltages.add(output_joltages)
#            inner_loop_tooks.append(time.perf_counter() - inner_loop_start)


    # outer_loop_took = time.perf_counter() - outer_loop_start
    # inner_loop_avg = sum(inner_loop_tooks) / len(inner_loop_tooks)
    # check_avg = sum(CHECK_TOOKS) / len(CHECK_TOOKS)
    # print(f"{outer_loop_took=} {inner_loop_avg=} ") # {NUMBER_TIMES_CHECKED=} {check_avg=}

    if len(new_possible_input_joltages) == 0:
        raise SearchFailedExcpetion()
    new_inputs = frozenset(sorted(new_possible_input_joltages, key=lambda x: heuristic(x, target_joltages, target_weights), reverse=True)[:keep_best])
#    new_inputs = frozenset(new_possible_input_joltages)
    new_depth = depth + 1
    return recursively_apply_button_to_joltage_until_target(new_inputs, button_tuples, target_joltages, new_depth, target_weights, keep_best)


def brute_force_joltages(machine: Machine) -> int:
    initial_joltages = tuple([0] * len(machine[2]))
    buttons = machine[1]

    def make_button_tuple(button: Button) -> Joltages:
        return apply_button_to_joltages(initial_joltages, button)

    button_tuples = frozenset(make_button_tuple(button) for button in buttons)

    def count_buttons_that_affect_joltage(i: int) -> int:
        count = 0
        for b in buttons:
            if i in b:
                count += 1
        return count

    target_weights = tuple(len(buttons) - count_buttons_that_affect_joltage(i) for i in range(len(machine[2])))

    keep_best_base = 10000
    keep_best = keep_best_base

    while True:
        try:
            return recursively_apply_button_to_joltage_until_target(frozenset([initial_joltages]), button_tuples, machine[2], 1, target_weights, keep_best)
        except SearchFailedExcpetion:
            keep_best += keep_best_base
    # button_presses = 0

    # while True:
    #     button_presses += 1
    #     button_sequences = list(product(buttons, repeat=button_presses))
    #     print(f"{button_presses=}")
    #     for sequence in button_sequences:
    #         #print(btn_seq_to_str(sequence))
    #         changed_joltages = apply_button_sequence_to_joltages(initial_joltages, sequence)
    #         if changed_joltages == machine[2]:
    #             return button_presses


def main():
    input = load_input()
    machines = [load_machine(line) for line in input]

    sum = 0

    for i, mach in enumerate(machines):
        # presses = brute_force_indicators(mach)
        presses = brute_force_joltages(mach)
        print(f"machine {i}: {presses}")
        sum += presses

    print(f"{sum=}")


if __name__ == "__main__":
    main()
