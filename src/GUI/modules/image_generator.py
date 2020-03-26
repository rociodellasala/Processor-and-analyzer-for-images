from PIL import Image
from math import sqrt
from math import pow
from tkinter import messagebox
from src.GUI import gui_constants


# Rectangle draw functions
def generate_rectangle(image_name, image_width, image_height, rectangle_width, rectangle_height, filled):
    if image_width >= 2 * rectangle_width and image_height >= 2 * rectangle_height:
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
        global save_path
        new_image.save(save_path + image_name)
        new_image.show()
    else:
        messagebox.showerror(title="Error", message="Width must be at least 2 times greater than the image width"
                                                    "and height must be at least 2 times grater than image height")


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
        pixels[x, height] = 255
    return pixels


def draw_vertical_line(pixels, width, starting_y, ending_y):
    for y in range(starting_y, ending_y + 1):
        pixels[width, y] = 255
    return pixels


# Circle draw functions
def generate_circle(image_name, image_width, image_height, circle_radius, filled):
    if image_width >= 2 * circle_radius and image_height >= 2 * circle_radius:
        new_image = Image.new("L", (int(image_width), int(image_height)))
        pixels = new_image.load()
        medium_x = image_width/2
        medium_y = image_height/2
        if filled:
            draw_filled_circle(pixels, medium_x, medium_y, circle_radius)
        else:
            draw_empty_circle(pixels, medium_x, medium_y, circle_radius)
        new_image.save(save_path + image_name)
        new_image.show()
    else:
        messagebox.showerror(title="Error", message="Both width and height of the image "
                                                    "must be at least 2 times greater than the radius")


def draw_empty_circle(pixels, medium_x, medium_y, circle_radius):
    border = circle_radius * 0.05
    for x in range(-circle_radius, circle_radius):
        for y in range(-circle_radius, circle_radius):
            aux = sqrt(pow(x, 2) + pow(y, 2))
            if circle_radius - border < aux < circle_radius:
                pixels[medium_x + x, medium_y + y] = 255
    return pixels


def draw_filled_circle(pixels, medium_x, medium_y, circle_radius):
    for x in range(-circle_radius, circle_radius):
        for y in range(-circle_radius, circle_radius):
            if sqrt(pow(x, 2) + pow(y, 2)) <= circle_radius:
                pixels[medium_x + x, medium_y + y] = 255
    return pixels


def gray_faded_image(image_width, image_height):
    new_image = Image.new("L", (int(image_width), int(image_height)))
    pixels = new_image.load()
    gray_value = 0
    column_length = int(image_width / gui_constants.MAX_COLOR_VALUE)
    if column_length == 0:
        column_length = 1
    current_column = 0
    for x in range(0, image_width):
        for y in range(0, image_height):
            pixels[x, y] = gray_value
        current_column += 1
        if current_column == column_length:
            current_column = 0
            gray_value += 1
    global save_path
    new_image.save(save_path + "gray_fading.png")
    new_image.show()


def color_faded_image(image_width, image_height, red, green, blue):
    new_image = Image.new("RGB", (int(image_width), int(image_height)))
    pixels = new_image.load()
    color_value = 0
    column_length = int(image_width / gui_constants.MAX_COLOR_VALUE)
    if column_length == 0:
        column_length = 1
    current_column = 0
    for x in range(0, image_width):
        for y in range(0, image_height):
            red_value = color_value if red else 0
            green_value = color_value if green else 0
            blue_value = color_value if blue else 0
            pixels[x, y] = (red_value, green_value, blue_value)
        current_column += 1
        if current_column == column_length:
            current_column = 0
            color_value += 1
    global save_path
    new_image.save(save_path + "color_fading.png")
    new_image.show()


save_path = "../../draws/"
