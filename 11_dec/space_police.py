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

