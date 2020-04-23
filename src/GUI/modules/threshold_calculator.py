import numpy as np
from PIL import Image
from math import pow
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


def otsu_threshold(image, image_height, image_width):
    pixels = np.array(image)
    probability = get_probability_distribution(pixels, image_height, image_width)
    probability_acummulated = get_accumulated_probability_distribution(probability)
    medias = get_medias(probability)
    global_media = 0
    for i in range(0, constants.MAX_COLOR_VALUE + 1):
        global_media += i * probability[i]
    variance = get_variance(global_media, medias, probability_acummulated)
    threshold = get_threshold_from_variance(variance)
    image_threshold(image, image_width, image_height, threshold)
    return threshold


def get_probability_distribution(pixels, image_height, image_width):
    size = image_height * image_width
    probability = np.zeros(constants.MAX_COLOR_VALUE + 1)
    for y in range(0, image_height):
        for x in range(0, image_width):
            index = pixels[y, x]
            probability[index] += 1
    return probability / size



def get_accumulated_probability_distribution(probability):
    probability_acummulated = np.zeros(constants.MAX_COLOR_VALUE + 1)
    probability_acummulated[0] = probability[0]
    for i in range(1, constants.MAX_COLOR_VALUE + 1):
        probability_acummulated[i] = probability_acummulated[i - 1] + probability[i]
    return probability_acummulated


def get_medias(probability):
    medias = np.zeros(constants.MAX_COLOR_VALUE + 1)
    for i in range(0, constants.MAX_COLOR_VALUE + 1):
        medias[i] = 0
        for j in range(0, i + 1):
            medias[i] += j * probability[j]
    return medias


def get_variance(global_media, medias, accumulated_probability):
    variance = np.zeros(constants.MAX_COLOR_VALUE + 1)
    for i in range(0, constants.MAX_COLOR_VALUE + 1):
        if int(accumulated_probability[i] == 0) or int(accumulated_probability[i]) == 1:
            variance[i] = -1
        else:
            numerator = pow(global_media * accumulated_probability[i] - medias[i], 2)
            denominator = accumulated_probability[i] * (1 - accumulated_probability[i])
            variance[i] = numerator / denominator
    return variance


def get_threshold_from_variance(variance):
    max = np.max(variance)
    possible_thresholds = np.zeros(1)
    for i in range(0, constants.MAX_COLOR_VALUE + 1):
        if variance[i] == max:
            possible_thresholds = np.append(possible_thresholds, i)
    return np.mean(possible_thresholds[1:])


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



