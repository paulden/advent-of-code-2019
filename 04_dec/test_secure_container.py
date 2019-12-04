from secure_container import is_valid_password, more_than_two_adjacent_digits, exactly_two_adjacent_digits


def test_is_valid_password_should_accept_valid_password():
    assert is_valid_password(357789, more_than_two_adjacent_digits) is True


def test_is_valid_password_should_reject_non_six_digit_password():
    assert is_valid_password(1234567, more_than_two_adjacent_digits) is False


def test_is_valid_password_should_reject_password_out_of_range():
    assert is_valid_password(111111, more_than_two_adjacent_digits) is False


def test_is_valid_password_should_reject_password_with_decreasing_digits():
    assert is_valid_password(357787, more_than_two_adjacent_digits) is False


def test_is_valid_password_should_reject_password_without_adjacent_digits():
    assert is_valid_password(456789, more_than_two_adjacent_digits) is False


def test_is_valid_password_should_reject_password_with_group_of_three_digits_when_validation_is_stronger():
    assert is_valid_password(357779, exactly_two_adjacent_digits) is False


def test_is_valid_password_should_accept_password_with_two_digits_but_other_large_group_when_validation_is_stronger():
    assert is_valid_password(777711, exactly_two_adjacent_digits) is False
