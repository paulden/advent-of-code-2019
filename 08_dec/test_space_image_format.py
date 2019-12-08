import numpy as np

from space_image_format import decode_image_data, find_layer_with_fewest_zeros, compute_layer_checksum, decode_image


def test_decode_image_data_should_return_list_with_single_matrix_when_image_has_one_layer():
    image_data = '12'
    width = 1
    height = 2

    decoded_image_data = decode_image_data(image_data, width, height)

    assert len(decoded_image_data) == 1
    np.testing.assert_array_equal(decoded_image_data[0], [[1], [2]])


def test_decode_image_data_should_return_two_matrices_when_image_has_two_layers():
    image_data = '1234'
    width = 1
    height = 2

    decoded_image = decode_image_data(image_data, width, height)

    assert len(decoded_image) == 2
    np.testing.assert_array_equal(decoded_image[0], [[1], [2]])
    np.testing.assert_array_equal(decoded_image[1], [[3], [4]])


def test_decode_image_data_should_return_two_matrices_with_appropriate_heights_and_widths_with_complex_data():
    image_data = '123456789012'
    width = 3
    height = 2

    decoded_image = decode_image_data(image_data, width, height)

    assert len(decoded_image) == 2
    np.testing.assert_array_equal(decoded_image[0], [[1, 2, 3], [4, 5, 6]])
    np.testing.assert_array_equal(decoded_image[1], [[7, 8, 9], [0, 1, 2]])


def test_find_layer_with_fewest_zeros_should_return_layer_with_fewest_zeros():
    image_data = '120411000006'
    width = 2
    height = 2

    layer_with_fewest_zeros = find_layer_with_fewest_zeros(image_data, width, height)
    np.testing.assert_array_equal(layer_with_fewest_zeros, [[1, 2], [0, 4]])


def test_compute_layer_checksum_should_return_layer_checksum():
    layer = np.array([[1, 2, 2], [1, 1, 1]])
    layer_checksum = compute_layer_checksum(layer)

    assert layer_checksum == 8


def test_decode_image_should_return_the_final_image():
    image_data = '0222112222120000'
    width = 2
    height = 2
    decoded_image = decode_image(image_data, width, height)

    np.testing.assert_array_equal(decoded_image, [[0, 1], [1, 0]])
