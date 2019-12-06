from universal_orbit_map import count_orbits, find_minimum_orbital_transfers


def test_count_orbits_should_return_1_when_B_orbits_COM():
    map_orbit = {'B': 'COM'}
    orbit_count = count_orbits(map_orbit)

    assert orbit_count == 1


def test_count_orbits_should_return_2_when_B_orbits_COM_and_C_orbits_COM():
    map_orbit = {'B': 'COM', 'C': 'COM'}
    orbit_count = count_orbits(map_orbit)

    assert orbit_count == 2


def test_count_orbits_should_return_3_when_B_orbits_COM_and_C_orbits_B():
    map_orbit = {'B': 'COM', 'C': 'B'}
    orbit_count = count_orbits(map_orbit)

    assert orbit_count == 3


def test_count_orbits_should_return_42_in_example_from_advent_of_code():
    map_orbit = {
        'B': 'COM',
        'C': 'B',
        'D': 'C',
        'E': 'D',
        'F': 'E',
        'G': 'B',
        'H': 'G',
        'I': 'D',
        'J': 'E',
        'K': 'J',
        'L': 'K'
    }
    orbit_count = count_orbits(map_orbit)

    assert orbit_count == 42


def test_find_minimum_orbital_transfers_should_return_0_when_orbit_is_the_same():
    map_bidirectional_orbit = {
        'B': ['COM', 'YOU', 'SAN'],
        'YOU': ['B'],
        'SAN': ['B']
    }
    minimum_orbital_transfers = find_minimum_orbital_transfers(map_bidirectional_orbit, 'YOU', 'SAN')

    assert minimum_orbital_transfers == 0


def test_find_minimum_orbital_transfers_should_return_1_when_orbit_is_one_object_away():
    map_bidirectional_orbit = {
        'B': ['COM', 'C', 'SAN'],
        'YOU': ['C'],
        'SAN': ['B'],
        'C': ['B', 'YOU'],
    }
    minimum_orbital_transfers = find_minimum_orbital_transfers(map_bidirectional_orbit, 'YOU', 'SAN')

    assert minimum_orbital_transfers == 1


def test_find_minimum_orbital_transfers_should_return_4_when_orbit_is_four_objects_away():

    map_bidirectional_orbit = {
        'B': ['COM', 'F', 'C'],
        'C': ['B', 'D'],
        'D': ['C', 'E'],
        'E': ['D', 'YOU'],
        'YOU': ['E'],
        'F': ['B', 'SAN'],
        'SAN': ['F'],
    }
    minimum_orbital_transfers = find_minimum_orbital_transfers(map_bidirectional_orbit, 'YOU', 'SAN')

    assert minimum_orbital_transfers == 4
