import numpy as np
from PIL import Image

MAX_PIXEL_VALUE = 255
MIN_PIXEL_VALUE = 0


def add_grey_images(image_1_width, image_1_height, image_1, image_2_width, image_2_height, image_2):
    width = int(image_1_width) if int(image_1_width) > int(image_2_width) else int(image_2_width)
    height = int(image_1_height) if int(image_1_height) > int(image_2_height) else int(image_2_height)
    pixels_image_1 = image_1.load()
    pixels_image_2 = image_2.load()
    added_image = np.zeros((width, height))
    for y in range(0, height):
        for x in range(0, width):
            pixel_image_1 = get_pixel_value(pixels_image_1, x, y, image_1_width, image_1_height)
            pixel_image_2 = get_pixel_value(pixels_image_2, x, y, image_2_width, image_2_height)
            added_image[y, x] = int(pixel_image_1 + pixel_image_2)
    img = Image.fromarray(added_image)
    img.show()
    return added_image


def subtract_grey_images(width, height, image_1, image_2):
    pixels_image_1 = image_1.load()
    pixels_image_2 = image_2.load()
    subtracted_image = np.zeros((width, height))
    for y in range(0, height):
        for x in range(0, width):
            subtracted_image[y, x] = int(pixels_image_1[x, y] - pixels_image_2[x, y])
    img = Image.fromarray(subtracted_image)
    img.show()
    return subtracted_image


def multiply_grey_images_with_scalar(width, height, image_1, scalar):
    pixels_image_1 = image_1.load()
    multiplied_image = np.zeros((width, height))
    for y in range(0, height):
        for x in range(0, width):
            multiplied_image[y, x] = int(pixels_image_1[x, y] * scalar)
    img = Image.fromarray(multiplied_image)
    img.show()
    return multiplied_image


def multiply_grey_images(image_1_width, image_1_height, image_1, image_2_width, image_2_height, image_2):
    width = int(image_1_width) if int(image_1_width) > int(image_2_width) else int(image_2_width)
    height = int(image_1_height) if int(image_1_height) > int(image_2_height) else int(image_2_height)
    pixels_image_1 = image_1.load()
    pixels_image_2 = image_2.load()
    multiplied_image = np.zeros((width, height))
    for y in range(0, height):
        for x in range(0, width):
            pixel_image_1 = get_pixel_value(pixels_image_1, x, y, image_1_width, image_1_height)
            pixel_image_2 = get_pixel_value(pixels_image_2, x, y, image_2_width, image_2_height)
            multiplied_image[y, x] = int(pixel_image_1 * pixel_image_2)
    img = Image.fromarray(multiplied_image)
    #img.show()
    lineally_adjust_image_values(multiplied_image, width, height)
    return multiplied_image


def get_pixel_value(pixels, x, y, width, height):
    if y > height or x > width:
        return 0
    else:
        return pixels[x, y]


def lineally_adjust_image_values(pixels, width, height):
    limits = get_max_and_min_value(pixels, width, height)
    max_value = limits[0]
    min_value = limits[1]
    print(max_value)
    print(min_value)
    if max_value == min_value:
        if max_value > MAX_PIXEL_VALUE:
            return MAX_PIXEL_VALUE
        elif min_value < MIN_PIXEL_VALUE:
            return MIN_PIXEL_VALUE
        return max_value
    slope = (MAX_PIXEL_VALUE - MIN_PIXEL_VALUE) / (max_value - min_value)
    constant = -slope * min_value
    adjusted_image = pixels
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            adjusted_image[x, y] = int(slope * current_value + constant)
    img = Image.fromarray(adjusted_image)
    img.show()


def get_max_and_min_value(pixels, width, height):
    max_value = None
    min_value = None
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            if max_value is None or max_value < current_value:
                max_value = current_value
            if min_value is None or min_value > current_value:
                min_value = current_value
    return [max_value, min_value]
