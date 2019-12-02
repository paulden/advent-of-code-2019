INSTRUCTION_LENGTH = 4

MULTIPLICATION_OPCODE = 2
ADDITION_OPCODE = 1
EXIT_SEQUENCE_CODE = 99

SEQUENCE_SEPARATOR = ','


def compute_intcode_sequence(sequence):
    instruction_pointer = 0
    while sequence[instruction_pointer] != EXIT_SEQUENCE_CODE:
        sequence = evaluate_instruction(sequence, instruction_pointer)
        instruction_pointer += INSTRUCTION_LENGTH
    return sequence


def evaluate_instruction(sequence, instruction_pointer):
    final_sequence = sequence.copy()

    opcode = sequence[instruction_pointer]
    first_parameter = sequence[1 + instruction_pointer]
    second_parameter = sequence[2 + instruction_pointer]
    output_position = sequence[3 + instruction_pointer]

    if first_parameter >= len(sequence) or second_parameter >= len(sequence) or output_position >= len(sequence):
        return final_sequence

    if opcode == ADDITION_OPCODE:
        final_sequence[output_position] = sequence[first_parameter] + sequence[second_parameter]
    elif opcode == MULTIPLICATION_OPCODE:
        final_sequence[output_position] = sequence[first_parameter] * sequence[second_parameter]
    return final_sequence


def parse_intcode_sequence(input_sequence):
    return [int(number) for number in input_sequence.split(SEQUENCE_SEPARATOR)]


def process_intcode_program(input_sequence):
    parsed_sequence = parse_intcode_sequence(input_sequence)
    return compute_intcode_sequence(parsed_sequence)


def find_possible_combinations(sequence, expected_output):
    possible_combinations = []

    for verb in range(100):
        for noun in range(100):
            current_sequence = sequence.copy()
            current_sequence[1] = verb
            current_sequence[2] = noun
            actual_output = compute_intcode_sequence(current_sequence)[0]
            if actual_output == expected_output:
                possible_combinations.append((verb, noun))

    return possible_combinations


if __name__ == '__main__':
    with open('./data/initial_sequence.txt') as initial_sequence:
        sequence = initial_sequence.read()
        parsed_initial_sequence = parse_intcode_sequence(sequence)

        parsed_initial_sequence[1] = 12
        parsed_initial_sequence[2] = 2
        processed_sequence = compute_intcode_sequence(parsed_initial_sequence)
        print('Part 1 - Updated Intcode sequence output: {}'.format(processed_sequence[0]))

        program_expected_output = 19690720
        input_verb, input_noun = find_possible_combinations(parsed_initial_sequence, program_expected_output)[0]
        print('Part 2 - Input verb and noun formula: {}'.format(input_verb * 100 + input_noun))
