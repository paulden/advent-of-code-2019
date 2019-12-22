from collections import defaultdict, deque

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
    input_pointer = 0
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
            if first_parameter_is_position_mode:
                sequence[first_parameter] = input_value[input_pointer]
            else:
                sequence[relative_base + first_parameter] = input_value[input_pointer]
            input_pointer += 1
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


def get_or_default(matrix, i, j, default=0):
    print(j, i)

    if 0 <= j < len(matrix) and 0 <= i < len(matrix[0]):
        return matrix[j][i]
    else:
        return default


def shortestPathLength(graph):
    N = len(graph)
    dist = [[float('inf')] * N for i in range(1 << N)]
    for x in range(N):
        dist[1 << x][x] = 0

    for cover in range(1 << N):
        repeat = True
        while repeat:
            repeat = False
            for head, d in enumerate(dist[cover]):
                for nei in graph[head]:
                    cover2 = cover | (1 << nei)
                    if d + 1 < dist[cover2][nei]:
                        dist[cover2][nei] = d + 1
                        if cover == cover2:
                            repeat = True

    return min(dist[2 ** N - 1])


if __name__ == '__main__':
    with open('./data/ascii.txt') as initial_sequence:
        program = initial_sequence.read()
        ascii_program = parse_intcode_sequence(program) + [0] * 10000

        final_state, output = compute_intcode_sequence(ascii_program.copy())

        rendered_map = ''.join([chr(tile) for tile in output])

        array_map = []
        line = []
        for tile in output:
            if tile == 10 and len(line) > 0:
                array_map.append(line)
                line = []
            else:
                line.append(tile)
        print(rendered_map)
        graph_points = defaultdict(set)

        map_height = len(array_map)
        map_width = len(array_map[0])
        for j in range(map_height):
            for i in range(map_width):
                if array_map[j][i] != 35:
                    continue
                if i > 0 and array_map[j][i - 1] == 35:
                    graph_points[(i, j)].add((i - 1, j))
                    graph_points[(i - 1, j)].add((i, j))
                if i < map_width - 1 and array_map[j][i + 1] == 35:
                    graph_points[(i, j)].add((i + 1, j))
                    graph_points[(i + 1, j)].add((i, j))
                if j > 0 and array_map[j - 1][i] == 35:
                    graph_points[(i, j)].add((i, j - 1))
                    graph_points[(i, j - 1)].add((i, j))
                if j < map_height - 1 and array_map[j + 1][i] == 35:
                    graph_points[(i, j)].add((i, j + 1))
                    graph_points[(i, j + 1)].add((i, j))

        total = 0
        for j in range(1, map_height - 1):
            line = ''
            for i in range(1, map_width - 1):
                if array_map[j][i] == 35 and array_map[j - 1][i] == 35 and array_map[j - 1][i] == 35 and array_map[j][i - 1] == 35 and array_map[j][i + 1] == 35:
                    line += 'O'
                    total += i * j
                else:
                    line += chr(array_map[j][i])
        print('Part 1 - Number of intersections: {}'.format(total))

        active_ascii_program = ascii_program.copy() + [0] * 10000
        active_ascii_program[0] = 2

        # Ok, I solved this one by hand with pen and paper...
        main_command = 'A,B,A,B,C,C,B,A,B,C'
        function_a = 'L,12,L,6,L,8,R,6'
        function_b = 'L,8,L,8,R,4,R,6,R,6'
        function_c = 'L,12,R,6,L,8'
        feed = 'n'

        main_command_ascii = [ord(character) for character in main_command]
        function_a_ascii = [ord(character) for character in function_a]
        function_b_ascii = [ord(character) for character in function_b]
        function_c_ascii = [ord(character) for character in function_c]
        feed_ascii = [ord(character) for character in feed.split(',')]

        total_command = main_command_ascii + [10] + function_a_ascii + [10] + function_b_ascii + [10] + function_c_ascii + [10] + feed_ascii + [10]

        final_state, output = compute_intcode_sequence(active_ascii_program, total_command)
        # print(''.join([chr(tile) for tile in output]))
        print('Part 2 - Dust collected: {}'.format([tile for tile in output if tile > 128][0]))