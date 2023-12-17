from dataclasses import dataclass
from pathlib import Path
from timeit import default_timer as timer


@dataclass(frozen=True)
class IndexedNumber:
    start_index: int
    end_index: int
    number: int


def _search_numbers_with_indexes(line: str) -> list[IndexedNumber]:
    results = []
    current_number = 0
    start_index = 0
    for index, character in enumerate(line):
        if character.isdigit():
            if current_number == 0:
                start_index = index
            current_number = current_number * 10 + int(character)
        else:
            if current_number == 0:
                continue
            else:
                results.append(IndexedNumber(start_index, index, current_number))
                current_number = 0
    if current_number != 0:
        results.append(IndexedNumber(start_index, len(line), current_number))
    return results


def _find_numbers_with_neighbouring_symbols(
    numbers: list[IndexedNumber], frame: list[str]
) -> list[int]:
    results = []
    for number in numbers:
        if number.start_index == 0:
            start_window = 0
        else:
            start_window = number.start_index - 1
        matches_symbol = False
        for line in frame:
            window = line[start_window : number.end_index + 1]
            for character in window:
                if (not character.isdigit()) and (character != "."):
                    matches_symbol = True
                    break
            if matches_symbol:
                break
        if matches_symbol:
            results.append(number.number)
    return results


def solve_puzzle1(data: list[str]) -> int:
    number_of_rows = len(data)
    matches = []
    for index in range(number_of_rows):
        if index == 0:
            frame = ["".join(["." for _ in data[0]])] + data[index : index + 2]
        elif index == number_of_rows - 1:
            frame = data[index - 1 : number_of_rows] + ["".join(["." for _ in data[0]])]
        else:
            frame = data[index - 1 : index + 2]
        numbers = _search_numbers_with_indexes(data[index])
        matched_numbers = _find_numbers_with_neighbouring_symbols(numbers, frame)
        matches += matched_numbers
    return sum(matches)


def main() -> None:
    sample_puzzle = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755#
..........
.664#598..
........10
.........%
""".splitlines()
    with open(Path("puzzle_day3.txt"), "r") as file:
        data = file.readlines()

    start = timer()
    solution1 = solve_puzzle1(data)
    end = timer()
    print(solution1)
    print(f"Time taken: {end-start}")

    start = timer()
    end = timer()
    print(f"Time taken: {end-start}")


if __name__ == "__main__":
    main()
