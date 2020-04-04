import numpy as np
from math import pow, sqrt
from PIL import Image
from filters import get_convolution
from image_operations import lineally_adjust_image_values, lineally_adjust_and_resize_colored_image_values


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
    # red_horizontal = horizontal_image[:, :, 0]
    # green_horizontal = horizontal_image[:, :, 1]
    # blue_horizontal = horizontal_image[:, :, 2]
    # Image.fromarray(lineally_adjust_image_values(red_horizontal, image_width, image_height)).show()
    # Image.fromarray(lineally_adjust_image_values(green_horizontal, image_width, image_height)).show()
    # Image.fromarray(lineally_adjust_image_values(blue_horizontal, image_width, image_height)).show()
    # Image.fromarray(lineally_adjust_and_resize_colored_image_values(horizontal_image, image_width, image_height), "RGB").show()


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


def sobel_detection(image, image_height, image_width):
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
    save_image(horizontal_image, save_path + "sobel_horizontal_image.ppm")
    save_image(vertical_image, save_path + "sobel_vertical_image.ppm")
    save_image(new_image, save_path + "sobel_generated_image.ppm")
    image_one = Image.fromarray(lineally_adjust_image_values(horizontal_image, image_width, image_height))
    image_two = Image.fromarray(lineally_adjust_image_values(vertical_image, image_width, image_height))
    image_three = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
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
    print(matrix)
    return matrix


def get_sobel_vertical_matrix():
    matrix = np.zeros((3, 3))
    matrix[0, 0] = -1
    matrix[0, 1] = -2
    matrix[0, 2] = -1
    matrix[2, 0] = 1
    matrix[2, 1] = 2
    matrix[2, 2] = 1
    print(matrix)
    return matrix


def save_image(image, file_path):
    img = Image.fromarray(image)
    img = img.convert("I")
    img.save(file_path)


def save_colored_image(image, file_path):
    img = Image.fromarray(image, "RGB")
    img = img.convert("RGB")
    img.save(file_path)


save_path = "../../generated/"
