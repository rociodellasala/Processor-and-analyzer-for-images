import numpy as np
from PIL import Image


def media_filter(image, image_height, image_width, window_size):
    if window_size % 2 == 0:
        window_size = window_size + 1
    new_image = np.zeros((image_height, image_width))
    pixels = image.load()
    sliding_window = generate_media_window(window_size)
    window_y_center = int(window_size / 2)
    window_x_center = int(window_size / 2)
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            new_image[y, x] = get_media_value(pixels, x, y, sliding_window, window_size)
    image = Image.fromarray(new_image)
    image.show()
    return new_image


def generate_media_window(window_size):
    sliding_window = np.ones((window_size, window_size))
    dimension = window_size * window_size
    for y in range(0, window_size):
        for x in range(0, window_size):
            sliding_window[y, x] = 1 / dimension
    return sliding_window


def get_media_value(pixels, x, y, sliding_window, window_size):
    starting_row = y - window_size / 2
    starting_col = x - window_size / 2
    total = 0
    for row in range(0, window_size):
        for col in range(0, window_size):
            pixels_row = starting_row + row
            pixels_col = starting_col + col
            total += (pixels[pixels_col, pixels_row] * sliding_window[row, col])
    return total
