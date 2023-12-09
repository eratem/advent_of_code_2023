from pathlib import Path
from timeit import default_timer as timer


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
    if result_numbers:
        return int(result_numbers[0] + result_numbers[-1])
    else:
        return 0


def improved_decomposition(line: str) -> int:
    digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    result_numbers = [int(char) for char in line if char in digits]
    if result_numbers:
        return result_numbers[0] * 10 + result_numbers[-1]
    else:
        return 0


def functional_decomposition1(line: str) -> int:
    matches = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    filtered = list(filter(lambda x: x in matches, line))
    if filtered:
        return int("".join([filtered[0], filtered[-1]]))
    else:
        return 0


def digitize(line: str) -> str:
    numbers_as_words = [
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
    ]
    smallest_index = len(line)
    winning_word = ""
    winning_number = ""
    found_word = True
    while found_word:
        found_word = False
        for word, number in numbers_as_words:
            if (index := line.find(word)) != -1:
                if index < smallest_index:
                    smallest_index = index
                    winning_word = word
                    winning_number = number
                    found_word = True
        if found_word:
            line = line.replace(winning_word, winning_number)
            smallest_index = len(line)
    return line


def functional_decomposition2(line: str) -> int:
    matches = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    digits = list(map(lambda x: int(x), filter(lambda x: x in matches, digitize(line))))
    return digits[0] * 10 + digits[-1]


def naive_puzzle1(data: list[str]) -> int:
    return sum([naive_decomposition(line) for line in data])


def improved_puzzle1(data: list[str]) -> int:
    return sum([improved_decomposition(line) for line in data])


def functional_puzzle1(data: list[str]) -> int:
    return sum(map(functional_decomposition1, data))


def functional_puzzle2(data: list[str]) -> int:
    return sum(map(functional_decomposition2, data))


data = load_puzzle()
start = timer()
print(naive_puzzle1(data))
end = timer()
print(f"Naive Puzzle 1: {end - start}")


start = timer()
print(improved_puzzle1(data))
end = timer()
print(f"Improved Puzzle 1: {end - start}")

start = timer()
print(functional_puzzle1(data))
end = timer()
print(f"Functional Puzzle 1: {end - start}")

start = timer()
print(functional_puzzle2(data))
end = timer()
print(f"Functional Puzzle 2: {end - start}")
