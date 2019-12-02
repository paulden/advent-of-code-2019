import pytest

from gravity_assist import compute_intcode_sequence, parse_intcode_sequence, find_possible_combinations


def test_compute_int_sequence_should_return_a_list_of_same_length():
    initial_state = [1, 0, 0, 0, 99]
    final_state = compute_intcode_sequence(initial_state)

    assert len(final_state) == len(initial_state)


def test_1_in_position_0_should_add_numbers():
    initial_state = [1, 0, 0, 0, 99]
    final_state = compute_intcode_sequence(initial_state)

    assert final_state == [2, 0, 0, 0, 99]


def test_1_in_position_0_should_add_numbers_from_positions_specified():
    initial_state = [1, 4, 0, 0, 99]
    final_state = compute_intcode_sequence(initial_state)

    assert final_state == [100, 4, 0, 0, 99]


def test_1_in_position_0_should_add_numbers_from_positions_specified_and_set_value_in_position_specified():
    initial_state = [1, 4, 0, 1, 99]
    final_state = compute_intcode_sequence(initial_state)

    assert final_state == [1, 100, 0, 1, 99]


def test_2_in_position_0_should_multiply_numbers_from_positions_specified_and_set_value_in_position_specified():
    initial_state = [2, 0, 4, 1, 99]
    final_state = compute_intcode_sequence(initial_state)

    assert final_state == [2, 198, 4, 1, 99]


def test_compute_intcode_sequence_should_run_sequences_until_99_arrives():
    initial_state = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    final_state = compute_intcode_sequence(initial_state)

    assert final_state == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]


def test_parse_intcode_sequence_should_split_sequences_in_a_list_using_commas():
    input_sequence = '1,9,10,3,2,3,11,0,99,30,40,50'
    parsed_sequence = parse_intcode_sequence(input_sequence)

    assert parsed_sequence == [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]


parametrized_data_test = [
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])
]


@pytest.mark.parametrize("initial_state,final_state", parametrized_data_test)
def test_compute_intcode_sequence_should_run_basic_sequences(initial_state, final_state):
    initial_state = [2, 0, 4, 1, 99]
    final_state = compute_intcode_sequence(initial_state)

    assert final_state == [2, 198, 4, 1, 99]


def test_find_possible_combinations_should_return_list_of_tuples():
    input_sequence = [1, 0, 0, 0, 99]
    expected_output = 2
    possible_combinations = find_possible_combinations(input_sequence, expected_output)

    assert possible_combinations[0] == (0, 0)
