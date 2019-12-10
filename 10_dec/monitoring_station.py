import numpy as np

from math import gcd
from itertools import cycle


def find_best_monitoring_location(asteroid_map):
    asteroid_map_matrix = np.array(asteroid_map)
    asteroid_locations = np.argwhere(asteroid_map_matrix == 1)
    largest_number_of_asteroids = 0
    best_monitoring_location = tuple(asteroid_locations[0])
    for (i, j) in asteroid_locations:
        relative_locations = asteroid_locations - [i, j]
        slope_parameters = [tuple(location / gcd(*location)) for location in relative_locations if not np.array_equal(location, [0, 0])]
        current_number_of_asteroids_observed = len(set(slope_parameters))
        if current_number_of_asteroids_observed > largest_number_of_asteroids:
            largest_number_of_asteroids = current_number_of_asteroids_observed
            best_monitoring_location = (i, j)
    return best_monitoring_location, largest_number_of_asteroids


def get_order_of_vaporized_asteroids(asteroid_map, laser_location):
    asteroid_map_matrix = np.array(asteroid_map)
    asteroid_locations = np.argwhere(asteroid_map_matrix == 1)
    relative_locations = asteroid_locations - laser_location

    polar_coordinates = np.array([list(cartesian_to_polar(*location)) for location in relative_locations if not np.array_equal(location, [0, 0])])
    polar_coordinates_sorted_by_angle = polar_coordinates[polar_coordinates[:, 1].argsort()]
    unique_angles_cycle = cycle(np.unique(polar_coordinates_sorted_by_angle[:, 1]))

    asteroids_vaporized = []
    while len(asteroids_vaporized) < len(polar_coordinates):
        current_angle = next(unique_angles_cycle)
        matching_angle_locations = np.where(polar_coordinates_sorted_by_angle[:, 1] == current_angle)
        possible_locations = polar_coordinates_sorted_by_angle[matching_angle_locations]
        remaining_asteroids = [location for location in possible_locations if list(location) not in asteroids_vaporized]
        if len(remaining_asteroids) > 0:
            closest_asteroid = np.amin(remaining_asteroids, axis=0)
            asteroids_vaporized.append(list(closest_asteroid))

    cartesian_coordinates_asteroids_vaporized = [polar_to_cartesian(*location) for location in asteroids_vaporized]
    return np.array(cartesian_coordinates_asteroids_vaporized) + laser_location


def cartesian_to_polar(x, y):
    radius = np.sqrt(x**2 + y**2)
    angle = (1 - np.arctan2(y, x) / np.pi) * 180
    return radius, angle


def polar_to_cartesian(radius, angle):
    transformed_angle = (1 - angle / 180) * np.pi
    x = radius * np.cos(transformed_angle)
    y = radius * np.sin(transformed_angle)
    return round(x), round(y)


if __name__ == '__main__':
    with open('./data/asteroid_map.txt') as input_map:
        asteroid_map = []
        for line in input_map.read().splitlines():
            asteroid_map.append([0 if location == '.' else 1 for location in line])

        best_location, asteroids_observed = find_best_monitoring_location(asteroid_map)

        print('Part 1 - Best location for asteroid observation is {}, observing {} asteroids'.format(best_location, asteroids_observed))

        asteroids_vaporized = get_order_of_vaporized_asteroids(asteroid_map, best_location)
        y, x = asteroids_vaporized[199]
        answer = x * 100 + y
        print('Part 2 - 200th asteroid vaporized is in coordinates ({}, {}), answer is {}'.format(x, y, answer))
