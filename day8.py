import math
from pathlib import Path
from typing import Dict, List, Tuple


def load_data(path: Path) -> List[str]:
    with open(path, "r") as file:
        data = file.readlines()
    return data


def _parse_puzzle_input(data: List[str]):
    directions = list(data[0].strip())
    mappings = {}
    for line in data[1:]:
        if line == "\n":
            continue
        else:
            items = line.strip().split(" = ")
            key = items[0]
            values = items[1].replace("(", " ").replace(")", " ").split(",")
            left = values[0].strip()
            right = values[1].strip()
            mappings[key] = (left, right)
    return (directions, mappings)


def _get_next_location(
    direction: str, location: str, mappings: Dict[str, Tuple[str, str]]
) -> str:
    if direction == "L":
        return mappings[location][0]
    else:
        return mappings[location][1]


def _traverse_puzzle1(
    directions: List[str], mappings: Dict[str, Tuple[str, str]]
) -> int:
    current_location = "AAA"
    counter = 0
    direction_length = len(directions)
    while current_location != "ZZZ":
        direction = directions[counter % direction_length]
        current_location = _get_next_location(direction, current_location, mappings)
        counter += 1
    return counter


def _find_all_starts(mappings: Dict[str, Tuple[str, str]]) -> List[str]:
    return [key for key in mappings.keys() if key[2] == "A"]


def location_ends_at_z(location: str) -> bool:
    return location[2] == "Z"

def lcm(a:int, b:int)->int:
    return abs(a*b) // math.gcd(a,b)

def _traverse_puzzle_2(
    start_locations: List[str],
    directions: List[str],
    mappings: Dict[str, Tuple[str, str]],
) -> int:
    locations= start_locations
    direction_length = len(directions)
    distances = []
    for location in locations:
        counter = 0
        while not location_ends_at_z(location):
            direction = directions[counter % direction_length]
            location = _get_next_location(direction, location, mappings)
            counter += 1
        distances.append(counter)
    max_dist = 1
    for distance in distances:
        max_dist = lcm(max_dist, distance)
    return max_dist


def main():
    data = load_data(Path("day8.txt"))
    directions, mappings = _parse_puzzle_input(data)
    puzzle1_result = _traverse_puzzle1(directions, mappings)
    print(puzzle1_result)
    starts = _find_all_starts(mappings)
    puzzle2_result = _traverse_puzzle_2(starts, directions, mappings)
    print(puzzle2_result)


if __name__ == "__main__":
    main()
