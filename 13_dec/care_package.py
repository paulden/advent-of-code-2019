BUFFER_FIRST_INSTRUCTION = '00000'

ADDITION_OPCODE = 1
MULTIPLICATION_OPCODE = 2
INPUT_OPCODE = 3
OUTPUT_OPCODE = 4
JUMP_IF_TRUE_OPCODE = 5
JUMP_IF_FALSE_OPCODE = 6
LESS_THAN_OPCODE = 7
EQUALS_OPCODE = 8
ADJUST_RELATIVE_BASE_OPCODE = 9
EXIT_SEQUENCE_CODE = 99

SEQUENCE_SEPARATOR = ','


def compute_intcode_sequence(sequence, input_value=None):
    instruction_pointer = 0
    relative_base = 0
    output = []

    while sequence[instruction_pointer] != EXIT_SEQUENCE_CODE:
        instruction_as_string = BUFFER_FIRST_INSTRUCTION + str(sequence[instruction_pointer])
        opcode = int(instruction_as_string[-2:])

        first_parameter = sequence[instruction_pointer + 1]
        first_parameter_mode = int(instruction_as_string[-3])
        first_parameter_is_position_mode = first_parameter_mode == 0
        first_parameter_is_immediate_mode = first_parameter_mode == 1
        first_parameter_is_relative_mode = first_parameter_mode == 2

        second_parameter = sequence[instruction_pointer + 2]
        second_parameter_mode = int(instruction_as_string[-4])
        second_parameter_is_position_mode = second_parameter_mode == 0
        second_parameter_is_immediate_mode = second_parameter_mode == 1
        second_parameter_is_relative_mode = second_parameter_mode == 2

        if opcode == INPUT_OPCODE:
            all_tiles_dict = {}
            for i in range(0, len(output), 3):
                all_tiles_dict[(output[i], output[i + 1])] = output[i + 2]

            for tile in all_tiles_dict:
                if tile[0] == -1:
                    print('Current score: {}'.format(all_tiles_dict[tile]))
                if all_tiles_dict[tile] == 4:
                    ball_position = tile
                    print('Ball position: {}'.format(ball_position))
                if all_tiles_dict[tile] == 3:
                    paddle_position = tile
                    print('Paddle position: {}'.format(paddle_position))

            if ball_position[0] > paddle_position[0]:
                input_value = 1
            elif ball_position[0] < paddle_position[0]:
                input_value = -1
            else:
                input_value = 0

            render_game(output)

            if first_parameter_is_position_mode:
                sequence[first_parameter] = input_value
            else:
                sequence[relative_base + first_parameter] = input_value
            instruction_pointer += 2
            continue

        if first_parameter_is_position_mode:
            first_parameter_value = sequence[first_parameter]
        elif first_parameter_is_immediate_mode:
            first_parameter_value = first_parameter
        elif first_parameter_is_relative_mode:
            first_parameter_value = sequence[relative_base + first_parameter]

        if opcode == OUTPUT_OPCODE:
            output.append(first_parameter_value)
            instruction_pointer += 2
            continue

        if opcode == ADJUST_RELATIVE_BASE_OPCODE:
            relative_base += first_parameter_value
            instruction_pointer += 2
            continue

        if second_parameter_is_position_mode:
            second_parameter_value = sequence[second_parameter]
        elif second_parameter_is_immediate_mode:
            second_parameter_value = second_parameter
        elif second_parameter_is_relative_mode:
            second_parameter_value = sequence[relative_base + second_parameter]

        third_parameter = sequence[instruction_pointer + 3]
        third_parameter_mode = int(instruction_as_string[-5])
        third_parameter_is_position_mode = third_parameter_mode == 0
        third_parameter_position = third_parameter if third_parameter_is_position_mode else relative_base + third_parameter

        if opcode == ADDITION_OPCODE:
            sequence[third_parameter_position] = first_parameter_value + second_parameter_value
            instruction_pointer += 4

        elif opcode == MULTIPLICATION_OPCODE:
            sequence[third_parameter_position] = first_parameter_value * second_parameter_value
            instruction_pointer += 4

        elif opcode == JUMP_IF_TRUE_OPCODE:
            instruction_pointer = second_parameter_value if first_parameter_value != 0 else instruction_pointer + 3
        elif opcode == JUMP_IF_FALSE_OPCODE:
            instruction_pointer = second_parameter_value if first_parameter_value == 0 else instruction_pointer + 3
        elif opcode == LESS_THAN_OPCODE:
            sequence[third_parameter_position] = 1 if first_parameter_value < second_parameter_value else 0
            instruction_pointer += 4
        elif opcode == EQUALS_OPCODE:
            sequence[third_parameter_position] = 1 if first_parameter_value == second_parameter_value else 0
            instruction_pointer += 4

    return sequence, output


def parse_intcode_sequence(input_sequence):
    return [int(number) for number in input_sequence.split(SEQUENCE_SEPARATOR)]


def process_intcode_program(input_sequence):
    parsed_sequence = parse_intcode_sequence(input_sequence)
    return compute_intcode_sequence(parsed_sequence)


def render_game(output):
    all_tiles_dict = {}
    for i in range(0, len(output), 3):
        all_tiles_dict[(output[i], output[i + 1])] = output[i + 2]
    for i in range(30):
        game_line = ''
        for j in range(100):
            if (j, i) in all_tiles_dict:
                tile = all_tiles_dict[(j, i)]
                if tile == 0:
                    game_line += '  '
                elif tile == 1:
                    game_line += '##'
                elif tile == 2:
                    game_line += '██'
                elif tile == 3:
                    game_line += '=='
                elif tile == 4:
                    game_line += '@@'
        print(game_line)


if __name__ == '__main__':
    with open('./data/game_program.txt') as initial_sequence:
        program = initial_sequence.read()
        game_program = parse_intcode_sequence(program) + [0] * 10000

        final_state, output = compute_intcode_sequence(game_program.copy())

        block_tiles = [(output[i], output[i + 1]) for i in range(0, len(output), 3) if output[i + 2] == 2]
        print('Part 1 - Number of block tiles'.format(len(block_tiles)))

        new_game_program = game_program.copy()
        new_game_program[0] = 2

        final_state_game_mode, output = compute_intcode_sequence(new_game_program)
        for i in range(len(output)):
            if output[i] == -1:
                print('Part 2 - Final score: {}'.format(output[i + 2]))

