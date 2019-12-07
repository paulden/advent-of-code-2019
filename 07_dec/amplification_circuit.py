from itertools import permutations
from amplifier import Amplifier

CLASSIC_SET_OF_SETTINGS = [0, 1, 2, 3, 4]
FEEBACK_LOOP_SET_OF_SETTINGS = [5, 6, 7, 8, 9]

SEQUENCE_SEPARATOR = ','


def find_highest_signal(program, set_of_settings):
    highest_signal = 0
    possible_settings = [setting for setting in permutations(set_of_settings)]
    for possible_setting in possible_settings:
        signal = compute_thruster_signal(program, possible_setting)
        if signal > highest_signal:
            highest_signal = signal
    return highest_signal


def compute_thruster_signal(program, setting_sequence):
    output_from_last_amp = 0
    current_amplifier_index = 0
    amplifiers = [Amplifier(program, setting) for setting in setting_sequence]
    final_amplifier = amplifiers[4]

    while not final_amplifier.is_halted():
        current_amplifier = amplifiers[current_amplifier_index]
        output_from_last_amp = current_amplifier.run(output_from_last_amp)
        current_amplifier_index = (current_amplifier_index + 1) % 5
    return final_amplifier.latest_output


def parse_intcode_sequence(input_sequence):
    return [int(number) for number in input_sequence.split(SEQUENCE_SEPARATOR)]


if __name__ == '__main__':
    with open('./data/amplification_controller_software.txt') as program:
        parsed_program = parse_intcode_sequence(program.read())

        highest_possible_signal = find_highest_signal(parsed_program, CLASSIC_SET_OF_SETTINGS)
        highest_possible_signal_using_feeback_loop = find_highest_signal(parsed_program, FEEBACK_LOOP_SET_OF_SETTINGS)
        print('Part 1 - Highest signal: {}'.format(highest_possible_signal))
        print('Part 2 - Highest signal: {}'.format(highest_possible_signal_using_feeback_loop))
