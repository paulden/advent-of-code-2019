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

from painting_robot import PaintingRobot


# def compute_intcode_sequence(sequence, input_value=None):
#     instruction_pointer = 0
#     relative_base = 0
#     output = []
#
#     while sequence[instruction_pointer] != EXIT_SEQUENCE_CODE:
#         instruction_as_string = BUFFER_FIRST_INSTRUCTION + str(sequence[instruction_pointer])
#         opcode = int(instruction_as_string[-2:])
#
#         first_parameter = sequence[instruction_pointer + 1]
#         first_parameter_mode = int(instruction_as_string[-3])
#         first_parameter_is_position_mode = first_parameter_mode == 0
#         first_parameter_is_immediate_mode = first_parameter_mode == 1
#         first_parameter_is_relative_mode = first_parameter_mode == 2
#
#         second_parameter = sequence[instruction_pointer + 2]
#         second_parameter_mode = int(instruction_as_string[-4])
#         second_parameter_is_position_mode = second_parameter_mode == 0
#         second_parameter_is_immediate_mode = second_parameter_mode == 1
#         second_parameter_is_relative_mode = second_parameter_mode == 2
#
#         if opcode == INPUT_OPCODE:
#             if first_parameter_is_position_mode:
#                 sequence[first_parameter] = input_value
#             else:
#                 sequence[relative_base + first_parameter] = input_value
#             instruction_pointer += 2
#             continue
#
#         if first_parameter_is_position_mode:
#             first_parameter_value = sequence[first_parameter]
#         elif first_parameter_is_immediate_mode:
#             first_parameter_value = first_parameter
#         elif first_parameter_is_relative_mode:
#             first_parameter_value = sequence[relative_base + first_parameter]
#
#         if opcode == OUTPUT_OPCODE:
#             output.append(first_parameter_value)
#             instruction_pointer += 2
#             continue
#
#         if opcode == ADJUST_RELATIVE_BASE_OPCODE:
#             relative_base += first_parameter_value
#             instruction_pointer += 2
#             continue
#
#         if second_parameter_is_position_mode:
#             second_parameter_value = sequence[second_parameter]
#         elif second_parameter_is_immediate_mode:
#             second_parameter_value = second_parameter
#         elif second_parameter_is_relative_mode:
#             second_parameter_value = sequence[relative_base + second_parameter]
#
#         third_parameter = sequence[instruction_pointer + 3]
#         third_parameter_mode = int(instruction_as_string[-5])
#         third_parameter_is_position_mode = third_parameter_mode == 0
#         third_parameter_position = third_parameter if third_parameter_is_position_mode else relative_base + third_parameter
#
#         if opcode == ADDITION_OPCODE:
#             sequence[third_parameter_position] = first_parameter_value + second_parameter_value
#             instruction_pointer += 4
#
#         elif opcode == MULTIPLICATION_OPCODE:
#             sequence[third_parameter_position] = first_parameter_value * second_parameter_value
#             instruction_pointer += 4
#
#         elif opcode == JUMP_IF_TRUE_OPCODE:
#             instruction_pointer = second_parameter_value if first_parameter_value != 0 else instruction_pointer + 3
#         elif opcode == JUMP_IF_FALSE_OPCODE:
#             instruction_pointer = second_parameter_value if first_parameter_value == 0 else instruction_pointer + 3
#         elif opcode == LESS_THAN_OPCODE:
#             sequence[third_parameter_position] = 1 if first_parameter_value < second_parameter_value else 0
#             instruction_pointer += 4
#         elif opcode == EQUALS_OPCODE:
#             sequence[third_parameter_position] = 1 if first_parameter_value == second_parameter_value else 0
#             instruction_pointer += 4
#
#     return sequence, output


def parse_intcode_sequence(input_sequence):
    return [int(number) for number in input_sequence.split(SEQUENCE_SEPARATOR)]


def paint_panels(panels, instruction, robot_position, robot_direction):
    panels[robot_position] = instruction[0]

    turn_left = instruction[1] == 0
    turn_right = not turn_left

    robot_direction = get_next_robot_direction(robot_direction, turn_left, turn_right)
    robot_position = get_next_robot_position(robot_direction, robot_position)

    return panels, robot_position, robot_direction


def get_next_robot_position(robot_direction, robot_position):
    if robot_direction == 'U':
        robot_position = (robot_position[0], robot_position[1] + 1)
    elif robot_direction == 'L':
        robot_position = (robot_position[0] - 1, robot_position[1])
    elif robot_direction == 'D':
        robot_position = (robot_position[0], robot_position[1] - 1)
    elif robot_direction == 'R':
        robot_position = (robot_position[0] + 1, robot_position[1])
    return robot_position


def get_next_robot_direction(robot_direction, turn_left, turn_right):
    if turn_left:
        if robot_direction == 'U':
            robot_direction = 'L'
        elif robot_direction == 'L':
            robot_direction = 'D'
        elif robot_direction == 'D':
            robot_direction = 'R'
        elif robot_direction == 'R':
            robot_direction = 'U'
    elif turn_right:
        if robot_direction == 'U':
            robot_direction = 'R'
        elif robot_direction == 'L':
            robot_direction = 'U'
        elif robot_direction == 'D':
            robot_direction = 'L'
        elif robot_direction == 'R':
            robot_direction = 'D'
    return robot_direction


def run_program_on_robot(robot, initial_input):
    robot_direction = 'U'
    robot_position = (0, 0)
    painted_panels = {}
    robot_next_input = initial_input
    while not robot.is_halted():
        color = robot.run(robot_next_input)
        direction = robot.run(robot_next_input)
        instruction = (color, direction)

        painted_panels, robot_position, robot_direction = paint_panels(painted_panels,
                                                                       instruction,
                                                                       robot_position,
                                                                       robot_direction)

        robot_next_input = painted_panels[robot_position] if robot_position in painted_panels else 0

    return painted_panels


if __name__ == '__main__':
    with open('./data/robot_program.txt') as program:
        painting_program = parse_intcode_sequence(program.read()) + [0] * 10000
        robot = PaintingRobot(painting_program)

        painted_panels_estimation = run_program_on_robot(robot, 0)

        robot_2 = PaintingRobot(painting_program)
        registration_identifier = run_program_on_robot(robot_2, 1)

        print('Part 1 - Number of painted panels: {}'.format(len(painted_panels_estimation)))
        print('Part 2 - Registration identifier:')
        for i in range(6):
            line = ''
            for j in range(50):
                if (j, -i) in registration_identifier:
                    line += '#' if registration_identifier[(j, -i)] == 1 else ' '
                else:
                    line += ' '
            print(line)

