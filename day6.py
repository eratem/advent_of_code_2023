import math
from pathlib import Path
from typing import List, Tuple


def _import_data(path: Path) -> List[str]:
    with open(path, "r") as file:
        data = file.readlines()
    return data


def _calculate_limits(time: int, distance: int) -> Tuple[int, int]:
    min_v = int((time - math.sqrt(time * time - 4 * distance)) / 2)
    if (min_v * (time - min_v)) > distance:
        lower = min_v
        upper = time - lower
    else:
        lower = min_v + 1
        upper = time - lower
    return (lower, upper)


def _parse_challenges(data: List[str]) -> List[Tuple[int, int]]:
    time = [int(entry) for entry in data[0].split(" ")[1:] if entry.strip().isnumeric()]
    distance = [
        int(entry) for entry in data[1].split(" ")[1:] if entry.strip().isnumeric()
    ]
    return list(zip(time, distance))


def solve_puzzle1(data: List[str]) -> int:
    challenges = _parse_challenges(data)
    limits = [_calculate_limits(time, distance) for time, distance in challenges]
    differences = [abs(upper - lower) + 1 for lower, upper in limits]
    total = 1
    for difference in differences:
        total *= difference
    return total


def _parse_for_second_puzzle(data: List[str]) -> Tuple[int, int]:
    time = int("".join(data[0].split(" ")[1:]).strip())
    distance = int("".join(data[1].split(" ")[1:]).strip())
    return time, distance


def solve_puzzle2(data: List[str]) -> int:
    time, distance = _parse_for_second_puzzle(data)
    upper, lower = _calculate_limits(time, distance)
    print(upper, lower)
    return abs(upper - lower) + 1


def main():
    path = Path("./day6_data.txt")
    example = Path("./example6.txt")
    data = _import_data(path)
    print(solve_puzzle1(data))
    print(solve_puzzle2(data))


if __name__ == "__main__":
    main()
