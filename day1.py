from pathlib import Path


def load_puzzle(path: Path = Path("puzzle_day1.txt")) -> list[str]:
    with open(path, "r") as file:
        data = file.readlines()
    return data


def naive_decomposition(line: str) -> int:
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    result_numbers: list[str] = []
    for char in line:
        if char in digits:
            result_numbers.append(char)
    return int(result_numbers[0] + result_numbers[-1])


data = load_puzzle()
print(sum([naive_decomposition(line) for line in data]))
