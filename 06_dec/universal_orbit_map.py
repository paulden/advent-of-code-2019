from collections import defaultdict

CENTER_OF_MASS = 'COM'

CURRENT_ORBIT_POSITION = 'YOU'
SANTA_ORBIT_POSITION = 'SAN'


def count_orbits(map_data):
    orbit_counts = 0
    for orbiting_object in map_data:
        orbit_counts += count_orbits_from_object(orbiting_object, map_data)
    return orbit_counts


def count_orbits_from_object(orbiting_object, map_data):
    object_orbited_around = map_data[orbiting_object]
    if object_orbited_around == CENTER_OF_MASS:
        return 1
    else:
        return 1 + count_orbits_from_object(object_orbited_around, map_data)


def find_minimum_orbital_transfers(bidirectional_orbits, start_object, end_object):
    shortest_path = find_shortest_path(bidirectional_orbits, start_object, end_object, [])
    return len(shortest_path) - 3


def find_shortest_path(bidirectional_orbits, start_object, end_object, path):
    path = path + [start_object]

    if start_object == end_object:
        return path

    if start_object not in bidirectional_orbits:
        return None

    shortest_path = None

    for orbiting_object in bidirectional_orbits[start_object]:
        if orbiting_object not in path:
            new_path_explored = find_shortest_path(bidirectional_orbits, orbiting_object, end_object, path)
            if new_path_explored:
                if not shortest_path or len(new_path_explored) < len(shortest_path):
                    shortest_path = new_path_explored
    return shortest_path


if __name__ == '__main__':
    with open('./data/orbit_map.txt') as orbit_map:
        map_data = {}
        map_data_bidirectional = defaultdict(list)
        for orbit in orbit_map.read().splitlines():
            object_orbited_around, object_orbiting = orbit.split(')')
            map_data[object_orbiting] = object_orbited_around
            map_data_bidirectional[object_orbiting].append(object_orbited_around)
            map_data_bidirectional[object_orbited_around].append(object_orbiting)

        total_number_of_orbits = count_orbits(map_data)
        minimim_orbital_transfers = find_minimum_orbital_transfers(map_data_bidirectional, CURRENT_ORBIT_POSITION, SANTA_ORBIT_POSITION)

        print('Part 1 - Total number of orbits: {}'.format(total_number_of_orbits))
        print('Part 2 - Minimum number of transfers: {}'.format(minimim_orbital_transfers))
