from pathlib import Path
from timeit import default_timer as timer


def _get_winning_numbers(line: str) -> list[int]:
    return [
        int(word)
        for word in (
            line.strip().split(":")[1].strip().split("|")[0].strip().split(" ")
        )
        if word.isdecimal()
    ]


def _get_candidate_numbers(line: str) -> list[int]:
    return [
        int(word)
        for word in (
            line.strip().split(":")[1].strip().split("|")[1].strip().split(" ")
        )
        if word.isdecimal()
    ]


def _calculate_points_per_card(line: str) -> int:
    winning_numbers = _get_winning_numbers(line)
    candidate_numbers = _get_candidate_numbers(line)
    points = 0
    for candidate_number in candidate_numbers:
        if candidate_number in winning_numbers:
            points += 1
    return points


def _calculate_amount_per_card(line: str) -> int:
    exponent = _calculate_points_per_card(line) - 1
    if exponent == -1:
        result = 0
    else:
        result = 2**exponent
    return result


def _calculate_number_of_cards(data: list[str]) -> list[int]:
    points_per_card = [_calculate_points_per_card(line) for line in data]
    number_of_rows = len(data)
    number_of_cards = [1 for _ in range(number_of_rows)]
    for index, points in enumerate(points_per_card):
        if points == 0:
            continue
        else:
            for count in range(points):
                if number_of_rows > index + count:
                    number_of_cards[index + count + 1] += number_of_cards[index]
    return number_of_cards


def find_total_winnings(data: list[str]) -> int:
    return sum([_calculate_amount_per_card(line) for line in data])


def find_total_cards_won(data: list[str]) -> int:
    return sum(_calculate_number_of_cards(data))


def main() -> None:
    with open(Path("puzzle_day4.txt"), "r") as file:
        data = file.readlines()

    start = timer()
    print(find_total_winnings(data))
    end = timer()
    print(f"Time taken: {end-start}")

    start = timer()
    print(find_total_cards_won(data))
    end = timer()
    print(f"Time taken: {end-start}")


if __name__ == "__main__":
    main()
