import numpy as np
import cv2
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
    delta_rho = 1
    rows = int((max_rho - min_rho) / delta_rho) + 1
    delta_theta = (15 / 180) * np.pi
    cols = int(((np.pi / 2) - (- np.pi / 2)) / delta_theta)
    cols = 6
    thetas = [0, np.pi / 8, np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2]
    accumulator = np.zeros((rows, cols))
    for y in range(0, image_height):
        for x in range(0, image_width):
            if image[y, x] == constants.MAX_COLOR_VALUE:
                for rho in range(0, rows):
                    for theta in range(0, cols):
                        current_rho = min_rho + rho * delta_rho
                        # current_theta = (-np.pi / 2) + (theta * delta_theta)
                        current_theta = thetas[theta]
                        value = abs(current_rho - x * np.cos(current_theta) - y * np.sin(current_theta))
                        if value <= epsilon:
                            accumulator[rho, theta] += 1

    # arr = np.zeros((10000, 2))
    # index = 0
    new_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    for y in range(0, image_height):
        for x in range(0, image_width):
            new_image[y, x] = image[y, x]
    for rho in range(0, rows):
        for theta in range(0, cols):
            if accumulator[rho, theta] >= threshold:
                current_rho = min_rho + rho * delta_rho
                # current_theta = (-np.pi / 2) + (theta * delta_theta)
                current_theta = thetas[theta]
                draw_lines(current_rho, current_theta, new_image, image_height, image_width)
                # arr[index, 0] = current_rho
                # arr[index, 1] = current_theta
                # index += 1

    save_colored_image(new_image, save_path + "hough_transform.ppm")
    img = Image.fromarray(new_image, 'RGB')
    img.show()


def circular_hough_transform(image, image_height, image_width, threshold, epsilon, radius):
    original = np.array(image)
    image = canny_method(image, image_height, image_width, 10, 10, 3, show_image=False)
    max_radius = radius + 5;
    min_radius = radius - 5;
    delta_radius = 0.1
    radius_quantity = int((max_radius - min_radius) / delta_radius + 1)
    a = image_width / 2
    max_a = a + 2
    min_a = a - 2
    delta_a = 0.1
    a_quantity = int((max_a - min_a) / delta_a + 1)
    b = image_height / 2
    max_b = b + 2
    min_b = b - 2
    delta_b = 0.1
    b_quantity = int((max_b - min_b) / delta_b + 1)
    accumulator = np.zeros((radius_quantity, a_quantity, b_quantity))
    for y in range(0, image_height):
        for x in range(0, image_width):
            if image[y, x] == constants.MAX_COLOR_VALUE:
                for radius_index in range(0, radius_quantity):
                    for a_index in range(0, a_quantity):
                        for b_index in range(0, b_quantity):
                            current_radius = min_radius + radius_index * delta_radius
                            current_a = min_a + a_index * delta_a
                            current_b = min_b + b_index * delta_b
                            x_difference = pow(x - current_a, 2)
                            y_difference = pow(y - current_b, 2)
                            squared_radius = pow(current_radius, 2)
                            value = abs(x_difference + y_difference - squared_radius)
                        if value <= epsilon:
                            accumulator[radius_index, a_index, b_index] += 1

    arr = np.zeros((10000, 3))
    index = 0
    new_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    for y in range(0, image_height):
        for x in range(0, image_width):
            new_image[y, x, 0] = original[y, x]
            new_image[y, x, 1] = original[y, x]
            new_image[y, x, 2] = original[y, x]

    for radius_index in range(0, radius_quantity):
        for a_index in range(0, a_quantity):
            for b_index in range(0, b_quantity):
                if accumulator[radius_index, a_index, b_index] >= threshold:
                    current_radius = min_radius + delta_radius * radius_index
                    current_a = min_a + delta_a * a_index
                    current_b = min_b + delta_b * b_index
                    draw_circle(current_radius, current_a, current_b, new_image, image_height, image_width, epsilon)
                    arr[index, 0] = current_radius
                    arr[index, 1] = current_a
                    arr[index, 2] = current_b
                    index += 1

    save_colored_image(new_image, save_path + "circular_hough_transform.ppm")
    img = Image.fromarray(new_image, 'RGB')
    img.show()


def draw_lines(rho, theta, image, image_height, image_width):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    # cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    if x1 == x2:
        for y in range(0, image_width):
            image[y, int(x0), 0] = constants.MAX_COLOR_VALUE
            image[y, int(x0), 1] = 0
            image[y, int(x0), 2] = 0

    else:
        slope = (y2 - y1) / (x2 - x1)
        origin_ordenate = y0 - slope * x0
        for x in range(0, image_width):
            y = int(slope * x + origin_ordenate)
            # y = int(- ((np.cos(theta) / np.sin(theta)) * x) + rho / np.sin(theta))
            if 0 <= y < image_height:
                image[y, x, 0] = constants.MAX_COLOR_VALUE
                image[y, x, 1] = 0
                image[y, x, 2] = 0


def draw_circle(radius, a, b, image, image_height, image_width, epsilon):
    x_start = int(a - radius)
    x_end = int(a + radius)
    y_start = int(b - radius)
    y_end = int(b + radius)

    for y in range(y_start, y_end + 1):
        for x in range(x_start, x_end + 1):
            if 0 <= x < image_width and 0 <= y < image_height:
                x_difference = pow(x - a, 2)
                y_difference = pow(y - b, 2)
                squared_radius = pow(radius, 2)
                value = abs(x_difference + y_difference - squared_radius)
                if value <= epsilon:
                    image[y, x, 0] = 0
                    image[y, x, 1] = constants.MAX_COLOR_VALUE
                    image[y, x, 2] = 0
                    for i in range(1, 5):
                        image[y + i, x, 1] = constants.MAX_COLOR_VALUE
                        image[y - i, x, 1] = constants.MAX_COLOR_VALUE
                        image[y, x + i, 1] = constants.MAX_COLOR_VALUE
                        image[y, x - i, 1] = constants.MAX_COLOR_VALUE
                        image[y, x, 1] = constants.MAX_COLOR_VALUE



def pixel_exchange(image, image_height, image_width, top_left_vertex_x, top_left_vertex_y, bottom_right_vertex_x,
                   bottom_right_vertex_y, epsilon, max_iterations, is_gray=False):
    pixels = np.array(image)
    new_image = np.ones((image_height, image_width)) * 3
    lin = {}
    lout = {}
    object_color = get_object_color(new_image, pixels, top_left_vertex_x, top_left_vertex_y, bottom_right_vertex_x,
                                    bottom_right_vertex_y, lin, lout, is_gray)
    for i in range(0, max_iterations):
        new_lin = {}
        new_lout = {}
        iterate_over_lout(pixels, image_height, image_width, new_image, object_color, epsilon, lout, new_lout, new_lin, is_gray)
        iterate_over_lin(image_height, image_width, new_image, lin, new_lin, new_lout)
        second_lin = {}
        second_lout = {}
        remove_extra_lin(pixels, image_height, image_width, new_image, new_lin, second_lin, second_lout, object_color,
                         epsilon, is_gray)
        remove_extra_lout(image_height, image_width, new_image, new_lout, second_lin, second_lout)
        lin = second_lin
        lout = second_lout
        # lin = new_lin
        # lout = new_lout
    border_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    for y in range(0, image_height):
        for x in range(0, image_width):
            if new_image[y, x] == -1 or new_image[y, x] == 1:
                border_image[y, x, 1] = np.uint8(255)
            else:
                border_image[y, x, 0] = np.uint8(pixels[y, x])
                border_image[y, x, 1] = np.uint8(pixels[y, x])
                border_image[y, x, 2] = np.uint8(pixels[y, x])


    save_colored_image(border_image, save_path + "pixel_exchange_image.ppm")
    img = Image.fromarray(border_image, 'RGB')
    img.show()


def iterate_over_lout(image, image_height, image_width, new_image, object_color, epsilon, lout, new_lout, new_lin, is_gray):
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    for pixel in lout:
        current_x = pixel[0]
        current_y = pixel[1]
        if has_same_color_as_object(image, current_y, current_x, object_color, epsilon, is_gray):
            new_image[current_y, current_x] = -1
            new_lin[(current_x, current_y)] = -1
            for i in range(0, 4):
                x_increment = directions[i][0]
                y_increment = directions[i][1]
                if (0 <= x_increment + current_x < image_width and 0 <= y_increment + current_y < image_height and
                        new_image[current_y + y_increment, current_x + x_increment] == 3):
                    new_image[current_y + y_increment, current_x + x_increment] = 1
                    new_lout[(current_x + x_increment, current_y + y_increment)] = 1
        else:
            new_lout[(current_x, current_y)] = 1


def has_same_color_as_object(image, y, x, object_color, epsilon, is_gray):
    if is_gray:
        return abs(image[y, x] - object_color) <= epsilon
    else:
        current_color = np.zeros(3)
        current_color[0] = image[y, x, 0]
        current_color[1] = image[y, x, 1]
        current_color[2] = image[y, x, 2]
        value = 1 - np.linalg.norm(current_color - object_color) / (sqrt(3) * 256)
        return value > 1 - epsilon


def iterate_over_lin(image_height, image_width, new_image, lin, new_lin, new_lout):
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
            if 0 <= new_x < image_width and 0 <= new_y < image_height and (new_x, new_y) in new_lout:
                blue_count += 1
        if blue_count == 0:
            new_image[new_y, new_x] = -3
        else:
            new_lin[(current_x, current_y)] = -1


def remove_extra_lin(image, image_height, image_width, new_image, lin, second_lin, second_lout, object_color, epsilon, is_gray):
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    for pixel in lin:
        current_x = pixel[0]
        current_y = pixel[1]
        if not has_same_color_as_object(image, current_y, current_x, object_color, epsilon, is_gray):
            second_lout[(current_x, current_y)] = 1
            new_image[current_y, current_x] = 1
            for i in range(0, 4):
                new_x = current_x + directions[i][1]
                new_y = current_y + directions[i][0]
                if 0 <= new_x < image_width and 0 <= new_y < image_height and new_image[new_y, new_x] == -3:
                    new_image[new_y, new_x] = -1
                    second_lin[(new_x, new_y)] = -1
        else:
            second_lin[(current_x, current_y)] = -1


def remove_extra_lout(image_height, image_width, new_image, lout, second_lin, second_lout):
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    for pixel in lout:
        current_x = pixel[0]
        current_y = pixel[1]
        lin_count = 0
        for i in range(0, 4):
            new_x = current_x + directions[i][1]
            new_y = current_y + directions[i][0]
            if 0 <= new_x < image_width and 0 <= new_y < image_height and (new_x, new_y) in second_lin:
                lin_count += 1
        if lin_count == 0:
            new_image[current_y, current_x] = 3
        else:
            second_lout[(current_x, current_y)] = 1


def get_object_color(new_image, pixels, top_left_vertex_x, top_left_vertex_y, bottom_right_vertex_x,
                     bottom_right_vertex_y, lin, lout, is_gray):
    color_sum = np.zeros(3)
    if is_gray:
        color_sum = 0
    square_height = (bottom_right_vertex_y - top_left_vertex_y) + 1
    square_width = (bottom_right_vertex_x - top_left_vertex_x) + 1
    square_size = square_height * square_width
    for y in range(top_left_vertex_y, bottom_right_vertex_y + 1):
        for x in range(top_left_vertex_x, bottom_right_vertex_x + 1):
            new_image[y, x] = -3
            if is_gray:
                color_sum += pixels[y, x]
            else:
                color_sum[0] += pixels[y, x, 0]
                color_sum[1] += pixels[y, x, 1]
                color_sum[2] += pixels[y, x, 2]

    for y in range(top_left_vertex_y, bottom_right_vertex_y + 1):
        new_image[y, top_left_vertex_x - 1] = -1
        lin[(top_left_vertex_x - 1, y)] = -1
        new_image[y, bottom_right_vertex_x + 1] = -1
        lin[(bottom_right_vertex_x + 1, y)] = -1
        new_image[y, top_left_vertex_x - 2] = 1
        lout[(top_left_vertex_x - 2, y)] = 1
        new_image[y, bottom_right_vertex_x + 2] = 1
        lout[(bottom_right_vertex_x + 2, y)] = 1

    for x in range(top_left_vertex_x, bottom_right_vertex_x + 1):
        new_image[top_left_vertex_y - 1, x] = -1
        lin[(x, top_left_vertex_y - 1)] = -1
        new_image[bottom_right_vertex_y + 1, x] = -1
        lin[(x, bottom_right_vertex_y + 1)] = -1
        new_image[top_left_vertex_y - 2, x] = 1
        lout[(x, top_left_vertex_y - 2)] = 1
        new_image[bottom_right_vertex_y + 2, x] = 1
        lout[(x, bottom_right_vertex_y + 2)] = 1

    new_image[top_left_vertex_y - 1, top_left_vertex_x - 1] = 1
    lout[(top_left_vertex_x - 1, top_left_vertex_y - 1)] = 1
    new_image[bottom_right_vertex_y + 1, top_left_vertex_x - 1] = 1
    lout[(top_left_vertex_x - 1, bottom_right_vertex_y + 1)] = 1
    new_image[bottom_right_vertex_y + 1, bottom_right_vertex_x + 1] = 1
    lout[(bottom_right_vertex_x + 1, bottom_right_vertex_y + 1)] = 1
    new_image[top_left_vertex_y - 1, bottom_right_vertex_x + 1] = 1
    lout[(bottom_right_vertex_x + 1, top_left_vertex_y - 1)] = 1
    # for y in range(top_left_vertex_y - 4, bottom_right_vertex_y + 5):
    #     for x in range(top_left_vertex_x - 4, bottom_right_vertex_x + 5):
    #         print(int(new_image[y, x]), end=' ' if new_image[y, x] >= 0 else '  ')
    #     print("")
    if is_gray:
        return int(color_sum / square_size)
    else:
        color_sum = color_sum / square_size
        color_sum[0] = int(color_sum[0])
        color_sum[1] = int(color_sum[1])
        color_sum[2] = int(color_sum[2])
        return color_sum


def save_image(image, file_path):
    img = Image.fromarray(image)
    img = img.convert("I")
    img.save(file_path)


def save_colored_image(image, file_path):
    img = Image.fromarray(image, "RGB")
    img = img.convert("RGB")
    img.save(file_path)


save_path = "../../generated/"