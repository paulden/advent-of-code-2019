import pytest

from monitoring_station import find_best_monitoring_location, cartesian_to_polar, polar_to_cartesian


def test_find_best_monitoring_location_should_return_0_0_and_number_asteroids_seend_when_only_one_asteroid_in_0_0():
    asteroid_map = [[1, 0],
                    [0, 0]]
    best_location, asteroids_observed_count = find_best_monitoring_location(asteroid_map)

    assert best_location == (0, 0)
    assert asteroids_observed_count == 0


def test_find_best_monitoring_location_should_return_1_1_and_number_asteroids_seend_when_only_one_asteroid_in_1_1():
    asteroid_map = [[0, 0],
                    [0, 1]]
    best_location, asteroids_observed_count = find_best_monitoring_location(asteroid_map)

    assert best_location == (1, 1)
    assert asteroids_observed_count == 0


def test_find_best_monitoring_location_should_return_1_0_and_number_asteroids_seend_when_most_asteroids_seen_on_line():
    asteroid_map = [[1, 1, 1],
                    [0, 0, 0]]
    best_location, asteroids_observed_count = find_best_monitoring_location(asteroid_map)

    assert best_location == (0, 1)
    assert asteroids_observed_count == 2


def test_find_best_monitoring_location_should_return_1_0_and_number_asteroids_seend_when_most_asteroids_seen_on_line_and_up():
    asteroid_map = [[1, 0, 1, 1],
                    [0, 0, 1, 0]]
    best_location, asteroids_observed_count = find_best_monitoring_location(asteroid_map)

    assert best_location == (0, 2)
    assert asteroids_observed_count == 3


def test_find_best_monitoring_location_should_return_3_4_and_number_asteroids_seend_when_most_asteroids_seen_on_all_map():
    asteroid_map = [[0, 1, 0, 0, 1],
                    [0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 1],
                    [0, 0, 0, 1, 1]]
    best_location, asteroids_observed_count = find_best_monitoring_location(asteroid_map)

    assert best_location == (4, 3)
    assert asteroids_observed_count == 8


data_test_cartesian_to_polar = [
    ([-1, 0], 1, 0),
    ([0, 1], 1, 90),
    ([1, 0], 1, 180),
    ([0, -1], 1, 270),
]


@pytest.mark.parametrize('relative_coordinates,expected_radius,expected_angle', data_test_cartesian_to_polar)
def test_cartesian_to_polar_location_should_return_increasing_angle_with_radius_equal_to_1(relative_coordinates, expected_radius, expected_angle):
    radius, angle = cartesian_to_polar(*relative_coordinates)

    assert radius == expected_radius
    assert angle == expected_angle


data_test_polar_to_cartesian = [
    ([1, 0], -1, 0),
    ([1, 90], 0, 1),
    ([1, 180], 1, 0),
    ([1, 270], 0, -1),
]


@pytest.mark.parametrize('polar_coordinates,expected_i,expected_j', data_test_polar_to_cartesian)
def test_polar_to_cartesian_location_should_return_relative_locations(polar_coordinates, expected_i, expected_j):
    i, j = polar_to_cartesian(*polar_coordinates)

    assert i == expected_i
    assert j == expected_j