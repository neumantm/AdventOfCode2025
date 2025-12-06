
from dataclasses import dataclass
from typing import Self


def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


@dataclass
class FreshRange():
    start: int
    end: int

    def contains(self, ing: int) -> bool:
        return ing >= self.start and ing <= self.end

    def merge_if_overlapping(self, other: Self) -> "FreshRange|None":
        if self.start <= other.start and self.end >= other.start:
            if other.end >= self.end:
                return FreshRange(self.start, other.end)
            else:
                return FreshRange(self.start, self.end)
        if self.end >= other.end and self.start <= other.end:
            if other.start <= self.start:
                return FreshRange(other.start, self.end)
            else:
                return FreshRange(self.start, self.end)
        return None

    def count(self) -> int:
        return (self.end + 1) - self.start

    def get_all_ingredients(self) -> set[int]:
        return set(range(self.start, self.end+1))

    def __str__(self) -> str:
        return f"{self.start} -> {self.end} -- {self.count()}"


def minimize_ranges(ranges: list[FreshRange]) -> list[FreshRange]:
    working_list = ranges.copy()

    def try_merge_anything(working_list: list[FreshRange]) -> bool:
        for i1, r1 in enumerate(working_list):
            for i2, r2 in enumerate(working_list):
                if i1 == i2:
                    continue
                mr = r1.merge_if_overlapping(r2)
                if mr:
                    working_list.append(mr)
                    working_list.remove(r1)
                    working_list.remove(r2)
                    return True
        return False

    while try_merge_anything(working_list):
        pass

    return working_list


def load_ranges(ranges: list[str]) -> list[FreshRange]:
    result: list[FreshRange] = []
    for r in ranges:
        parts = r.split("-")
        start = int(parts[0])
        end = int(parts[1])
        result.append(FreshRange(start, end))
    return result


def main():
    input = load_input()

    cut_point = input.index("\n")
    ranges = [line.strip() for line in input[:cut_point]]
    ingredients = [line.strip() for line in input[cut_point + 1:]]

    fresh_ingredients = load_ranges(ranges)

    print("loaded")

    # B
    print(fresh_ingredients)
    minimized = minimize_ranges(fresh_ingredients)
    print("----")

    minimized.sort(key=lambda r: r.start)
    for m in minimized:
        print(m)

    counts = [it.count() for it in minimized]
    amount_of_fresh = sum(counts)
    print(amount_of_fresh)

    # A
    return

    num_fresh_ingredients = 0

    for i, ingr in enumerate(ingredients):
        print(f"{i}/{len(ingredients)}")
        for fresh_range in fresh_ingredients:
            if fresh_range.contains(int(ingr)):
                num_fresh_ingredients += 1
                break

    print(num_fresh_ingredients)


if __name__ == "__main__":
    main()
