from PIL import Image
from math import cos
from math import sin

def generate_rectangle(image_name, image_width, image_height, rectangle_width, rectangle_height, filled):
    new_image = Image.new("L", (int(image_width), int(image_height)))
    pixels = new_image.load()
    starting_x = int(image_width / 2 - rectangle_width / 2)
    ending_x = int(image_width / 2 + rectangle_width / 2)
    starting_y = int(image_height / 2 - rectangle_height / 2)
    ending_y = int(image_height / 2 + rectangle_height / 2)
    if filled:
        draw_filled_rectangle(pixels, starting_x, ending_x, starting_y, ending_y)
    else:
        draw_empty_rectangle(pixels, starting_x, ending_x, starting_y, ending_y)
    new_image.save(image_name)
    new_image.show()


def draw_filled_rectangle(pixels, left, right, upper, lower):
    for x in range(left, right + 1):
        for y in range(upper, lower + 1):
            pixels[x, y] = 255
    return pixels


def draw_empty_rectangle(pixels, left, right, upper, lower):
    pixels = draw_horizontal_line(pixels, upper, left, right)
    pixels = draw_horizontal_line(pixels, lower, left, right)
    pixels = draw_vertical_line(pixels, left, upper, lower)
    return draw_vertical_line(pixels, right, upper, lower)


def draw_horizontal_line(pixels, height, starting_x, ending_x):
    for x in range(starting_x, ending_x + 1):
        pixels[height, x] = 255
    return pixels


def draw_vertical_line(pixels, width, starting_y, ending_y):
    for y in range(starting_y, ending_y + 1):
        pixels[y, width] = 255
    return pixels

def generate_circle(image_name, image_width, image_height, circle_radius, filled):
    new_image = Image.new("L", (int(image_width), int(image_height)))
    pixels = new_image.load()
    medium_x = image_width/2
    medium_y = image_height/2
    if filled:
        draw_filled_circle(pixels, medium_x, medium_y, circle_radius)
    else:
        draw_empty_circle(pixels, medium_x, medium_y, circle_radius)
    new_image.save(image_name)
    new_image.show()


def draw_empty_circle(pixels, medium_x, medium_y, circle_radius):
    for theta in range(0, 360):
        x = medium_x + circle_radius * cos(theta)
        y = medium_y + circle_radius * sin(theta)
        pixels[x, y] = 255
    return pixels


def draw_filled_circle(pixels, medium_x, medium_y, circle_radius):
    for theta in range(0, 360):
        for radius in range(0, circle_radius):
            x = medium_x + radius * cos(theta)
            y = medium_y + radius * sin(theta)
            pixels[x, y] = 255
    return pixels
