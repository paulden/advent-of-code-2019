def compute_fuel_requirement(mass):
    computed_fuel = int(mass / 3) - 2
    fuel_requirement = max(0, computed_fuel)
    return fuel_requirement


def compute_total_fuel_requirement_for_module(mass):
    total_fuel_required = compute_fuel_requirement(mass)
    if total_fuel_required == 0:
        return 0
    else:
        additional_fuel_for_fuel = compute_total_fuel_requirement_for_module(total_fuel_required)
        return total_fuel_required + additional_fuel_for_fuel


if __name__ == '__main__':
    first_part_fuel_required = 0
    second_part_fuel_required = 0
    with open('./data/module_masses.txt') as module_masses:
        for module_mass in module_masses:
            first_part_fuel_required += compute_fuel_requirement(int(module_mass))
            second_part_fuel_required += compute_total_fuel_requirement_for_module(int(module_mass))
        print('Part 1 - Initial fuel requirement: {}'.format(first_part_fuel_required))
        print('Part 2 - Initial fuel requirement: {}'.format(second_part_fuel_required))
