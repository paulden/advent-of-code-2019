from moon import Moon
from math import gcd

io_initial_position = (-13, 14, -7)
europa_initial_position = (-18, 9, 0)
ganymede_initial_position = (0, -3, -3)
callisto_initial_position = (-15, 3, -13)

io = Moon(io_initial_position)
europa = Moon(europa_initial_position)
ganymede = Moon(ganymede_initial_position)
callisto = Moon(callisto_initial_position)

initial_positions = [io_initial_position, europa_initial_position, ganymede_initial_position, callisto_initial_position]
jupiter_moons = [io, europa, ganymede, callisto]

surrounding_moons = {
    io: [europa, ganymede, callisto],
    europa: [io, ganymede, callisto],
    ganymede: [io, europa, callisto],
    callisto: [io, europa, ganymede],
}


def simulate_moons_motion():
    for step in range(1000):
        for moon in jupiter_moons:
            moon.get_next_velocity(surrounding_moons[moon])
        for moon in jupiter_moons:
            moon.get_next_position()


def update_positions_and_velocities(positions, velocities):
    moons_count = len(positions)
    for moon in range(moons_count):
        for other_moon in range(moons_count):
            if positions[moon] > positions[other_moon]:
                velocities[moon] -= 1
            elif positions[moon] < positions[other_moon]:
                velocities[moon] += 1

    for moon in range(moons_count):
        positions[moon] += velocities[moon]

    return positions, velocities


def lcd(a, b):
    return abs(a * b) // gcd(a, b)


def get_minimal_period(positions, velocities):
    past_positions = set()
    step = 0
    while True:
        update_positions_and_velocities(positions, velocities)
        position_hash = hash(tuple(zip(positions, velocities)))
        if position_hash in past_positions:
            return step
        else:
            past_positions.add(position_hash)
            step += 1


if __name__ == '__main__':
    simulate_moons_motion()
    total_system_energy = sum([moon.get_total_energy() for moon in jupiter_moons])
    print('Part 1 - Total energy in the system: {}'.format(total_system_energy))

    x_positions = [moon[0] for moon in initial_positions]
    y_positions = [moon[1] for moon in initial_positions]
    z_positions = [moon[2] for moon in initial_positions]

    x_velocities = [0] * 4
    y_velocities = [0] * 4
    z_velocities = [0] * 4

    x_period = get_minimal_period(x_positions, x_velocities)
    y_period = get_minimal_period(y_positions, y_velocities)
    z_period = get_minimal_period(z_positions, z_velocities)

    common_period = lcd(lcd(x_period, y_period), z_period)

    print('Part 2 - Steps until system returns to a previous state: {}'.format(common_period))
