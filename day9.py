from pathlib import Path
from typing import List


def load_data(path: Path) -> List[str]:
    with open(path, "r") as file:
        data = file.readlines()
    return data

def _split_line_into_numbers(line: str)->List[int]:
    return [int(element.strip()) for element in line.strip().split(" ")]

def _parse_data(data: List[str])->List[List[int]]:
    return [_split_line_into_numbers(line) for line in data]

def _find_next_number_in_series(history: List[int])->int:
    last_differences = []
    current_line = history
    while not all(item == 0 for item in current_line):
        last_differences.append(current_line[-1])
        current_line = [next - current for current, next in zip(current_line, current_line[1:])]
    return sum(last_differences)

def _find_previous_number_in_series(history: List[int])->int:
    previous_differences = []
    current_line = history
    while not all(item == 0 for item in current_line):
        previous_differences.append(current_line[0])
        current_line = [current-next for current, next in zip(current_line, current_line[1:])]
    return sum(previous_differences)
def main():
    data = load_data(Path("day9.txt"))
    histories = _parse_data(data)
    result = sum([_find_next_number_in_series(history) for history in histories])
    print(result)
    result2 = sum([_find_previous_number_in_series(history) for history in histories])
    print(result2)

if __name__ == "__main__":
    main()
