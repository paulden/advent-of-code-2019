import pytest

from air_conditioner import compute_intcode_sequence, parse_intcode_sequence


def test_compute_int_sequence_should_return_a_list_of_same_length():
    initial_state = [1, 0, 0, 0, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert len(final_state) == len(initial_state)


def test_1_in_position_0_should_add_numbers():
    initial_state = [1, 0, 0, 0, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert final_state == [2, 0, 0, 0, 99]


def test_1_in_position_0_should_add_numbers_from_positions_specified():
    initial_state = [1, 4, 0, 0, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert final_state == [100, 4, 0, 0, 99]


def test_1_in_position_0_should_add_numbers_from_positions_specified_and_set_value_in_position_specified():
    initial_state = [1, 4, 0, 1, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert final_state == [1, 100, 0, 1, 99]


def test_2_in_position_0_should_multiply_numbers_from_positions_specified_and_set_value_in_position_specified():
    initial_state = [2, 0, 4, 1, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert final_state == [2, 198, 4, 1, 99]


def test_compute_intcode_sequence_should_run_sequences_until_99_arrives():
    initial_state = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    final_state, output = compute_intcode_sequence(initial_state)

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


@pytest.mark.parametrize('initial_state,final_state', parametrized_data_test)
def test_compute_intcode_sequence_should_run_basic_sequences(initial_state, final_state):
    initial_state = [2, 0, 4, 1, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert final_state == [2, 198, 4, 1, 99]


def test_1_in_position_0_with_immediate_parameters_mode_should_add_numbers_with_immediate_values():
    initial_state = [1101, 5, 5, 2, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert final_state == [1101, 5, 10, 2, 99]


def test_2_in_position_0_with_immediate_parameters_mode_should_multiply_numbers_with_immediate_values():
    initial_state = [1102, 5, 5, 2, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert final_state == [1102, 5, 25, 2, 99]


def test_1_in_position_0_with_immediate_parameters_should_handle_negative_values():
    initial_state = [1101, -5, 5, 2, 99]
    final_state, output = compute_intcode_sequence(initial_state)

    assert final_state == [1101, -5, 0, 2, 99]


def test_3_in_position_0_should_save_input_to_appropriate_address():
    input_value = 99
    initial_state = [3, 2, 0]
    final_state, output = compute_intcode_sequence(initial_state, input_value)

    assert final_state == [3, 2, 99]


def test_4_in_position_0_should_return_output_from_position_mode():
    input_value = 1337
    initial_state = [4, 2, 99]
    final_state, output = compute_intcode_sequence(initial_state, input_value)

    assert output == 99


def test_104_in_position_0_should_return_output_from_immediate_mode():
    input_value = 1337
    initial_state = [104, 8080, 99]
    final_state, output = compute_intcode_sequence(initial_state, input_value)

    assert output == 8080


def test_1105_in_position_0_should_jump_to_immediate_pointer_if_true_and_end_evaluation():
    input_value = 1337
    initial_state = [1105, 1, 8, 1, 1, 1, 1, 1, 99]
    final_state, output = compute_intcode_sequence(initial_state, input_value)

    assert final_state == [1105, 1, 8, 1, 1, 1, 1, 1, 99]


def test_5_in_position_0_should_jump_to_position_pointer_if_true_and_end_evalutation():
    input_value = 1337
    initial_state = [5, 1, 3, 8, 1, 1, 1, 1, 99]
    final_state, output = compute_intcode_sequence(initial_state, input_value)

    assert final_state == [5, 1, 3, 8, 1, 1, 1, 1, 99]


def test_1106_in_position_0_should_jump_to_immediate_pointer_if_false_and_end_evalutation():
    input_value = 1337
    initial_state = [1106, 0, 8, 8, 1, 1, 1, 1, 99]
    final_state, output = compute_intcode_sequence(initial_state, input_value)

    assert final_state == [1106, 0, 8, 8, 1, 1, 1, 1, 99]
