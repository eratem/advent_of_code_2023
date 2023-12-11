from pathlib import Path
from timeit import default_timer as timer


def _get_rgb_from_game_set(game_set: str) -> tuple[int, int, int]:
    items = game_set.split(",")
    r, g, b = 0, 0, 0
    for item in items:
        if "red" in item:
            r = int(item.replace("red", "").strip())
        if "green" in item:
            g = int(item.replace("green", "").strip())
        if "blue" in item:
            b = int(item.replace("blue", "").strip())
    return (r, g, b)


def _decode_max_rgb(rgb_info: str) -> tuple[int, int, int]:
    max_r = 0
    max_g = 0
    max_b = 0
    for game_set in rgb_info.split(";"):
        r, g, b = _get_rgb_from_game_set(game_set)
        max_r = max(max_r, r)
        max_g = max(max_g, g)
        max_b = max(max_b, b)
    return (max_r, max_g, max_b)


def _is_valid_game(r, g, b):
    return r <= 12 and g <= 13 and b <= 14


def _max_rgb_dependent_id(game_info: str, r: int, g: int, b: int) -> int:
    if _is_valid_game(r, g, b):
        return int(game_info.split(" ")[1])
    else:
        return 0


def _get_game_info_and_rgb_info_from_line(line: str) -> tuple[str, str]:
    split_line = line.split(":")
    game_info = split_line[0]
    rgb_info = split_line[1]
    return game_info, rgb_info


def _valid_game_id(line: str) -> int:
    game_info, rgb_info = _get_game_info_and_rgb_info_from_line(line)
    r, g, b = _decode_max_rgb(rgb_info)
    return _max_rgb_dependent_id(game_info, r, g, b)


def _power_of_the_game(line: str) -> int:
    _, rgb_info = _get_game_info_and_rgb_info_from_line(line)
    r, g, b = _decode_max_rgb(rgb_info)
    return r * g * b


def sum_of_valid_games(data: list[str]) -> int:
    return sum([_valid_game_id(line) for line in data])


def sum_of_powers_of_the_games(data: list[str]) -> int:
    return sum([_power_of_the_game(line) for line in data])


def main() -> None:
    with open(Path("puzzle_day2.txt"), "r") as file:
        data = file.readlines()

    start = timer()
    print(f"Sum of valid games is: {sum_of_valid_games(data)}")
    end = timer()
    print(f"Time taken: {end-start}")

    start = timer()
    print(f"Sum of power of games is: {sum_of_powers_of_the_games(data)}")
    end = timer()
    print(f"Time taken: {end-start}")


if __name__ == "__main__":
    main()
