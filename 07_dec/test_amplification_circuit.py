import pytest

from amplification_circuit import find_highest_signal, compute_thruster_signal, CLASSIC_SET_OF_SETTINGS

parametrized_data_test_thruster = [
    ([4, 3, 2, 1, 0], [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], 43210),
    ([0, 1, 2, 3, 4], [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], 54321),
    ([1, 0, 4, 3, 2], [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0], 65210)
]


@pytest.mark.parametrize('phase_setting_sequence,program,expected_output_signal', parametrized_data_test_thruster)
def test_compute_thruster_signal_should_return_output_from_last_amplifier_when_phase_setting_sequence_is_provided(phase_setting_sequence, program, expected_output_signal):
    output_signal = compute_thruster_signal(program, phase_setting_sequence)

    assert output_signal == expected_output_signal


parametrized_data_test_highest_signal = [
    ([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], 43210),
    ([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], 54321),
    ([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0], 65210)
]


@pytest.mark.parametrize('program,expected_highest_signal', parametrized_data_test_highest_signal)
def test_find_highest_signal_should_return_highest_possible_signal_when_program_is_provided(program, expected_highest_signal):
    highest_signal = find_highest_signal(program, CLASSIC_SET_OF_SETTINGS)

    assert highest_signal == expected_highest_signal


def test_compute_feedback_thruster_signal_should_return_output_from_last_amplifier_when_program_halts():
    program = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
    phase_setting_sequence = [9, 8, 7, 6, 5]
    output_signal = compute_thruster_signal(program, phase_setting_sequence)

    assert output_signal == 139629729


def test_compute_feedback_thruster_signal_should_return_output_from_last_amplifier_when_program_halts_2():
    program = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
               -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
               53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
    phase_setting_sequence = [9, 7, 8, 5, 6]
    output_signal = compute_thruster_signal(program, phase_setting_sequence)

    assert output_signal == 18216
