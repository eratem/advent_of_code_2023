import day5


def test_source_start_in_mapping_range_just_below_is_false():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 6, 10)
    assert not day5._source_start_in_mapping_range(source, mapping)


def test_source_start_in_mapping_range_just_in_is_true():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 5, 10)
    assert day5._source_start_in_mapping_range(source, mapping)


def test_source_start_in_mapping_range_just_beyond_is_false():
    source = day5.SourceRange(15, 10)
    mapping = day5.Mapping(10, 5, 10)
    assert not day5._source_start_in_mapping_range(source, mapping)


def test_source_start_in_mapping_range_just_at_the_end_is_true():
    source = day5.SourceRange(14, 10)
    mapping = day5.Mapping(10, 5, 10)
    assert day5._source_start_in_mapping_range(source, mapping)


def test_source_end_in_mapping_range_just_before_is_false():
    source = day5.SourceRange(0, 5)
    mapping = day5.Mapping(10, 5, 10)
    assert not day5._source_end_in_mapping_range(source, mapping)


def test_source_end_in_mapping_range_just_at_beginning_is_true():
    source = day5.SourceRange(0, 5)
    mapping = day5.Mapping(10, 4, 10)
    assert day5._source_end_in_mapping_range(source, mapping)


def test_source_end_in_mapping_range_just_at_the_end_is_true():
    source = day5.SourceRange(0, 5)
    mapping = day5.Mapping(10, 0, 5)
    assert day5._source_end_in_mapping_range(source, mapping)


def test_source_end_in_mapping_range_just_beyond_the_end_is_false():
    source = day5.SourceRange(0, 5)
    mapping = day5.Mapping(10, 0, 4)
    assert not day5._source_end_in_mapping_range(source, mapping)


def test_source_range_ends_before_mapping_just_at_the_end_is_false():
    source = day5.SourceRange(0, 5)
    mapping = day5.Mapping(10, 4, 10)
    assert not day5._source_range_ends_before_mapping(source, mapping)


def test_source_range_ends_before_mapping_just_before_is_true():
    source = day5.SourceRange(0, 5)
    mapping = day5.Mapping(10, 5, 10)
    assert day5._source_range_ends_before_mapping(source, mapping)


def test_source_end_is_beyond_mapping_at_end_is_false():
    source = day5.SourceRange(0, 5)
    mapping = day5.Mapping(10, 0, 5)
    assert not day5._source_end_is_beyond_mapping(source, mapping)


def test_source_end_is_beyond_mapping_just_beyond_is_true():
    source = day5.SourceRange(0, 5)
    mapping = day5.Mapping(10, 0, 4)
    assert day5._source_end_is_beyond_mapping(source, mapping)


def test_source_start_is_before_mapping_just_before_is_true():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 6, 10)
    assert day5._source_start_is_before_mapping(source, mapping)


def test_source_start_is_before_mapping_just_in_is_false():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 5, 10)
    assert not day5._source_start_is_before_mapping(source, mapping)


def test_source_start_is_beyond_mapping_at_end_is_false():
    source = day5.SourceRange(4, 5)
    mapping = day5.Mapping(10, 0, 5)
    assert not day5._source_start_is_beyond_mapping(source, mapping)


def test_source_start_is_beyond_mapping_just_beyond_is_true():
    source = day5.SourceRange(5, 5)
    mapping = day5.Mapping(10, 0, 5)
    assert day5._source_start_is_beyond_mapping(source, mapping)


def test_map_full_range_does_not_shift_if_mapping_same_as_start():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(5, 5, 10)
    result = day5._map_full_range(source, mapping)
    assert result == source


def test_map_full_range_does_shift_by_difference():
    source = day5.SourceRange(5, 10)
    start = 5
    difference = 5
    mapping = day5.Mapping(start + difference, start, 10)
    expected = day5.SourceRange(source.start + difference, source.count)
    result = day5._map_full_range(source, mapping)
    assert expected == result


def test_map_full_range_specific():
    source = day5.SourceRange(5, 5)
    mapping = day5.Mapping(10, 0, 15)
    expected = day5.SourceRange(15, 5)
    result = day5._map_full_range(source, mapping)
    assert expected == result


def test_map_tail_end_first_entry_has_unmodified_starting_point():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(20, 10, 10)
    first, second = day5._map_tail_end(source, mapping)
    assert source.start == first.start


def test_map_tail_end_counts_of_result_ranges_equal_to_source():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(20, 10, 10)
    first, second = day5._map_tail_end(source, mapping)
    assert source.count == first.count + second.count


def test_map_tail_end_second_range_starts_at_mapping_destination_start():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(20, 10, 10)
    first, second = day5._map_tail_end(source, mapping)
    assert second.start == mapping.destination_start


def test_map_tail_end_first_range_ends_one_before_mapping_source_start():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(20, 10, 10)
    first, second = day5._map_tail_end(source, mapping)
    first_end = first.start + first.count - 1
    assert first_end == mapping.source_start - 1


def test_map_tail_specific_first():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(20, 10, 10)
    first, second = day5._map_tail_end(source, mapping)
    expected_first = day5.SourceRange(5, 5)
    assert expected_first == first


def test_map_tail_specific_second():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(20, 10, 10)
    first, second = day5._map_tail_end(source, mapping)
    expected_second = day5.SourceRange(20, 5)
    assert expected_second == second


def test_map_range_head_counts_of_result_ranges_equal_to_source():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 0, 10)
    first, second = day5._map_range_head(source, mapping)
    assert source.count == first.count + second.count


def test_map_range_head_first_start_is_offset_by_mapping_difference():
    source = day5.SourceRange(5, 10)
    difference = 5
    start = 0
    mapping = day5.Mapping(start + difference, start, 10)
    first, second = day5._map_range_head(source, mapping)
    assert source.start + difference == first.start


def test_map_range_head_second_start_is_offset_by_first_count():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 0, 10)
    first, second = day5._map_range_head(source, mapping)
    second_start_offset = second.start - source.start
    assert first.count == second_start_offset


def test_map_range_head_first_range_end_equals_mapping_end():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 0, 10)
    mapping_end = mapping.destination_start + mapping.count - 1
    first, second = day5._map_range_head(source, mapping)
    first_end = first.start + first.count - 1
    assert mapping_end == first_end


def test_map_range_head_specific_first():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 0, 10)
    first, second = day5._map_range_head(source, mapping)
    expected_first = day5.SourceRange(15, 5)
    assert expected_first == first


def test_map_range_head_specific_second():
    source = day5.SourceRange(5, 10)
    mapping = day5.Mapping(10, 0, 10)
    first, second = day5._map_range_head(source, mapping)
    expected_second = day5.SourceRange(10, 5)
    assert expected_second == second


def test_map_surrounding_range_first_start_unchanged():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    first, second, new = day5._map_surrounding_range(source, mapping)
    assert source.start == first.start


def test_map_surrounding_range_new_end_same_as_source_end():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    source_end = source.start + source.count - 1
    first, second, new = day5._map_surrounding_range(source, mapping)
    new_end = new.start + new.count - 1
    assert source_end == new_end


def test_map_surrounding_range_count_of_ranges_same_as_source_count():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    first, second, new = day5._map_surrounding_range(source, mapping)
    total_count = first.count + second.count + new.count
    assert source.count == total_count


def test_map_surrounding_range_first_ends_one_before_mapping_source_start():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    first, second, new = day5._map_surrounding_range(source, mapping)
    first_end = first.start + first.count - 1
    assert first_end == mapping.source_start - 1


def test_map_surrounding_range_second_start_at_mapping_destination_start():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    first, second, new = day5._map_surrounding_range(source, mapping)
    assert second.start == mapping.destination_start


def test_map_surrounding_range_second_count_equal_to_mapping_count():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    first, second, new = day5._map_surrounding_range(source, mapping)
    assert second.count == mapping.count


def test_map_surrounding_range_specific_first():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    first, second, new = day5._map_surrounding_range(source, mapping)
    expected_first = day5.SourceRange(0, 5)
    assert expected_first == first


def test_map_surrounding_range_specific_second():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    first, second, new = day5._map_surrounding_range(source, mapping)
    expected_second = day5.SourceRange(15, 5)
    assert expected_second == second


def test_map_surrounding_range_specific_new():
    source = day5.SourceRange(0, 15)
    mapping = day5.Mapping(15, 5, 5)
    first, second, new = day5._map_surrounding_range(source, mapping)
    expected_new = day5.SourceRange(10, 5)
    assert expected_new == new
