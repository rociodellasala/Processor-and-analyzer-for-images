from PIL import Image


def generate_rectangle(image_name, image_width, image_height, rectangle_width, rectangle_height, filled):
    new_image = Image.new("L", (int(image_width), int(image_height)))
    pixels = new_image.load()
    starting_x = int(image_width / 2 - rectangle_width / 2)
    ending_x = int(image_width / 2 + rectangle_width / 2)
    starting_y = int(image_height / 2 - rectangle_height / 2)
    ending_y = int(image_height / 2 + rectangle_height / 2)
    pixels = draw_empty_rectangle(pixels, starting_x, ending_x, starting_y, ending_y)
    new_image.save(image_name)
    new_image.show()


def draw_filled_rectangle(pixels, upper_left, upper_right, lower_left, lower_right):
    return None


def draw_empty_rectangle(pixels, left, right, upper, lower):
    pixels = draw_horizontal_line(pixels, upper, left, right)
    pixels = draw_horizontal_line(pixels, lower, left, right)
    pixels = draw_vertical_line(pixels, left, upper, lower)
    # pixels[lower, right] = 255
    return draw_vertical_line(pixels, right, upper, lower)


def draw_horizontal_line(pixels, height, starting_x, ending_x):
    for x in range(starting_x, ending_x + 1):
        pixels[height, x] = 255
    return pixels


def draw_vertical_line(pixels, width, starting_y, ending_y):
    for y in range(starting_y, ending_y + 1):
        pixels[y, width] = 255
    return pixels
