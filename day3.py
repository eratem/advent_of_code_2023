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
        elif current_number != 0:
            results.append(IndexedNumber(start_index - 1, index, current_number))
            current_number = 0
    if current_number != 0:
        results.append(IndexedNumber(start_index - 1, len(line), current_number))
    return results


def _get_gear_indexes(line: str) -> list[int]:
    return [index for index, character in enumerate(line) if character == "*"]


def _find_gear_ratios(gear_indexes: list[int], frame: list[str]) -> list[int]:
    gear_ratios = []
    indexed_number_frame = [_search_numbers_with_indexes(line) for line in frame]
    found_gear_numbers = []
    for gear_index in gear_indexes:
        for line in indexed_number_frame:
            for indexed_number in line:
                if indexed_number.start_index <= gear_index <= indexed_number.end_index:
                    found_gear_numbers.append(indexed_number.number)
        if len(found_gear_numbers) == 2:
            gear_ratios.append(found_gear_numbers[0] * found_gear_numbers[1])
        found_gear_numbers = []
    return gear_ratios


def _find_numbers_with_neighbouring_symbols(
    indexed_numbers: list[IndexedNumber], frame: list[str]
) -> list[int]:
    results = []
    for indexed_number in indexed_numbers:
        if indexed_number.start_index <= 0:
            start_window = 0
        else:
            start_window = indexed_number.start_index
        matches_symbol = False
        for line in frame:
            window = line[start_window : indexed_number.end_index + 1]
            for character in window:
                if (not character.isdigit()) and (character != "."):
                    matches_symbol = True
                    break
            if matches_symbol:
                break
        if matches_symbol:
            results.append(indexed_number.number)
    return results


def solve_puzzle1(data: list[str]) -> int:
    data = [line.strip() for line in data]
    number_of_rows = len(data)
    matches = []
    for index, current_row in enumerate(data):
        if index == 0:
            frame = data[index : index + 2]
        elif index == number_of_rows - 1:
            frame = data[index - 1 : number_of_rows]
        else:
            frame = data[index - 1 : index + 2]
        numbers = _search_numbers_with_indexes(current_row)
        matches += _find_numbers_with_neighbouring_symbols(numbers, frame)
    return sum(matches)


def solve_puzzle2(data: list[str]) -> int:
    data = [line.strip() for line in data]
    number_of_rows = len(data)
    gear_ratios = []
    for index, current_row in enumerate(data):
        if index == 0:
            frame = data[index : index + 2]
        elif index == number_of_rows - 1:
            frame = data[index - 1 : number_of_rows]
        else:
            frame = data[index - 1 : index + 2]
        gear_indexes = _get_gear_indexes(current_row)
        gear_ratios += _find_gear_ratios(gear_indexes, frame)
    return sum(gear_ratios)


def main() -> None:
    with open(Path("puzzle_day3.txt"), "r") as file:
        data = file.readlines()

    start = timer()
    solution1 = solve_puzzle1(data)
    end = timer()
    print(solution1)
    print(f"Time taken: {end-start}")

    start = timer()
    solution2 = solve_puzzle2(data)
    end = timer()
    print(solution2)
    print(f"Time taken: {end-start}")


if __name__ == "__main__":
    main()
