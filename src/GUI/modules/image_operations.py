import numpy as np
from PIL import Image


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
    img.show()
    return multiplied_image


def get_pixel_value(pixels, x, y, width, height):
    if y > height or x > width:
        return 0
    else:
        return pixels[x, y]