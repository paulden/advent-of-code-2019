import numpy as np
import matplotlib.pyplot as plt

TRANSPARENT_PIXEL_CODE = 2


def decode_image_data(image, width, height):
    layers = []
    layer_length_in_data = width * height
    number_of_layers = int(len(image) / layer_length_in_data)
    for layer_index in range(number_of_layers):
        start_pointer = layer_index * layer_length_in_data
        end_pointer = layer_index * layer_length_in_data + layer_length_in_data

        current_layer_data = [int(digit) for digit in (image[start_pointer:end_pointer])]
        current_layer_formatted = np.array(current_layer_data).reshape((height, width))

        layers.append(current_layer_formatted)
    return layers


def find_layer_with_fewest_zeros(image, width, height):
    layers = decode_image_data(image, width, height)
    layer_with_fewest_zeros = layers[0]
    for layer in layers:
        layer_number_of_zeros = np.count_nonzero(layer == 0)
        fewest_number_of_zeros = np.count_nonzero(layer_with_fewest_zeros == 0)
        if layer_number_of_zeros < fewest_number_of_zeros:
            layer_with_fewest_zeros = layer
    return layer_with_fewest_zeros


def compute_layer_checksum(layer):
    number_of_ones = np.count_nonzero(layer == 1)
    number_of_twos = np.count_nonzero(layer == 2)
    return number_of_ones * number_of_twos


def decode_image(image, width, height):
    layers = decode_image_data(image, width, height)
    flattened_layers = [layer.reshape(width * height) for layer in layers]
    final_image = []
    for pixel_index in range(width * height):
        layer_index = 0
        while flattened_layers[layer_index][pixel_index] == TRANSPARENT_PIXEL_CODE:
            layer_index += 1
        final_image.append(flattened_layers[layer_index][pixel_index])
    formatted_final_image = np.array(final_image).reshape((height, width))
    return formatted_final_image


if __name__ == '__main__':
    with open('./data/password_image.txt') as password_image:
        image_data = password_image.read()

        layer_with_fewest_zeros = find_layer_with_fewest_zeros(image_data, 25, 6)
        checksum = compute_layer_checksum(layer_with_fewest_zeros)
        final_image = decode_image(image_data, 25, 6)

        print('Part 1 - Verifying image was not corrupted: {}'.format(checksum))
        print('Part 2 - Printing image decoded using Matplotlib:')
        plt.imshow(final_image, cmap="gray")
        plt.show()
