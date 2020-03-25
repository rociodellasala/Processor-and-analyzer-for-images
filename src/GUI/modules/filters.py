import numpy as np
import math
from PIL import Image
from image_operations import lineally_adjust_image_values


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
            new_image[y, x] = get_convolution(pixels, x, y, sliding_window, window_size)
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


def get_convolution(pixels, x, y, sliding_window, window_size):
    starting_row = y - window_size / 2
    starting_col = x - window_size / 2
    total = 0
    for row in range(0, window_size):
        for col in range(0, window_size):
            pixels_row = starting_row + row
            pixels_col = starting_col + col
            total += (pixels[pixels_col, pixels_row] * sliding_window[row, col])
    return total


def median_filter(image, image_height, image_width, window_size):
    new_image = np.zeros((image_height, image_width))
    pixels = image.load()
    window_y_center = int(window_size / 2)
    window_x_center = int(window_size / 2)
    middle = int(window_size / 2)
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            new_image[y, x] = get_median_window(pixels, x, y, window_size)[middle]
    image = Image.fromarray(new_image)
    image.show()
    return new_image


def get_median_window(pixels, x, y, windows_size):
    median_window = np.zeros(windows_size * windows_size)
    if windows_size % 2 == 0:
        windows_size += 1
    starting_col = int(x - windows_size / 2)
    starting_row = int(y - windows_size / 2)
    ending_col = int(x + windows_size / 2)
    ending_row = int(y + windows_size / 2)
    index = 0
    for i in range(starting_row, ending_row):
        for j in range(starting_col, ending_col):
            median_window[index] = pixels[j, i]
            index += 1
    median_window = np.sort(median_window)
    return median_window


def weighted_median_filter(image, image_height, image_width, window_size):
    new_image = np.zeros((image_height, image_width))
    pixels = image.load()
    window_y_center = 1
    window_x_center = 1
    sliding_window = get_weighted_median_window()
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            new_image[y, x] = get_weighted_median_value(pixels, x, y, window_size, sliding_window)
    image = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image.show()
    return new_image


def get_weighted_median_value(pixels, x, y, window_size, sliding_window):
    array_size = int(np.sum(sliding_window))
    new_array = np.zeros(array_size)
    starting_col = int(x - window_size / 2)
    starting_row = int(y - window_size / 2)
    ending_col = int(x + window_size / 2)
    ending_row = int(y + window_size / 2)
    first_middle = int(array_size / 2) - 1
    second_middle = first_middle + 1
    index = 0
    for i in range(starting_row, ending_row):
        for j in range(starting_col, ending_col):
            row = i - starting_row
            col = j - starting_col
            value = int(sliding_window[row, col])
            for k in range(0, value):
                new_array[index] = pixels[j, i]
                index += 1
    new_array = np.sort(new_array)
    return int((new_array[first_middle] + new_array[second_middle]) / 2)


def get_weighted_median_window():
    weighted_median_window = np.zeros([3, 3])
    weighted_median_window[0, 0] = 1
    weighted_median_window[0, 1] = 2
    weighted_median_window[0, 2] = 1
    weighted_median_window[1, 0] = 2
    weighted_median_window[1, 1] = 4
    weighted_median_window[1, 2] = 2
    weighted_median_window[2, 0] = 1
    weighted_median_window[2, 1] = 2
    weighted_median_window[2, 2] = 1
    return weighted_median_window


def gaussian_filter(image, image_height, image_width, sigma):
    new_image = np.zeros((image_height, image_width))
    window_size = 2 * sigma + 1
    pixels = image.load()
    window_y_center = int(window_size / 2)
    window_x_center = int(window_size / 2)
    sliding_window = get_gaussian_window(window_size, sigma)
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            new_image[y, x] = get_convolution(pixels, x, y, sliding_window, window_size)
    image = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image.show()
    return new_image


def get_gaussian_window(window_size, sigma):
    origin_x = int(window_size / 2)
    origin_y = int(window_size / 2)
    sliding_window = np.zeros([window_size, window_size])
    for y in range(0, window_size):
        for x in range(0, window_size):
            sliding_window[y, x] = get_gaussian_value(x - origin_x, y - origin_y, sigma)
    return sliding_window


def get_gaussian_value(x, y, sigma):
    exponent = -(np.power(x, 2) + np.power(y, 2)) / (np.power(sigma, 2))
    value = (1 / (2 * math.pi * np.power(sigma, 2))) * np.exp(exponent)
    return value


def border_enhancement_filter(image, image_height, image_width):
    new_image = np.zeros((image_height, image_width))
    window_size = 3
    pixels = image.load()
    window_y_center = 1
    window_x_center = 1
    sliding_window = get_border_enhancement_window()
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            new_image[y, x] = get_convolution(pixels, x, y, sliding_window, window_size)
    image = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image.show("Border enhancement", lineally_adjust_image_values(new_image, image_width, image_height))
    return new_image


def get_border_enhancement_window():
    sliding_window = np.zeros([3, 3])
    sliding_window[0, 0] = -1
    sliding_window[0, 1] = -1
    sliding_window[0, 2] = -1
    sliding_window[1, 0] = -1
    sliding_window[1, 1] = 8
    sliding_window[1, 2] = -1
    sliding_window[2, 0] = -1
    sliding_window[2, 1] = -1
    sliding_window[2, 2] = -1
    print(sliding_window)
    return sliding_window
