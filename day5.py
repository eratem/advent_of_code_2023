from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass(order=True)
class Mapping:
    sort_index: int = field(init=False, repr=False)
    destination_start: int
    source_start: int
    count: int

    def __post_init__(self):
        self.sort_index = self.source_start


@dataclass(order=True)
class SourceRange:
    sort_index: int = field(init=False, repr=False)
    start: int
    count: int

    def __post_init__(self):
        self.sort_index = self.start


def _get_seeds_from_data(data: List[str]) -> List[int]:
    seed_line = data[0]
    return [int(seed) for seed in seed_line.strip().split(" ") if seed.isnumeric()]


def load_data(path: Path) -> List[str]:
    with open(path, "r") as file:
        data = file.readlines()
    return data


def _split_data_into_paragraphs(data: List[str]) -> List[List[str]]:
    paragraphs = []
    paragraph = []
    for line in data:
        if line != "\n":
            paragraph.append(line.strip())
        else:
            paragraphs.append(paragraph)
            paragraph = []
    if paragraph:
        paragraphs.append(paragraph)
    return paragraphs[1:]


def _convert_line_to_mapping(line: str) -> Mapping:
    return Mapping(*[int(entry) for entry in line.split(" ")])


def _parse_paragraph(paragraph: List[str]) -> List[Mapping]:
    return [_convert_line_to_mapping(line) for line in paragraph[1:]]


def _map_single_seed_to_location(
    seed: int, conversion_table: List[List[Mapping]]
) -> int:
    for paragraph in conversion_table:
        for mapping in paragraph:
            if seed >= mapping.source_start and seed < (
                mapping.source_start + mapping.count
            ):
                seed += mapping.destination_start - mapping.source_start
                break
    return seed


def _convert_paragraphs_to_mappings(paragraphs: List[List[str]]) -> List[List[Mapping]]:
    return [sorted(_parse_paragraph(paragraph)) for paragraph in paragraphs]


def solve_puzzle1(data) -> int:
    paragraphs = _split_data_into_paragraphs(data)
    seeds = _get_seeds_from_data(data)
    paragraph_mappings = _convert_paragraphs_to_mappings(paragraphs)
    locations = [
        _map_single_seed_to_location(seed, paragraph_mappings) for seed in seeds
    ]
    return min(locations)


def _get_seed_ranges_from_data(data: List[str]) -> List[SourceRange]:
    seed_line = data[0].strip().split(" ")[1:]
    seed_ranges = []
    for start, length in zip(seed_line[::2], seed_line[1::2]):
        if start.isnumeric() and length.isnumeric():
            seed_ranges.append(SourceRange(int(start), int(length)))
    return seed_ranges


def _source_start_in_mapping_range(source: SourceRange, mapping: Mapping) -> bool:
    return (source.start >= mapping.source_start) and (
        source.start < mapping.source_start + mapping.count
    )


def _source_end_in_mapping_range(source: SourceRange, mapping: Mapping) -> bool:
    return (source.start + source.count > mapping.source_start) and (
        source.start + source.count <= mapping.source_start + mapping.count
    )


def _source_range_ends_before_mapping(source: SourceRange, mapping: Mapping) -> bool:
    return source.start + source.count <= mapping.source_start


def _source_end_is_beyond_mapping(source: SourceRange, mapping: Mapping) -> bool:
    return source.start + source.count > mapping.source_start + mapping.count


def _source_start_is_before_mapping(source: SourceRange, mapping: Mapping) -> bool:
    return source.start < mapping.source_start


def _source_start_is_beyond_mapping(source: SourceRange, mapping: Mapping) -> bool:
    return source.start >= mapping.source_start + mapping.count


def _source_is_fully_inside_mapping(source: SourceRange, mapping: Mapping) -> bool:
    return _source_start_in_mapping_range(
        source, mapping
    ) and _source_end_in_mapping_range(source, mapping)


def _source_end_reaches_into_mapping(source: SourceRange, mapping: Mapping) -> bool:
    return _source_start_is_before_mapping(
        source, mapping
    ) and _source_end_in_mapping_range(source, mapping)


def _source_end_reaches_out_of_mapping(source: SourceRange, mapping: Mapping) -> bool:
    return _source_start_in_mapping_range(
        source, mapping
    ) and _source_end_is_beyond_mapping(source, mapping)


def _source_surrounds_mapping(source: SourceRange, mapping: Mapping) -> bool:
    return _source_start_is_before_mapping(
        source, mapping
    ) and _source_end_is_beyond_mapping(source, mapping)


def _map_full_range(source: SourceRange, mapping: Mapping) -> SourceRange:
    new_start = source.start + mapping.destination_start - mapping.source_start
    return SourceRange(new_start, source.count)


def _map_tail_end(
    source: SourceRange, mapping: Mapping
) -> Tuple[SourceRange, SourceRange]:
    first_count = mapping.source_start - source.start
    first_range = SourceRange(source.start, first_count)
    second_count = source.count - first_count
    second_range = SourceRange(mapping.destination_start, second_count)
    return (first_range, second_range)


def _map_range_head(
    source: SourceRange, mapping: Mapping
) -> Tuple[SourceRange, SourceRange]:
    first_start = source.start + mapping.destination_start - mapping.source_start
    first_count = mapping.source_start + mapping.count - source.start
    first_range = SourceRange(first_start, first_count)
    new_start = mapping.source_start + mapping.count
    new_count = source.count - first_count
    new_range = SourceRange(new_start, new_count)
    return (first_range, new_range)


def _map_surrounding_range(
    source: SourceRange, mapping: Mapping
) -> Tuple[SourceRange, SourceRange, SourceRange]:
    first_count = mapping.source_start - source.start
    first_range = SourceRange(source.start, first_count)
    second_range = SourceRange(mapping.destination_start, mapping.count)
    new_start = mapping.source_start + mapping.count
    new_count = source.count - first_count - mapping.count
    new_range = SourceRange(new_start, new_count)
    return first_range, second_range, new_range


def _transform_source_range_to_destination_ranges(
    source_ranges: List[SourceRange], mappings: List[Mapping]
) -> List[SourceRange]:
    destination_ranges = []
    for source_range in source_ranges:
        current_range: Optional[SourceRange] = source_range
        for mapping in mappings:
            if current_range is None:
                break
            if _source_start_is_beyond_mapping(current_range, mapping):
                continue
            elif _source_range_ends_before_mapping(current_range, mapping):
                continue
            elif _source_is_fully_inside_mapping(current_range, mapping):
                destination_ranges.append(_map_full_range(current_range, mapping))
                current_range = None
                break
            elif _source_end_reaches_into_mapping(current_range, mapping):
                first_range, second_range = _map_tail_end(current_range, mapping)
                destination_ranges.append(first_range)
                destination_ranges.append(second_range)
                current_range = None
                break
            elif _source_end_reaches_out_of_mapping(current_range, mapping):
                first_range, current_range = _map_range_head(current_range, mapping)
                destination_ranges.append(first_range)
            elif _source_surrounds_mapping(current_range, mapping):
                first_range, second_range, current_range = _map_surrounding_range(
                    current_range, mapping
                )
                destination_ranges.append(first_range)
                destination_ranges.append(second_range)
        if current_range is not None:
            destination_ranges.append(current_range)
    return destination_ranges


def _transform_through_all_paragraphs(
    seeds: List[SourceRange], paragraph_mappings: List[List[Mapping]]
) -> List[SourceRange]:
    destination_ranges = seeds
    for paragraph in paragraph_mappings:
        destination_ranges = _transform_source_range_to_destination_ranges(
            destination_ranges, paragraph
        )
    return destination_ranges


def solve_puzzle2(data) -> int:
    paragraphs = _split_data_into_paragraphs(data)
    seeds = _get_seed_ranges_from_data(data)
    paragraph_mappings = _convert_paragraphs_to_mappings(paragraphs)
    destination_ranges = _transform_through_all_paragraphs(seeds, paragraph_mappings)
    return sorted(destination_ranges)[0].start


def main() -> None:
    path = Path("./day5_data.txt")
    example = Path("./example5.txt")
    data = load_data(path)
    print(solve_puzzle1(data))
    print(solve_puzzle2(data))


if __name__ == "__main__":
    main()
