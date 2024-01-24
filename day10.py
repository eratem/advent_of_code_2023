from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Pipe:
    x: int
    y: int
    symbol: str
    inlet: str = field(compare=False)


def _import_data(path: Path) -> List[str]:
    with open(path, "r") as file:
        data = file.readlines()
    return [line.strip() for line in data]


def _parse_data_to_maze(data: List[str]) -> List[List[str]]:
    return [list(line) for line in data]


def _find_starting_index(maze: List[List[str]]) -> Pipe:
    for x_index, line in enumerate(maze):
        for y_index, token in enumerate(line):
            if token == "S":
                return Pipe(x_index, y_index, "S", "")
    return Pipe(-1, -1, "X", "")


def _find_starting_connectors(
    maze: List[List[str]], start: Pipe
) -> List[Pipe]:
    up = None
    down = None
    left = None
    right = None
    if (start.x > 0) and (token := maze[start.x - 1][start.y]) in ["|", "F", "7"]:
        up = Pipe(start.x - 1, start.y, token, "D")
    if (start.y > 0) and (token := maze[start.x][start.y - 1]) in ["-", "F", "L"]:
        left = Pipe(start.x, start.y - 1, token, "R")
    if ((start.x + 1) < len(maze)) and (token := maze[start.x + 1][start.y]) in [
        "L",
        "|",
        "J",
    ]:
        down = Pipe(start.x + 1, start.y, token, "U")
    if ((start.y + 1) < len(maze[0])) and (token := maze[start.x][start.y + 1]) in [
        "7",
        "-",
        "J",
    ]:
        right = Pipe(start.x, start.y + 1, token, "L")
    return [connector for connector in [up, down, left, right] if connector is not None]

def _get_next_connector(maze: List[List[str]], connector: Pipe)->Pipe:
    key = (connector.symbol, connector.inlet)
    if key in (("7", "L"), ("|","U"),("F","R")):
        x = connector.x+1
        y = connector.y
        return Pipe(x,y,maze[x][y],"U")
    if key in (("|", "D"),("J","L"),("L","R")):
        x = connector.x-1
        y = connector.y
        return Pipe(x,y,maze[x][y], "D")
    if key in (("-","L"),("F","D"),("L","U")):
        x = connector.x
        y = connector.y+1
        return Pipe(x,y,maze[x][y], "L")
    if key in (("-", "R"),("J","U"),("7","D")):
        x = connector.x
        y = connector.y-1
        return Pipe(x,y,maze[x][y], "R")
    return Pipe(-1,-1,"X", "")

def _connectors_not_meeting(maze: List[List[str]], first: Pipe, second:Pipe)->bool:
    already_the_same = first == second
    next_to_each_other = first == _get_next_connector(maze, second)
    return not (already_the_same or next_to_each_other)

def _move_through_maze(maze: List[List[str]], start: Pipe)->int:
    first_connectors = _find_starting_connectors(maze,start)
    counter = 1
    connector_1 = first_connectors[0]
    connector_2 = first_connectors[1]
    while _connectors_not_meeting(maze, connector_1, connector_2):
        connector_1 = _get_next_connector(maze, connector_1)
        connector_2 = _get_next_connector(maze, connector_2)
        counter += 1
    return counter

def main():
    data = _import_data(Path("day10.txt"))
    maze = _parse_data_to_maze(data)
    start = _find_starting_index(maze)
    max_distance = _move_through_maze(maze, start)
    print(max_distance)


if __name__ == "__main__":
    main()
