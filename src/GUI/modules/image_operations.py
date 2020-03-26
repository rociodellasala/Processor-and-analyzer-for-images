import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from math import log10
from math import pow

MAX_PIXEL_VALUE = 255
MIN_PIXEL_VALUE = 0
L = 256


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
    img = Image.fromarray(lineally_adjust_image_values(added_image, width, height))
    img.show()
    #TODO save added_image
    return added_image


def subtract_grey_images(width, height, image_1, image_2):
    pixels_image_1 = image_1.load()
    pixels_image_2 = image_2.load()
    subtracted_image = np.zeros((width, height))
    for y in range(0, height):
        for x in range(0, width):
            subtracted_image[y, x] = int(pixels_image_1[x, y] - pixels_image_2[x, y])
    img = Image.fromarray(lineally_adjust_image_values(subtracted_image, width, height))
    img.show()
    #TODO save subtracted_image
    return subtracted_image


def subtract_colored_images(width, height, image_1, image_2):
    pixels_1 = image_1.load()
    pixels_2 = image_2.load()
    subtracted_image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            red_value_1 = int(pixels_1[x, y][0])
            red_value_2 = int(pixels_2[x, y][0])
            green_value_1 = int(pixels_1[x, y][1])
            green_value_2 = int(pixels_2[x, y][1])
            blue_value_1 = int(pixels_1[x, y][2])
            blue_value_2 = int(pixels_2[x, y][2])
            subtracted_image[y, x, 0] = np.uint8(red_value_1 - red_value_2)
            subtracted_image[y, x, 1] = np.uint8(green_value_1 - green_value_2)
            subtracted_image[y, x, 2] = np.uint8(blue_value_1 - blue_value_2)
    img = Image.fromarray(lineally_adjust_colored_image_values(subtracted_image, width, height), 'RGB')
    img.show()
    #TODO save subtracted_image


def multiply_grey_images_with_scalar(width, height, image_1, scalar):
    pixels_image_1 = image_1.load()
    multiplied_image = np.zeros((width, height))
    for y in range(0, height):
        for x in range(0, width):
            multiplied_image[y, x] = int(pixels_image_1[x, y] * scalar)
    img = Image.fromarray(lineally_adjust_image_values(multiplied_image, width, height))
    img.show()
    # TODO save multiplied image
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
    img = Image.fromarray(lineally_adjust_image_values(multiplied_image, width, height))
    img.show()
    # TODO save multiplied image
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
    if max_value == min_value:
        slope = 0
    else:
        slope = (MAX_PIXEL_VALUE - MIN_PIXEL_VALUE) / (max_value - min_value)
    if max_value == min_value:
        if max_value > MAX_PIXEL_VALUE:
            constant = MAX_PIXEL_VALUE
        elif min_value < MIN_PIXEL_VALUE:
            constant = MIN_PIXEL_VALUE
        else:
            constant = max_value
    else:
        constant = -slope * min_value
    adjusted_image = pixels
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            adjusted_image[x, y] = int(slope * current_value + constant)
    return adjusted_image


def lineally_adjust_colored_image_values(pixels, width, height):
    limits = get_colored_max_and_min_value(pixels, width, height)
    red_max_value = limits[0]
    red_min_value = limits[0]
    green_max_value = limits[0]
    green_min_value = limits[0]
    blue_max_value = limits[0]
    blue_min_value = limits[0]
    if red_max_value == red_min_value:
        red_slope = 0
    else:
        red_slope = (MAX_PIXEL_VALUE - MIN_PIXEL_VALUE) / (red_max_value - red_min_value)
    if green_max_value == green_min_value:
        green_slope = 0
    else:
        green_slope = (MAX_PIXEL_VALUE - MIN_PIXEL_VALUE) / (green_max_value - green_min_value)
    if blue_max_value == blue_min_value:
        blue_slope = 0
    else:
        blue_slope = (MAX_PIXEL_VALUE - MIN_PIXEL_VALUE) / (blue_max_value - blue_min_value)
    if red_max_value == red_min_value:
        if red_max_value > MAX_PIXEL_VALUE:
            red_constant = MAX_PIXEL_VALUE
        elif red_min_value < MIN_PIXEL_VALUE:
            red_constant = MIN_PIXEL_VALUE
        else:
            red_constant = red_max_value
    else:
        red_constant = -red_slope * red_min_value
    if green_max_value == green_min_value:
        if green_max_value > MAX_PIXEL_VALUE:
            green_constant = MAX_PIXEL_VALUE
        elif green_min_value < MIN_PIXEL_VALUE:
            green_constant = MIN_PIXEL_VALUE
        else:
            green_constant = green_max_value
    else:
        green_constant = -green_slope * green_min_value
    if blue_max_value == blue_min_value:
        if blue_max_value > MAX_PIXEL_VALUE:
            blue_constant = MAX_PIXEL_VALUE
        elif blue_min_value < MIN_PIXEL_VALUE:
            blue_constant = MIN_PIXEL_VALUE
        else:
            blue_constant = blue_max_value
    else:
        blue_constant = -blue_slope * blue_min_value
    adjusted_image = pixels
    for y in range(0, height):
        for x in range(0, width):
            current_red_value = int(pixels[x, y][0])
            current_green_value = int(pixels[x, y][1])
            current_blue_value = int(pixels[x, y][2])
            adjusted_image[x, y][0] = int(red_slope * current_red_value + red_constant)
            adjusted_image[x, y][1] = int(green_slope * current_green_value + green_constant)
            adjusted_image[x, y][0] = int(blue_slope * current_blue_value + blue_constant)
    return adjusted_image


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


def get_colored_max_and_min_value(pixels, width, height):
    red_max_value = None
    green_max_value = None
    blue_max_value = None
    red_min_value = None
    green_min_value = None
    blue_min_value = None
    for y in range(0, height):
        for x in range(0, width):
            current_red_value = int(pixels[x, y][0])
            current_green_value = int(pixels[x, y][1])
            current_blue_value = int(pixels[x, y][2])
            if red_max_value is None or red_max_value < current_red_value:
                red_max_value = current_red_value
            if red_min_value is None or red_min_value > current_red_value:
                red_min_value = current_red_value
            if green_max_value is None or green_max_value < current_green_value:
                green_max_value = current_green_value
            if green_min_value is None or green_min_value > current_green_value:
                green_min_value = current_green_value
            if blue_max_value is None or blue_max_value < current_blue_value:
                blue_max_value = current_blue_value
            if blue_min_value is None or blue_min_value > current_blue_value:
                blue_min_value = current_blue_value
    return [red_max_value, red_min_value, green_max_value, green_min_value, blue_max_value, blue_min_value]


def dynamic_range_compression(image, width, height):
    pixels = image.load()
    max_value = get_max_and_min_value(pixels, width, height)[0]
    c = (L - 1) / log10(1 + max_value)
    compressed_image = np.zeros((width, height))
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            compressed_image[y, x] = int(c * log10(1 + current_value))
    img = Image.fromarray(compressed_image)
    img.show()
    # TODO save compressed image


def gamma_pow_function(image, width, height, gamma):
    pixels = image.load()
    c = pow((L - 1), 1 - gamma)
    compressed_image = np.zeros((width, height))
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            compressed_image[y, x] = int(c * pow(current_value, gamma))
    img = Image.fromarray(lineally_adjust_image_values(compressed_image, width, height))
    img.show()
    # TODO save compressed image


def grey_image_negative(image, width, height):
    pixels = image.load()
    negative_image = np.zeros((height, width))
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            negative_image[y, x] = -current_value + L - 1
    img = Image.fromarray(negative_image)
    img.show()


def colored_image_negative(image, width, height):
    pixels = image.load()
    negative_image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            red_value = int(pixels[x, y][0])
            green_value = int(pixels[x, y][1])
            blue_value = int(pixels[x, y][2])
            negative_image[y, x, 0] = np.uint8(-red_value + L - 1)
            negative_image[y, x, 1] = np.uint8(-green_value + L - 1)
            negative_image[y, x, 2] = np.uint8(-blue_value + L - 1)
    img = Image.fromarray(negative_image, 'RGB')
    img.show()


def grey_level_histogram(image, width, height):
    grey_levels = calculate_histogram(image, width, height)
    plt.hist(grey_levels, bins=L, edgecolor='black')
    plt.title("Grey level histogram")
    plt.xlabel("Grey value")
    plt.ylabel("Quantity")
    plt.savefig(save_path + "grey_level_histogram.png")
    histogram_image = Image.open(save_path + "grey_level_histogram.png")
    histogram_image.show()


def calculate_histogram(image, width, height):
    pixels = image.load()
    grey_levels = np.zeros((height * width))
    i = 0
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            grey_levels[i] = current_value
            i += 1
    return grey_levels


def image_threshold(image, width, height, threshold):
    pixels = image.load()
    new_image = np.zeros((height, width))
    for y in range(0, height):
        for x in range(0, width):
            current_value = 0 if int(pixels[x, y]) <= threshold else MAX_PIXEL_VALUE
            new_image[y, x] = current_value
    img = Image.fromarray(new_image)
    img.show()


def image_equalization(image, width, height):
    pixels = image.load()
    grey_levels = np.zeros(L)
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            grey_levels[current_value] += 1
    total_pixels = width * height
    new_grey_levels = np.zeros(L)
    min_value = L
    for i in range(0, L):
        accumulated_value = 0
        for j in range(0, i + 1):
            accumulated_value += grey_levels[j]
        new_grey_levels[i] = accumulated_value / total_pixels
        if new_grey_levels[i] < min_value:
            min_value = new_grey_levels[i]
    for i in range(0, L):
        new_grey_levels[i] = int((L - 1) * (new_grey_levels[i] - min_value) / (1 - min_value) + 0.5)
    print(new_grey_levels)
    new_image = np.zeros((height, width))
    for y in range(0, height):
        for x in range(0, width):
            current_value = int(pixels[x, y])
            new_image[y, x] = new_grey_levels[current_value]
    img = Image.fromarray(new_image)
    img.show()
    grey_level_histogram(img, width, height)
    # TODO modularize function


save_path = "../../generated/"
