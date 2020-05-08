import numpy as np
from math import pow, sqrt, fabs, exp, pi
from PIL import Image
from filters import get_convolution, bilateral_filter
from image_operations import lineally_adjust_image_values, lineally_adjust_and_resize_colored_image_values
from matrix_operations import rotate_matrix_with_angle
from threshold_calculator import global_threshold
from src.GUI import gui_constants as constants


def prewit_detection(image, image_height, image_width):
    pixels = np.array(image)
    horizontal_matrix = get_prewit_horizontal_matrix()
    horizontal_image = np.zeros((image_height, image_width))
    vertical_matrix = get_prewit_vertical_matrix()
    vertical_image = np.zeros((image_height, image_width))
    new_image = np.zeros((image_height, image_width))
    window_y_center = 1
    window_x_center = 1
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            horizontal_image[y, x] = get_convolution(pixels, x, y, horizontal_matrix, 3)
            vertical_image[y, x] = get_convolution(pixels, x, y, vertical_matrix, 3)
            new_image[y, x] = sqrt(pow(horizontal_image[y, x], 2) + pow(vertical_image[y, x], 2))
    save_image(horizontal_image, save_path + "prewit_horizontal_image.ppm")
    save_image(vertical_image, save_path + "prewit_vertical_image.ppm")
    save_image(new_image, save_path + "prewit_generated_image.ppm")
    image_one = Image.fromarray(lineally_adjust_image_values(horizontal_image, image_width, image_height))
    image_two = Image.fromarray(lineally_adjust_image_values(vertical_image, image_width, image_height))
    image_three = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image_one.show()
    image_two.show()
    image_three.show()


def prewit_color_detection(image, image_height, image_width):
    pixels = np.array(image)
    pixels_red = pixels[:, :, 0];
    pixels_green = pixels[:, :, 1];
    pixels_blue = pixels[:, :, 2];
    horizontal_matrix = get_prewit_horizontal_matrix()
    horizontal_image = np.zeros((image_height, image_width, 3))
    vertical_matrix = get_prewit_vertical_matrix()
    vertical_image = np.zeros((image_height, image_width, 3))
    new_image = np.zeros((image_height, image_width, 3))
    window_y_center = 1
    window_x_center = 1
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            horizontal_image[y, x, 0] = get_convolution(pixels_red, x, y, horizontal_matrix, 3)
            horizontal_image[y, x, 1] = get_convolution(pixels_green, x, y, horizontal_matrix, 3)
            horizontal_image[y, x, 2] = get_convolution(pixels_blue, x, y, horizontal_matrix, 3)
            vertical_image[y, x, 0] = get_convolution(pixels_red, x, y, vertical_matrix, 3)
            vertical_image[y, x, 1] = get_convolution(pixels_green, x, y, vertical_matrix, 3)
            vertical_image[y, x, 2] = get_convolution(pixels_blue, x, y, vertical_matrix, 3)
            new_image[y, x, 0] = sqrt(pow(horizontal_image[y, x, 0], 2) + pow(vertical_image[y, x, 0], 2))
            new_image[y, x, 1] = sqrt(pow(horizontal_image[y, x, 1], 2) + pow(vertical_image[y, x, 1], 2))
            new_image[y, x, 2] = sqrt(pow(horizontal_image[y, x, 2], 2) + pow(vertical_image[y, x, 2], 2))

    save_colored_image(lineally_adjust_and_resize_colored_image_values(horizontal_image, image_width, image_height),
                       save_path + "prewit_colored_horizontal_image.ppm")
    save_colored_image(lineally_adjust_and_resize_colored_image_values(vertical_image, image_width, image_height),
                        save_path + "prewit_colored_vertical_image.ppm")
    save_colored_image(lineally_adjust_and_resize_colored_image_values(new_image, image_width, image_height),
                        save_path + "prewit_colored_generated_image.ppm")
    image_one = Image.fromarray(lineally_adjust_and_resize_colored_image_values(horizontal_image, image_width, image_height), "RGB")
    image_two = Image.fromarray(lineally_adjust_and_resize_colored_image_values(vertical_image, image_width, image_height), "RGB")
    image_three = Image.fromarray(lineally_adjust_and_resize_colored_image_values(new_image, image_width, image_height), "RGB")
    image_one.show()
    image_two.show()
    image_three.show()


def get_prewit_horizontal_matrix():
    matrix = np.zeros((3, 3))
    matrix[0, 0] = -1
    matrix[1, 0] = -1
    matrix[2, 0] = -1
    matrix[0, 2] = 1
    matrix[1, 2] = 1
    matrix[2, 2] = 1
    return matrix


def get_prewit_vertical_matrix():
    matrix = np.zeros((3, 3))
    matrix[0, 0] = -1
    matrix[0, 1] = -1
    matrix[0, 2] = -1
    matrix[2, 0] = 1
    matrix[2, 1] = 1
    matrix[2, 2] = 1
    return matrix


def sobel_detection(image, image_height, image_width, show_images=True):
    pixels = np.array(image)
    horizontal_matrix = get_sobel_horizontal_matrix()
    horizontal_image = np.zeros((image_height, image_width))
    vertical_matrix = get_sobel_vertical_matrix()
    vertical_image = np.zeros((image_height, image_width))
    new_image = np.zeros((image_height, image_width))
    window_y_center = 1
    window_x_center = 1
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            horizontal_image[y, x] = get_convolution(pixels, x, y, horizontal_matrix, 3)
            vertical_image[y, x] = get_convolution(pixels, x, y, vertical_matrix, 3)
            new_image[y, x] = sqrt(pow(horizontal_image[y, x], 2) + pow(vertical_image[y, x], 2))
    if show_images:
        save_image(horizontal_image, save_path + "sobel_horizontal_image.ppm")
        save_image(vertical_image, save_path + "sobel_vertical_image.ppm")
        save_image(new_image, save_path + "sobel_generated_image.ppm")
        image_one = Image.fromarray(lineally_adjust_image_values(horizontal_image, image_width, image_height))
        image_two = Image.fromarray(lineally_adjust_image_values(vertical_image, image_width, image_height))
        image_three = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
        image_one.show()
        image_two.show()
        image_three.show()
    return [horizontal_image, vertical_image, new_image]



def sobel_color_detection(image, image_height, image_width):
    pixels = np.array(image)
    pixels_red = pixels[:, :, 0];
    pixels_green = pixels[:, :, 1];
    pixels_blue = pixels[:, :, 2];
    horizontal_matrix = get_sobel_horizontal_matrix()
    horizontal_image = np.zeros((image_height, image_width, 3))
    vertical_matrix = get_sobel_vertical_matrix()
    vertical_image = np.zeros((image_height, image_width, 3))
    new_image = np.zeros((image_height, image_width, 3))
    window_y_center = 1
    window_x_center = 1
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            horizontal_image[y, x, 0] = get_convolution(pixels_red, x, y, horizontal_matrix, 3)
            horizontal_image[y, x, 1] = get_convolution(pixels_green, x, y, horizontal_matrix, 3)
            horizontal_image[y, x, 2] = get_convolution(pixels_blue, x, y, horizontal_matrix, 3)
            vertical_image[y, x, 0] = get_convolution(pixels_red, x, y, vertical_matrix, 3)
            vertical_image[y, x, 1] = get_convolution(pixels_green, x, y, vertical_matrix, 3)
            vertical_image[y, x, 2] = get_convolution(pixels_blue, x, y, vertical_matrix, 3)
            new_image[y, x, 0] = sqrt(pow(horizontal_image[y, x, 0], 2) + pow(vertical_image[y, x, 0], 2))
            new_image[y, x, 1] = sqrt(pow(horizontal_image[y, x, 1], 2) + pow(vertical_image[y, x, 1], 2))
            new_image[y, x, 2] = sqrt(pow(horizontal_image[y, x, 2], 2) + pow(vertical_image[y, x, 2], 2))

    save_colored_image(lineally_adjust_and_resize_colored_image_values(horizontal_image, image_width, image_height),
                       save_path + "sobel_colored_horizontal_image.ppm")
    save_colored_image(lineally_adjust_and_resize_colored_image_values(vertical_image, image_width, image_height),
                        save_path + "sobel_colored_vertical_image.ppm")
    save_colored_image(lineally_adjust_and_resize_colored_image_values(new_image, image_width, image_height),
                        save_path + "prewit_colored_generated_image.ppm")
    image_one = Image.fromarray(lineally_adjust_and_resize_colored_image_values(horizontal_image, image_width, image_height), "RGB")
    image_two = Image.fromarray(lineally_adjust_and_resize_colored_image_values(vertical_image, image_width, image_height), "RGB")
    image_three = Image.fromarray(lineally_adjust_and_resize_colored_image_values(new_image, image_width, image_height), "RGB")
    image_one.show()
    image_two.show()
    image_three.show()


def get_sobel_horizontal_matrix():
    matrix = np.zeros((3, 3))
    matrix[0, 0] = -1
    matrix[1, 0] = -2
    matrix[2, 0] = -1
    matrix[0, 2] = 1
    matrix[1, 2] = 2
    matrix[2, 2] = 1
    return matrix


def get_sobel_vertical_matrix():
    matrix = np.zeros((3, 3))
    matrix[0, 0] = -1
    matrix[0, 1] = -2
    matrix[0, 2] = -1
    matrix[2, 0] = 1
    matrix[2, 1] = 2
    matrix[2, 2] = 1
    return matrix


def four_direction_border_detection(image, image_height, image_width, famous_matrix=1):
    pixels = np.array(image)
    horizontal_matrix = get_famous_horizontal_matrix(famous_matrix)
    first_diagonal_matrix = rotate_matrix_with_angle(horizontal_matrix, 3, 45)
    vertical_matrix = rotate_matrix_with_angle(first_diagonal_matrix, 3, 45)
    second_diagonal_matrix = rotate_matrix_with_angle(vertical_matrix, 3, 45)
    horizontal_image = np.zeros((image_height, image_width))
    first_diagonal_image = np.zeros((image_height, image_width))
    vertical_image = np.zeros((image_height, image_width))
    second_diagonal_image = np.zeros((image_height, image_width))
    new_image = np.zeros((image_height, image_width))
    window_y_center = 1
    window_x_center = 1
    current_values = np.zeros(4)
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            horizontal_image[y, x] = get_convolution(pixels, x, y, horizontal_matrix, 3)
            first_diagonal_image[y, x] = get_convolution(pixels, x, y, first_diagonal_matrix, 3)
            vertical_image[y, x] = get_convolution(pixels, x, y, vertical_matrix, 3)
            second_diagonal_image[y, x] = get_convolution(pixels, x, y, second_diagonal_matrix, 3)
            current_values[0] = horizontal_image[y, x]
            current_values[1] = first_diagonal_image[y, x]
            current_values[2] = vertical_image[y, x]
            current_values[3] = second_diagonal_image[y, x]
            new_image[y, x] = np.max(current_values)
    save_image(horizontal_image, save_path + "horizontal_image.ppm")
    save_image(first_diagonal_image, save_path + "first_diagonal_image.ppm")
    save_image(vertical_image, save_path + "vertical_image.ppm")
    save_image(second_diagonal_image, save_path + "second_diagonal_image.ppm")
    save_image(new_image, save_path + "four_directions_generated_image.ppm")
    image_one = Image.fromarray(lineally_adjust_image_values(horizontal_image, image_width, image_height))
    image_two = Image.fromarray(lineally_adjust_image_values(first_diagonal_image, image_width, image_height))
    image_three = Image.fromarray(lineally_adjust_image_values(vertical_image, image_width, image_height))
    image_four = Image.fromarray(lineally_adjust_image_values(second_diagonal_image, image_width, image_height))
    image_five = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image_one.show()
    image_two.show()
    image_three.show()
    image_four.show()
    image_five.show()


def get_famous_horizontal_matrix(famous_matrix):
    if famous_matrix == 1:
        return get_sobel_horizontal_matrix()
    elif famous_matrix == 2:
        return get_prewit_horizontal_matrix()
    else:
        return get_kirsh_horizontal_matrix()


def get_kirsh_horizontal_matrix():
    matrix = np.zeros((3, 3))
    matrix[0, 0] = -3
    matrix[1, 0] = -3
    matrix[2, 0] = -3
    matrix[0, 1] = -3
    matrix[1, 1] = 0
    matrix[2, 1] = -3
    matrix[0, 2] = 5
    matrix[1, 2] = 5
    matrix[2, 2] = 5
    return matrix


def laplacian_method(image, image_height, image_width, sinthesis_method):
    pixels = np.array(image)
    matrix = get_laplacian_matrix()
    new_image = np.zeros((image_height, image_width))
    window_y_center = 1
    window_x_center = 1
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            new_image[y, x] = get_convolution(pixels, x, y, matrix, 3)
    horizontal_image = horizontal_zero_crossing(new_image, image_height, image_width)
    vertical_image = vertical_zero_crossing(new_image, image_height, image_width)
    if sinthesis_method == "and":
        new_image = and_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    elif sinthesis_method == "or":
        new_image = or_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    else:
        new_image = module_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    save_image(new_image, save_path + "laplacian_generated_image.ppm")
    image = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image.show()


def laplacian_method_with_slope_evaluation(image, image_height, image_width, threshold, sinthesis_method):
    pixels = np.array(image)
    matrix = get_laplacian_matrix()
    new_image = np.zeros((image_height, image_width))
    window_y_center = 1
    window_x_center = 1
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            new_image[y, x] = get_convolution(pixels, x, y, matrix, 3)
    horizontal_image = horizontal_zero_crossing_with_slope(new_image, image_height, image_width, threshold)
    vertical_image = vertical_zero_crossing_with_slope(new_image, image_height, image_width, threshold)
    if sinthesis_method == "and":
        new_image = and_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    elif sinthesis_method == "or":
        new_image = or_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    else:
        new_image = module_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    save_image(new_image, save_path + "laplacian_generated_with_slope_image.ppm")
    image = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image.show()


def get_laplacian_matrix():
    matrix = np.zeros((3, 3))
    matrix[0, 0] = 0
    matrix[0, 1] = -1
    matrix[0, 2] = 0
    matrix[1, 0] = -1
    matrix[1, 1] = 4
    matrix[1, 2] = -1
    matrix[2, 0] = 0
    matrix[2, 1] = -1
    matrix[2, 2] = 0
    return matrix


def laplacian_gaussian_method(image, image_height, image_width, sigma, threshold, sinthesis_method):
    n = int(6 * sigma + 1)
    pixels = np.array(image)
    matrix = get_laplacian_gaussian_matrix(n, sigma)
    new_image = np.zeros((image_height, image_width))
    window_y_center = int(n / 2)
    window_x_center = int(n / 2)
    for y in range(window_y_center, image_height - window_y_center):
        for x in range(window_x_center, image_width - window_x_center):
            new_image[y, x] = get_convolution(pixels, x, y, matrix, n)
    horizontal_image = horizontal_zero_crossing_with_slope(new_image, image_height, image_width, threshold)
    vertical_image = vertical_zero_crossing_with_slope(new_image, image_height, image_width, threshold)
    if sinthesis_method == "and":
        new_image = and_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    elif sinthesis_method == "or":
        new_image = or_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    else:
        new_image = module_sinthesis(horizontal_image, vertical_image, image_height, image_width)
    save_image(new_image, save_path + "laplacian_gaussian_generated_with_slope_image.ppm")
    image = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image.show()


def get_laplacian_gaussian_matrix(size, sigma):
    matrix = np.zeros((size, size))
    x_center = int(size / 2)
    y_center = int(size / 2)
    for y in range(0, size):
        for x in range(0, size):
            matrix[y, x] = gausian_laplacian_function(x - x_center, y - y_center, sigma)
    return matrix


def gausian_laplacian_function(x, y, sigma):
    sigma_squared = sigma * sigma
    sigma_to_the_third = sigma_squared * sigma
    factor = - 1 / (sqrt(2 * pi) * sigma_to_the_third)
    expression = (x * x + y * y) / sigma_squared
    return factor * (2 - expression) * exp(-expression / 2)


def get_angle_matrix(horizontal_image, vertical_image, image_height, image_width):
    angle_matrix = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width):
            if horizontal_image[y, x] == 0:
                angle_matrix[y, x] = 90
            else:
                vertical_value = vertical_image[y, x]
                horizontal_value = horizontal_image[y, x]
                angle = np.arctan(vertical_value / horizontal_value)
                angle = angle * 180 / np.pi
                if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                    angle = 0
                elif 22.5 <= angle < 67.5:
                    angle = 45
                elif 67.5 <= angle < 112.5:
                    angle = 90
                else:
                    angle = 135
                angle_matrix[y, x] = angle
    return angle_matrix


def get_x_increment(angle):
    if angle == 0 or angle == 45:
        return 1
    elif angle == 135:
        return -1
    else:
        return 0


def get_y_increment(angle):
    if angle == 90 or angle == 45 or angle == 135:
        return -1
    else:
        return 0


def suppress_false_maximums(synthesized_image, angle_matrix, image_height, image_width):
    new_image = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width):
            x_increment = get_x_increment(angle_matrix[y, x])
            y_increment = get_y_increment(angle_matrix[y, x])
            before_x = x - x_increment
            before_y = y - y_increment
            after_x = x + x_increment
            after_y = y + y_increment
            if (0 <= before_x < image_width and 0 <= before_y < image_height) and \
                    (synthesized_image[before_y, before_x] > synthesized_image[y, x]):
                new_image[y, x] = 0
            elif (0 <= after_x < image_width and 0 <= after_y < image_height) and \
                    (synthesized_image[after_y, after_x] > synthesized_image[y, x]):
                new_image[y, x] = 0
            else:
                new_image[y, x] = constants.MAX_COLOR_VALUE
    return new_image


def has_border_neighbours(suppressed_image, high_threshold, new_image, image_height, image_width, x, y,
                          four_neighbours):
    if four_neighbours:
        increments = [[0, -1], [1, 0], [0, 1], [-1, 0]]
    else:
        increments = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
    for i in range(0, len(increments)):
        new_x = x + increments[i][1]
        new_y = y + increments[i][0]
        if 0 <= new_x < image_width and 0 <= new_y < image_height:
            if suppressed_image[new_y, new_x] > high_threshold or new_image[new_y, new_x] == constants.MAX_COLOR_VALUE:
                return True
    return False


def canny_method(image, image_height, image_width, sigma_s, sigma_r, window_size, four_neighbours=True):
    filtered_image = bilateral_filter(image, image_height, image_width, sigma_s, sigma_r, window_size, False)
    images = sobel_detection(filtered_image, image_height, image_width, False)
    horizontal_image = images[0]
    vertical_image = images[1]
    synthesized_image = images[2]
    angle_matrix = get_angle_matrix(horizontal_image, vertical_image, image_height, image_width)
    suppressed_image = suppress_false_maximums(synthesized_image, angle_matrix, image_height, image_width)
    min_pixel_value = int(np.min(suppressed_image))
    max_pixel_value = int(np.max(suppressed_image))
    deviation = int(np.std(suppressed_image))
    threshold = global_threshold(suppressed_image, image_height, image_width, False, False)
    low_threshold = max(min_pixel_value, threshold - deviation)
    high_threshold = min(threshold + deviation, max_pixel_value)
    new_image = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width):
            current_value = suppressed_image[y, x]
            if current_value <= low_threshold:
                new_image[y, x] = 0
            elif current_value > high_threshold:
                new_image[y, x] = constants.MAX_COLOR_VALUE
            elif has_border_neighbours(suppressed_image, high_threshold, new_image, image_height,
                                       image_width, x, y, four_neighbours):
                new_image[y, x] = constants.MAX_COLOR_VALUE
            else:
                new_image[y, x] = 0
    save_image(new_image, save_path + "canny_generated_image.ppm")
    image = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    image.show()
    return new_image


def horizontal_zero_crossing(image, image_height, image_width):
    horizontal_image = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width - 1):
            value = image[y, x] * image[y, x + 1]
            if value < 0:
                horizontal_image[y, x] = constants.MAX_COLOR_VALUE
            elif value == 0 and image[y, x] != 0:
                if x + 2 < image_width:
                    value = image[y, x + 2] * image[y, x]
                    if value < 0:
                        horizontal_image[y, x] = constants.MAX_COLOR_VALUE
                    else:
                        horizontal_image[y, x] = 0
            else:
                horizontal_image[y, x] = 0
    return horizontal_image


def vertical_zero_crossing(image, image_height, image_width):
    vertical_image = np.zeros((image_height, image_width))
    for y in range(0, image_height - 1):
        for x in range(0, image_width):
            value = image[y, x] * image[y + 1, x]
            if value < 0:
                vertical_image[y, x] = constants.MAX_COLOR_VALUE
            elif value == 0 and image[y, x] != 0:
                if y + 2 < image_height:
                    value = image[y + 2, x] * image[y, x]
                    if value < 0:
                        vertical_image[y, x] = constants.MAX_COLOR_VALUE
                    else:
                        vertical_image[y, x] = 0
            else:
                vertical_image[y, x] = 0
    return vertical_image


def horizontal_zero_crossing_with_slope(image, image_height, image_width, threshold):
    horizontal_image = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width - 1):
            value = image[y, x] * image[y, x + 1]
            if value < 0:
                total = int(fabs(image[y, x]) + fabs(image[y, x + 1]))
                horizontal_image[y, x] = constants.MAX_COLOR_VALUE if total >= threshold else 0
            elif value == 0 and image[y, x] != 0:
                if x + 2 < image_width:
                    value = image[y, x + 2] * image[y, x]
                    if value < 0:
                        total = int(fabs(image[y, x]) + fabs(image[y, x + 2]))
                        horizontal_image[y, x] = constants.MAX_COLOR_VALUE if total >= threshold else 0
                    else:
                        horizontal_image[y, x] = 0
            else:
                horizontal_image[y, x] = 0
    return horizontal_image


def vertical_zero_crossing_with_slope(image, image_height, image_width, threshold):
    vertical_image = np.zeros((image_height, image_width))
    for y in range(0, image_height - 1):
        for x in range(0, image_width):
            value = image[y, x] * image[y + 1, x]
            if value < 0:
                total = int(fabs(image[y, x]) + fabs(image[y + 1, x]))
                vertical_image[y, x] = constants.MAX_COLOR_VALUE if total >= threshold else 0
            elif value == 0 and image[y, x] != 0:
                if y + 2 < image_height:
                    value = image[y + 2, x] * image[y, x]
                    if value < 0:
                        total = int(fabs(image[y, x]) + fabs(image[y + 2, x]))
                        vertical_image[y, x] = constants.MAX_COLOR_VALUE if total >= threshold else 0
                    else:
                        vertical_image[y, x] = 0
            else:
                vertical_image[y, x] = 0
    return vertical_image


def and_sinthesis(horizontal_image, vertical_image, image_height, image_width):
    new_image = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width):
            if horizontal_image[y, x] > 0 and vertical_image[y, x] > 0:
                new_image[y, x] = constants.MAX_COLOR_VALUE
            else:
                new_image[y, x] = 0
    return new_image


def or_sinthesis(horizontal_image, vertical_image, image_height, image_width):
    new_image = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width):
            if horizontal_image[y, x] > 0 or vertical_image[y, x] > 0:
                new_image[y, x] = constants.MAX_COLOR_VALUE
            else:
                new_image[y, x] = 0
    return new_image


def module_sinthesis(horizontal_image, vertical_image, image_height, image_width):
    new_image = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width):
            new_image[y, x] = int(sqrt(pow(horizontal_image[y, x], 2) + pow(vertical_image[y, x], 2)))
    return new_image


def save_image(image, file_path):
    img = Image.fromarray(image)
    img = img.convert("I")
    img.save(file_path)


def save_colored_image(image, file_path):
    img = Image.fromarray(image, "RGB")
    img = img.convert("RGB")
    img.save(file_path)


save_path = "../../generated/"
