RIGHT_MOVE_LABEL = 'R'
LEFT_MOVE_LABEL = 'L'
UP_MOVE_LABEL = 'U'
DOWN_MOVE_LABEL = 'D'

SEQUENCE_SEPARATOR = ','


def find_closest_distance(first_wire_path, second_wire_path):
    crossing_points = find_crossing_points(first_wire_path, second_wire_path)
    manhattan_distances = [compute_manhattan_distance(crossing_point) for crossing_point in crossing_points]
    return min(manhattan_distances)


def find_fewest_steps(first_wire_path, second_wire_path):
    first_wire_visited_points = list_visited_points(first_wire_path)
    second_wire_visited_points = list_visited_points(second_wire_path)
    crossing_points = find_crossing_points(first_wire_path, second_wire_path)
    steps_for_crossing_points = []
    for crossing_point in crossing_points:
        steps_in_first_path = first_wire_visited_points.index(crossing_point) + 1
        steps_in_second_path = second_wire_visited_points.index(crossing_point) + 1
        steps_for_crossing_points.append(steps_in_first_path + steps_in_second_path)
    return min(steps_for_crossing_points)


def find_crossing_points(first_wire_path, second_wire_path):
    first_wire_visited_points = list_visited_points(first_wire_path)
    second_wire_visited_points = list_visited_points(second_wire_path)
    return list(set(first_wire_visited_points) & set(second_wire_visited_points))


def list_visited_points(moves):
    visited_points = []
    current_position = (0, 0)
    for move in moves:
        direction = move[0]
        steps = int(move[1:])
        for step in range(steps):
            current_position = move_position(current_position, direction)
            visited_points.append(current_position)
    return visited_points


def move_position(current_position, direction):
    x_position = current_position[0]
    y_position = current_position[1]
    new_position = current_position
    if direction == RIGHT_MOVE_LABEL:
        new_position = (x_position + 1, y_position)
    elif direction == LEFT_MOVE_LABEL:
        new_position = (x_position - 1, y_position)
    elif direction == UP_MOVE_LABEL:
        new_position = (x_position, y_position + 1)
    elif direction == DOWN_MOVE_LABEL:
        new_position = (x_position, y_position - 1)
    return new_position


def parse_wire_path(wire_path):
    return [move for move in wire_path.split(SEQUENCE_SEPARATOR)]


def compute_manhattan_distance(origin, destination=(0, 0)):
    return abs(origin[0] - destination[0]) + abs(origin[1] - destination[1])


if __name__ == '__main__':
    with open('./data/wire_paths.txt') as wire_paths:
        first_wire_moves = parse_wire_path(wire_paths.readline())
        second_wire_moves = parse_wire_path(wire_paths.readline())

        closest_distance = find_closest_distance(first_wire_moves, second_wire_moves)
        fewest_steps_required = find_fewest_steps(first_wire_moves, second_wire_moves)

        print('Part 1 - Closest distance in crossing points: {}'.format(closest_distance))
        print('Part 2 - Fewest steps: {}'.format(fewest_steps_required))
