

# row, column
from dataclasses import dataclass, field


Coord = tuple[int, int]


def below(coord: Coord) -> Coord:
    return (coord[0] + 1, coord[1])


def left(coord: Coord) -> Coord:
    return (coord[0], coord[1] - 1)


def right(coord: Coord) -> Coord:
    return (coord[0], coord[1] + 1)


# rows of cells; true = splitter
Field = list[list[bool]]


def get(field: Field, pos: Coord) -> bool:
    return field[pos[0]][pos[1]]


def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def load_field(input: list[str]) -> tuple[Coord, Field]:
    result: Field = []
    start_pos: Coord | None = None
    for i, line in enumerate(input):
        result.append([cell == "^" for cell in line])
        if "S" in line:
            start_pos = (i, line.index("S"))

    if start_pos is None:
        raise ValueError("Did not find start")

    return start_pos, result


@dataclass
class BeamTip:
    pos: Coord = field()
    weight: int = field(default=1)


class BeamSimulation():
    beam_tips: dict[Coord, BeamTip]
    field: Field
    split_count: int
    split_count_times_beam_weight: int

    def __init__(self, field: Field, start: Coord) -> None:
        self.beam_tips = {start: BeamTip(start)}
        self.field = field
        self.split_count = 0
        self.split_count_times_beam_weight = 0

    def add_tip_at(self, coord: Coord, weight=1):
        if coord in self.beam_tips:
            self.beam_tips[coord].weight += weight
        else:
            self.beam_tips[coord] = BeamTip(coord, weight)

    def split_beam(self, beam_tip: BeamTip):
        self.add_tip_at(left(below(beam_tip.pos)), beam_tip.weight)
        self.add_tip_at(right(below(beam_tip.pos)), beam_tip.weight)

    def step(self) -> None:
        old_beam_tips = self.beam_tips
        self.beam_tips = dict()

        for coord, beam_tip in old_beam_tips.items():
            if get(self.field, below(coord)):
                self.split_beam(beam_tip)
                self.split_count += 1
                self.split_count_times_beam_weight += beam_tip.weight
            else:
                self.add_tip_at(below(coord), beam_tip.weight)


def main():
    input = load_input()
    start_pos, field = load_field(input)
    sim = BeamSimulation(field, start_pos)
    for i in range(len(field)-1):
        print(f"{i}/{len(field)-1}")
        sim.step()
    print(f"{sim.split_count=}")
    print(f"{sim.split_count_times_beam_weight+1=}")


if __name__ == "__main__":
    main()
