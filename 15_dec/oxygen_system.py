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

from repair_droid import RepairDroid
import random
import time
from collections import defaultdict


def parse_intcode_sequence(input_sequence):
    return [int(number) for number in input_sequence.split(SEQUENCE_SEPARATOR)]


def get_next_movement(visited_points, current_location):
    next_locations = {
        (current_location[0], current_location[1] + 1): 1,
        (current_location[0], current_location[1] - 1): 2,
        (current_location[0] - 1, current_location[1]): 3,
        (current_location[0] + 1, current_location[1]): 4
    }

    unknown_locations = [next_locations[location] for location in next_locations.keys() if location not in visited_points]

    if len(unknown_locations) > 0:
        return random.choice(unknown_locations)

    possible_locations = [next_locations[location] for location in next_locations.keys() if visited_points[location] > 0]
    return random.choice(possible_locations)


def get_possible_points(visited_points, current_location):
    next_locations = [
        (current_location[0], current_location[1] + 1),
        (current_location[0], current_location[1] - 1),
        (current_location[0] - 1, current_location[1]),
        (current_location[0] + 1, current_location[1])
    ]

    return [location for location in next_locations if location not in visited_points]


def render_map(visited_points):
    for i in range(-20, 50):
        line = ''
        for j in range(-100, 100):
            if (j, i) == current_location:
                line += 'D'
            elif (i, j) == (0, 0):
                line += 'X'
            else:
                if (j, i) in visited_points:
                    if visited_points[(j, i)] == 1:
                        line += '.'
                    elif visited_points[(j, i)] == 0:
                        line += '#'
                    elif visited_points[(j, i)] == 2:
                        line += 'O'
                else:
                    line += ' '
        print(line)


def find_shortest_path(graph, start, end, path):
    path = path + [start]

    if start == end:
        return path

    if start not in graph:
        return None

    shortest_path = None

    for node in graph[start]:
        if node not in path:
            new_path_explored = find_shortest_path(graph, node, end, path)
            if new_path_explored:
                if not shortest_path or len(new_path_explored) < len(shortest_path):
                    shortest_path = new_path_explored
                else:
                    continue
    return shortest_path


def find_path(graph, start, end, path):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None


def get_commands(path):
    commands = []
    current_location = path[0]

    for i in range(1, len(path)):
        next_locations = {
            (current_location[0], current_location[1] + 1): 1,
            (current_location[0], current_location[1] - 1): 2,
            (current_location[0] - 1, current_location[1]): 3,
            (current_location[0] + 1, current_location[1]): 4
        }
        commands.append(next_locations[path[i]])
        current_location = path[i]

    return commands


if __name__ == '__main__':
    with open('./data/repair_program.txt') as program:
        painting_program = parse_intcode_sequence(program.read()) + [0] * 10000
        robot = RepairDroid(painting_program)

        current_location = (0, 0)
        visited_points = {
            (0, 0): 1
        }
        graph_points = defaultdict(set)
        points_to_visit = set()
        adjacent_non_visited_points = get_possible_points(visited_points, current_location)

        for point in adjacent_non_visited_points:
            graph_points[current_location].add(point)
            graph_points[point].add(current_location)

        points_to_visit.update(adjacent_non_visited_points)
        status_code = 0

        while len(points_to_visit) > 0:
            next_point_to_visit = points_to_visit.pop()

            print('Visiting: {}'.format(next_point_to_visit))
            path = find_shortest_path(graph_points, current_location, next_point_to_visit, [])
            commands = get_commands(path)

            for command in commands:
                status_code = robot.run(command)
                if command == 1:
                    target_location = (current_location[0], current_location[1] + 1)
                elif command == 2:
                    target_location = (current_location[0], current_location[1] - 1)
                elif command == 3:
                    target_location = (current_location[0] - 1, current_location[1])
                elif command == 4:
                    target_location = (current_location[0] + 1, current_location[1])

                visited_points[target_location] = status_code
                if status_code != 0:
                    current_location = target_location

                adjacent_non_visited_points = get_possible_points(visited_points, current_location)

                for point in adjacent_non_visited_points:
                    graph_points[current_location].add(point)
                    graph_points[point].add(current_location)

                points_to_visit.update(adjacent_non_visited_points)
                render_map(visited_points)

            blocked_points = []
            for point in graph_points:
                if point in visited_points and visited_points[point] == 0:
                    blocked_points.append(point)

            for point in blocked_points:
                graph_points.pop(point, None)

        oxygen_location = [location for location in visited_points if visited_points[location] == 2][0]
        path = find_shortest_path(graph_points, (0, 0), oxygen_location, [])
        commands = get_commands(path)

        non_filled_points = set([location for location in visited_points if visited_points[location] == 1])
        filled_points = set([location for location in visited_points if visited_points[location] == 2])

        minutes_elapsed = 0
        while len(non_filled_points) > 0:
            print(len(non_filled_points))
            minutes_elapsed += 1
            for filled_point in filled_points:
                adjacent_points = [
                    (filled_point[0], filled_point[1] + 1),
                    (filled_point[0], filled_point[1] - 1),
                    (filled_point[0] - 1, filled_point[1]),
                    (filled_point[0] + 1, filled_point[1])
                ]

                for point in adjacent_points:
                    if visited_points[point] == 1:
                        visited_points[point] = 2

            non_filled_points = set([location for location in visited_points if visited_points[location] == 1])
            filled_points = set([location for location in visited_points if visited_points[location] == 2])
            render_map(visited_points)

        print('Part 1 - Shortest path to oxygen hole: {}'.format(len(commands)))
        print('Part 2 - {} minutes required to fill oxygen'.format(minutes_elapsed))
