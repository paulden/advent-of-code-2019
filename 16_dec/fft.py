from itertools import cycle, accumulate

BASE_PATTERN = [0, 1, 0, -1]


def transform_signal(original_signal):
    new_signal = []
    for i in range(len(original_signal)):

        pattern = []
        for element in BASE_PATTERN:
            pattern.extend([element] * (i + 1))

        pattern_cycle = cycle(pattern)
        next(pattern_cycle)

        transformation_result = sum([digit * next(pattern_cycle) for digit in original_signal])
        new_digit = abs(transformation_result) % 10
        new_signal.append(new_digit)

    return new_signal


def transform_signal_partly(digits):
    # Here, the offset indicates we only need the second half of the matrix so only cumulative sum part
    cumulative_sum = accumulate(digits)
    return [abs(number) % 10 for number in cumulative_sum]


if __name__ == '__main__':
    signal = '59708072843556858145230522180223745694544745622336045476506437914986923372260274801316091345126141549522285839402701823884690004497674132615520871839943084040979940198142892825326110513041581064388583488930891380942485307732666485384523705852790683809812073738758055115293090635233887206040961042759996972844810891420692117353333665907710709020698487019805669782598004799421226356372885464480818196786256472944761036204897548977647880837284232444863230958576095091824226426501119748518640709592225529707891969295441026284304137606735506294604060549102824977720776272463738349154440565501914642111802044575388635071779775767726626682303495430936326809'
    signal_digits = [int(digit) for digit in signal]

    for _ in range(100):
        signal_digits = transform_signal(signal_digits)
    result = ''.join(str(digit) for digit in signal_digits[:8])
    print('Part 1 - First eight digits after 100 transformations: {}'.format(result))

    signal_digits = [int(digit) for digit in signal]
    offset = int(signal[:7])

    number_of_last_digits_required = 10000 * len(signal) - offset
    full_signal = signal_digits * 10000
    last_digits = [full_signal[-i - 1] for i in range(number_of_last_digits_required)]

    for _ in range(100):
        last_digits = transform_signal_partly(last_digits)

    offset_part = "".join(str(i) for i in last_digits[-1:-9:-1])
    print(offset_part)
