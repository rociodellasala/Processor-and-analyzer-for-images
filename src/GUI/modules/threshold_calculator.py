import numpy as np
from PIL import Image
from src.GUI import gui_constants as constants


def global_threshold(image, image_height, image_width):
    pixels = np.array(image)
    current_t = int(np.mean(pixels))
    last_t = -1
    while abs(last_t - current_t) <= 0.5:
        last_t = current_t
        current_t = calculate_global_threshold(pixels, image_height, image_width, last_t)
    image_threshold(image, image_width, image_height, current_t)


def calculate_global_threshold(pixels, image_height, image_width, t):
    g1 = np.zeros(1)
    g2 = np.zeros(1)
    for y in range(0, image_height):
        for x in range(0, image_width):
            if pixels[y, x] >= int(t + 1):
                g2 = np.append(g2, pixels[y, x])
            else:
                g1 = np.append(g1, pixels[y, x])
    m1 = np.mean(g1[1:])
    m2 = np.mean(g2[1:])
    return (m1 + m2) / 2


def image_threshold(image, width, height, threshold):
    pixels = image.load()
    new_image = np.zeros((height, width))
    for y in range(0, height):
        for x in range(0, width):
            current_value = 0 if int(pixels[x, y]) <= threshold else constants.MAX_COLOR_VALUE
            new_image[y, x] = current_value
    save_image(new_image, save_path + "global_threshold_image.ppm")
    img = Image.fromarray(new_image)
    img.show()


def save_image(image, file_path):
    img = Image.fromarray(image)
    img = img.convert("I")
    img.save(file_path)


save_path = "../../generated/"



