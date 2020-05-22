import numpy as np
from math import pow, sqrt, fabs, exp, pi
from PIL import Image
from filters import get_convolution, bilateral_filter
from image_operations import lineally_adjust_image_values, lineally_adjust_and_resize_colored_image_values, \
    lineally_adjust_colored_image_values
from matrix_operations import rotate_matrix_with_angle
from threshold_calculator import global_threshold
from src.GUI import gui_constants as constants
from border_detectors import canny_method


def hough_transform(image, image_height, image_width, threshold, epsilon):
    image = canny_method(image, image_height, image_width, 10, 10, 3, show_image=False)
    max_size = max(image_height, image_width)
    max_rho = np.sqrt(2) * max_size
    min_rho = - np.sqrt(2) * max_size
    delta_rho = max_size * 0.1
    rows = int((max_rho - min_rho) / delta_rho)
    delta_theta = (15 / 180) * np.pi
    cols = int(((np.pi / 2) - (- np.pi / 2)) / delta_theta)
    accumulator = np.zeros((rows, cols))
    for y in range(0, image_height):
        for x in range(0, image_width):
            if image[y, x] == constants.MAX_COLOR_VALUE:
                for rho in range(0, rows):
                    for theta in range(0, cols):
                        current_rho = min_rho + rho * delta_rho
                        current_theta = (-np.pi / 2) + (theta * delta_theta)
                        value = abs(current_rho - x * np.cos(current_theta) - y * np.sin(current_theta))
                        if value <= epsilon:
                            accumulator[rho, theta] += 1

    arr = np.zeros((8, 2))
    index = 0
    for rho in range(0, rows):
        for theta in range(0, cols):
            if accumulator[rho, theta] >= threshold:
                current_rho = min_rho + rho * delta_rho
                current_theta = (-np.pi / 2) + (theta * delta_theta)
                draw_lines(current_rho, current_theta, image, image_height, image_width)
                arr[index, 0] = current_rho
                arr[index, 1] = current_theta
                index += 1

    save_image(image, save_path + "hough_transform.ppm")
    image = Image.fromarray(lineally_adjust_image_values(image, image_width, image_height))
    image.show()


def draw_lines(rho, theta, image, image_height, image_width):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    slope = (y2 - y1) / (x2 - x1)
    origin_ordenate = y0 - slope * x0
    for x in range(0, image_width):
        y = int(slope * x + origin_ordenate)
        # y = int(- ((np.cos(theta) / np.sin(theta)) * x) + rho / np.sin(theta))
        if 0 <= y < image_height:
            image[y, x] = constants.MAX_COLOR_VALUE
    print("aca")


def pixel_exchange(image, image_height, image_width, top_left_vertex_x, top_left_vertex_y, bottom_right_vertex_x,
                   bottom_right_vertex_y, epsilon, max_iterations):
    pixels = np.array(image)
    new_image = np.ones((image_height, image_width)) * 3
    lin = []
    lout = []
    object_color = get_object_color(new_image, pixels, top_left_vertex_x, top_left_vertex_y, bottom_right_vertex_x,
                                    bottom_right_vertex_y, lin, lout)
    for i in range(0, max_iterations):
        new_lin = []
        new_lout = []
        iterate_over_lout(pixels, image_height, image_width, new_image, object_color, epsilon, lout, new_lout, new_lin)
        iterate_over_lin(image_height, image_width, new_image, lin, new_lin)
        lin = new_lin
        lout = new_lout
    border_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    for y in range(0, image_height):
        for x in range(0, image_width):
            border_image[y, x, 0] = np.uint8(pixels[y, x])
            if new_image[y, x] == -1 or new_image[y, x] == 1:
                border_image[y, x, 2] = np.uint8(255)
    save_colored_image(border_image, save_path + "pixel_exchange_image.ppm")
    img = Image.fromarray(border_image, 'RGB')
    img.show()


def iterate_over_lout(image, image_height, image_width, new_image, object_color, epsilon, lout, new_lout, new_lin):
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    for pixel in lout:
        current_x = pixel[0]
        current_y = pixel[1]
        if abs(image[current_y, current_x] - object_color) <= epsilon:
            new_image[current_y, current_x] = -1
            new_lin.append((current_x, current_y))
            for i in range(0, 4):
                x_increment = directions[i][0]
                y_increment = directions[i][1]
                if (0 <= x_increment + current_x < image_width and 0 <= y_increment + current_y < image_height and
                        new_image[current_y + y_increment, current_x + x_increment] == 3):
                    new_image[current_y + y_increment, current_x + x_increment] = 1
                    new_lout.append((current_x + x_increment, current_y + y_increment))
        else:
            new_lout.append((current_x, current_y))


def iterate_over_lin(image_height, image_width, new_image, lin, new_lin):
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    for pixel in lin:
        blue_count = 0
        current_x = pixel[0]
        current_y = pixel[1]
        for i in range(0, 4):
            x_increment = directions[i][0]
            y_increment = directions[i][1]
            new_x = current_x + x_increment
            new_y = current_y + y_increment
            if 0 <= new_x < image_width and 0 <= new_y <= image_height and new_image[new_y, new_x] == 1:
                blue_count += 1
        if blue_count == 0:
            new_image[new_y, new_x] = -3
        else:
            new_lin.append((current_x, current_y))


def get_object_color(new_image, pixels, top_left_vertex_x, top_left_vertex_y, bottom_right_vertex_x,
                     bottom_right_vertex_y, lin, lout):
    color_sum = 0
    square_height = (bottom_right_vertex_y - top_left_vertex_y) + 1
    square_width = (bottom_right_vertex_x - top_left_vertex_x) + 1
    square_size = square_height * square_width
    for y in range(top_left_vertex_y, bottom_right_vertex_y + 1):
        for x in range(top_left_vertex_x, bottom_right_vertex_x + 1):
            new_image[y, x] = -3
            color_sum += pixels[y, x]

    for y in range(top_left_vertex_y, bottom_right_vertex_y + 1):
        new_image[y, top_left_vertex_x - 1] = -1
        lin.append((top_left_vertex_x - 1, y))
        new_image[y, bottom_right_vertex_x + 1] = -1
        lin.append((bottom_right_vertex_x + 1, y))
        new_image[y, top_left_vertex_x - 2] = 1
        lout.append((top_left_vertex_x - 2, y))
        new_image[y, bottom_right_vertex_x + 2] = 1
        lout.append((bottom_right_vertex_x + 2, y))

    for x in range(top_left_vertex_x, bottom_right_vertex_x + 1):
        new_image[top_left_vertex_y - 1, x] = -1
        lin.append((x, top_left_vertex_y - 1))
        new_image[bottom_right_vertex_y + 1, x] = -1
        lin.append((x, top_left_vertex_y + 1))
        new_image[top_left_vertex_y - 2, x] = 1
        lout.append((x, top_left_vertex_y - 2))
        new_image[bottom_right_vertex_y + 2, x] = 1
        lout.append((x, top_left_vertex_y + 2))

    new_image[top_left_vertex_y - 1, top_left_vertex_x - 1] = 1
    lout.append((top_left_vertex_x - 1, top_left_vertex_y - 1))
    new_image[bottom_right_vertex_y + 1, top_left_vertex_x - 1] = 1
    lout.append((top_left_vertex_x - 1, bottom_right_vertex_y + 1))
    new_image[bottom_right_vertex_y + 1, bottom_right_vertex_x + 1] = 1
    lout.append((bottom_right_vertex_x + 1, bottom_right_vertex_y + 1))
    new_image[top_left_vertex_y - 1, bottom_right_vertex_x + 1] = 1
    lout.append((bottom_right_vertex_x + 1, top_left_vertex_y - 1))
    return int(color_sum / square_size)


def save_image(image, file_path):
    img = Image.fromarray(image)
    img = img.convert("I")
    img.save(file_path)


def save_colored_image(image, file_path):
    img = Image.fromarray(image, "RGB")
    img = img.convert("RGB")
    img.save(file_path)


save_path = "../../generated/"