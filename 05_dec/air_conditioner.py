BUFFER_FIRST_INSTRUCTION = '00000'

ADDITION_OPCODE = 1
MULTIPLICATION_OPCODE = 2
INPUT_OPCODE = 3
OUTPUT_OPCODE = 4
JUMP_IF_TRUE_OPCODE = 5
JUMP_IF_FALSE_OPCODE = 6
LESS_THAN_OPCODE = 7
EQUALS_OPCODE = 8
EXIT_SEQUENCE_CODE = 99

SEQUENCE_SEPARATOR = ','


def compute_intcode_sequence(sequence, input_value=None):
    instruction_pointer = 0
    output = 0

    while sequence[instruction_pointer] != EXIT_SEQUENCE_CODE:
        first_instruction_as_string = BUFFER_FIRST_INSTRUCTION + str(sequence[instruction_pointer])
        opcode = int(first_instruction_as_string[-2:])

        first_parameter = sequence[instruction_pointer + 1]
        first_parameter_is_position_mode = int(first_instruction_as_string[-3]) == 0

        second_parameter = sequence[instruction_pointer + 2]
        second_parameter_is_position_mode = int(first_instruction_as_string[-4]) == 0

        if opcode == INPUT_OPCODE:
            sequence[first_parameter] = input_value
            instruction_pointer += 2
            continue

        first_parameter_value = sequence[first_parameter] if first_parameter_is_position_mode else first_parameter

        if opcode == OUTPUT_OPCODE:
            output = first_parameter_value
            instruction_pointer += 2
            continue

        second_parameter_value = sequence[second_parameter] if second_parameter_is_position_mode else second_parameter

        output_position = sequence[instruction_pointer + 3]
        if opcode == ADDITION_OPCODE:
            sequence[output_position] = first_parameter_value + second_parameter_value
            instruction_pointer += 4

        elif opcode == MULTIPLICATION_OPCODE:
            sequence[output_position] = first_parameter_value * second_parameter_value
            instruction_pointer += 4

        elif opcode == JUMP_IF_TRUE_OPCODE:
            instruction_pointer = second_parameter_value if first_parameter_value != 0 else instruction_pointer + 3
        elif opcode == JUMP_IF_FALSE_OPCODE:
            instruction_pointer = second_parameter_value if first_parameter_value == 0 else instruction_pointer + 3
        elif opcode == LESS_THAN_OPCODE:
            sequence[output_position] = 1 if first_parameter_value < second_parameter_value else 0
            instruction_pointer += 4
        elif opcode == EQUALS_OPCODE:
            sequence[output_position] = 1 if first_parameter_value == second_parameter_value else 0
            instruction_pointer += 4

    return sequence, output


def parse_intcode_sequence(input_sequence):
    return [int(number) for number in input_sequence.split(SEQUENCE_SEPARATOR)]


def process_intcode_program(input_sequence):
    parsed_sequence = parse_intcode_sequence(input_sequence)
    return compute_intcode_sequence(parsed_sequence)


if __name__ == '__main__':
    with open('./data/initial_sequence.txt') as initial_sequence:
        sequence = initial_sequence.read()
        parsed_initial_sequence = parse_intcode_sequence(sequence)

        first_part_final_sequence, first_part_output = compute_intcode_sequence(parsed_initial_sequence.copy(), 1)
        second_part_final_sequence, second_part_output = compute_intcode_sequence(parsed_initial_sequence.copy(), 5)
        print('Part 1 - Diagnostic code: {}'.format(first_part_output))
        print('Part 2 - Diagnostic code: {}'.format(second_part_output))
