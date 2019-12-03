import pytest

from crossed_wires import find_crossing_points, compute_manhattan_distance, parse_wire_path, find_closest_distance, \
    find_fewest_steps


def test_find_crossing_points_should_return_list_with_1_1_tuple_when_wires_are_connected_directly():
    first_wire_path = ['R1', 'U1']
    second_wire_path = ['U1', 'R1']

    crossing_points = find_crossing_points(first_wire_path, second_wire_path)

    assert crossing_points == [(1, 1)]


def test_find_crossing_points_should_return_empty_list_when_wires_are_not_connected():
    first_wire_path = ['R1', 'U1']
    second_wire_path = ['D1', 'R1']

    crossing_points = find_crossing_points(first_wire_path, second_wire_path)

    assert crossing_points == []


def test_find_crossing_points_should_return_crossing_points_when_wires_connect_once():
    first_wire_path = ['R2', 'U2']
    second_wire_path = ['U2', 'R2']

    crossing_points = find_crossing_points(first_wire_path, second_wire_path)

    assert crossing_points == [(2, 2)]


def test_find_crossing_points_should_return_crossing_points_when_wires_connect_multiple_times():
    first_wire_path = ['R8', 'U5', 'L5', 'D3']
    second_wire_path = ['U7', 'R6', 'D4', 'L4']

    crossing_points = find_crossing_points(first_wire_path, second_wire_path)

    assert crossing_points == [(3, 3), (6, 5)]


def test_find_crossing_points_should_return_crossing_points_when_wires_connect_once_after_more_than_ten_moves():
    first_wire_path = ['R10', 'U10']
    second_wire_path = ['U10', 'R10']

    crossing_points = find_crossing_points(first_wire_path, second_wire_path)

    assert crossing_points == [(10, 10)]


def test_compute_manhattan_distance_should_return_0_when_points_are_at_the_same_position():
    origin = (0, 0)
    destination = (0, 0)

    manhattan_distance = compute_manhattan_distance(origin, destination)

    assert manhattan_distance == 0


def test_compute_manhattan_distance_should_return_6_when_points_are_at_0_0_and_3_3():
    origin = (3, 3)
    destination = (0, 0)

    manhattan_distance = compute_manhattan_distance(origin, destination)

    assert manhattan_distance == 6


def test_compute_manhattan_distance_should_default_to_0_0_when_destination_is_not_provided():
    origin = (3, 3)

    manhattan_distance = compute_manhattan_distance(origin)

    assert manhattan_distance == 6


def test_parse_wire_path_should_split_wire_paths_in_a_list_using_commas():
    wire_path = 'R8,U5,L5,D3'
    parsed_wire_path = parse_wire_path(wire_path)

    assert parsed_wire_path == ['R8', 'U5', 'L5', 'D3']


parametrized_data_test = [
    (['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
     ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'], 159),
    (['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51'],
     ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7'], 135)
]


@pytest.mark.parametrize('first_wire_moves,second_wire_moves,expected_closest_distance', parametrized_data_test)
def test_find_closest_point_should_return_closest_points_for_wires(first_wire_moves, second_wire_moves,
                                                                   expected_closest_distance):
    actual_closest_distance = find_closest_distance(first_wire_moves, second_wire_moves)

    assert actual_closest_distance == expected_closest_distance


parametrized_data_test = [
    (['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
     ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'], 610),
    (['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51'],
     ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7'], 410)
]


@pytest.mark.parametrize('first_wire_moves,second_wire_moves,expected_fewest_steps', parametrized_data_test)
def test_find_fewest_steps_should_return_fewest_steps_for_wires(first_wire_moves, second_wire_moves,
                                                                expected_fewest_steps):
    actual_fewest = find_fewest_steps(first_wire_moves, second_wire_moves)

    assert actual_fewest == expected_fewest_steps
