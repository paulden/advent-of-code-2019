import re
from collections import defaultdict
from math import ceil
from statistics import median


def parse_volume_and_name(data):
    volume = int(re.findall(r'\d+', data)[0])
    name = re.findall('[A-Z]+', data)[0]
    return volume, name


def get_components_required_and_volume_created(name, volume, reactions_list):
    for target, components in reactions_list.items():
        target_volume, target_name = target
        if target_name == name:
            reactions_to_trigger = ceil(volume / target_volume)
            volume_created = target_volume * reactions_to_trigger
            components_required = [(component[0] * reactions_to_trigger, component[1]) for component in components]
            return components_required, volume_created


def get_ore_needed(chemicals_to_create):
    total_ore_needed = 0
    inventory = defaultdict(int)

    while len(chemicals_to_create) > 0:
        next_round_of_chemicals_to_create = []

        for chemical in chemicals_to_create:
            chemical_volume, chemical_name = chemical
            if chemical_name == 'ORE':
                total_ore_needed += chemical_volume
            elif chemical_name in inventory:
                volume_to_create = chemical_volume - inventory[chemical_name]
                if volume_to_create > 0:
                    inventory.pop(chemical_name)
                    next_round_of_chemicals_to_create.append((volume_to_create, chemical_name))
                else:
                    inventory[chemical_name] -= chemical_volume
            else:
                next_components, volume_created = get_components_required_and_volume_created(chemical_name,
                                                                                             chemical_volume, reactions)
                if volume_created > chemical_volume:
                    inventory[chemical_name] += volume_created - chemical_volume
                next_round_of_chemicals_to_create.extend(next_components)

        chemicals_to_create = next_round_of_chemicals_to_create
    return total_ore_needed


if __name__ == '__main__':
    with open('data/reactions.txt') as reactions_data:
        reactions = {}
        for reaction_string in reactions_data.read().splitlines():
            components_string, target_string = reaction_string.split('=>')
            components = [parse_volume_and_name(component) for component in components_string.split(',')]
            target = parse_volume_and_name(target_string)
            reactions[target] = components

        empty_inventory = defaultdict(int)
        ore_needed = get_ore_needed([(1, 'FUEL')])
        print('Part 1 - Ore needed to produce 1 FUEL: {}'.format(ore_needed))

        ore_available = 1000000000000
        min_range = 0
        max_range = ore_available
        pivot_point = int(median([min_range, max_range]))

        while max_range - min_range > 1:

            ore_consumed = get_ore_needed([(pivot_point, 'FUEL')])
            if ore_available - ore_consumed < 0:
                max_range = pivot_point
            else:
                min_range = pivot_point
            pivot_point = int(median([min_range, max_range]))

        print('Part 2 - Maximum amount of fuel produced for {} ores: {}'.format(ore_available, pivot_point))
