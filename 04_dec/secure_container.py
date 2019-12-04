LOWER_BOUND_PASSWORD_RANGE = 357253
UPPER_BOUND_PASSWORD_RANGE = 892942

REQUIRED_NUMBER_OF_DIGITS = 6


def is_valid_password(password, condition_on_adjacent_digit):
    password_array = [int(digit) for digit in str(password)]
    if not LOWER_BOUND_PASSWORD_RANGE <= password <= UPPER_BOUND_PASSWORD_RANGE:
        return False
    if len(password_array) != REQUIRED_NUMBER_OF_DIGITS:
        return False

    previous_digit = password_array[0]
    number_of_adjacent_digits = [1] * 10

    for digit_index in range(1, len(password_array)):
        current_digit = password_array[digit_index]
        if previous_digit > current_digit:
            return False
        if previous_digit == current_digit:
            number_of_adjacent_digits[current_digit] += 1
        previous_digit = current_digit

    for number_of_adjacent_digit in number_of_adjacent_digits:
        if condition_on_adjacent_digit(number_of_adjacent_digit):
            return True

    return False


def more_than_two_adjacent_digits(number_of_digits):
    return number_of_digits >= 2


def exactly_two_adjacent_digits(number_of_digits):
    return number_of_digits == 2


if __name__ == '__main__':
    password_range = range(LOWER_BOUND_PASSWORD_RANGE, UPPER_BOUND_PASSWORD_RANGE + 1)
    valid_passwords = [password for password in password_range
                       if is_valid_password(password, more_than_two_adjacent_digits)]
    even_more_valid_passwords = [password for password in password_range
                                 if is_valid_password(password, exactly_two_adjacent_digits)]

    print('Part 1 - Number of valid passwords: {}'.format(len(valid_passwords)))
    print('Part 2 - Number of even more valid passwords: {}'.format(len(even_more_valid_passwords)))
