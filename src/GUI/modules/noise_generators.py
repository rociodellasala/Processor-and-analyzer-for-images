import numpy as np
from PIL import Image
from number_generators import gaussian_generator
from number_generators import rayleigh_generator
from number_generators import exponential_generator
from image_operations import lineally_adjust_image_values


def gaussian_noise_generator(percentage, is_additive, image, image_width, image_height, mu, sigma):
    pixels = image.load()
    noise_values = gaussian_generator(mu, sigma, image_height * image_width)
    new_image = get_image_with_noise(pixels, image_height, image_width, noise_values,
                                     is_additive, percentage)
    save_image(new_image, save_path + "gaussian_noise_image.ppm")
    img = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    img.show()
    return new_image


def rayleigh_noise_generator(percentage, is_additive, image, image_width, image_height, xi):
    pixels = image.load()
    noise_values = rayleigh_generator(xi, image_height * image_width)
    new_image = get_image_with_noise(pixels, image_height, image_width, noise_values,
                                     is_additive, percentage)
    save_image(new_image, save_path + "rayleigh_noise_image.ppm")
    img = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    img.show()
    return new_image


def exponential_noise_generator(percentage, is_additive, image, image_width, image_height, lambda_value):
    pixels = image.load()
    noise_values = exponential_generator(lambda_value, image_height * image_width)
    new_image = get_image_with_noise(pixels, image_height, image_width, noise_values,
                                     is_additive, percentage)
    save_image(new_image, save_path + "exponential_noise_image.ppm")
    img = Image.fromarray(lineally_adjust_image_values(new_image, image_width, image_height))
    img.show()
    return new_image


def get_image_with_noise(pixels, image_height, image_width, noise_generated_values,
                         is_additive, percentage):
    new_image = np.zeros((image_height, image_width))
    if is_additive:
        noise_values = np.zeros((image_height, image_width))
    else:
        noise_values = np.ones((image_height, image_width))
    count = 0
    for y in range(0, image_height):
        for x in range(0, image_width):
            if np.random.uniform(0.0, 1.0, 1)[0] <= percentage:
                noise_values[y, x] = noise_generated_values[count]
                count += 1
            if is_additive:
                new_image[y, x] = pixels[x, y] + noise_values[y, x]
            else:
                new_image[y, x] = pixels[x, y] * noise_values[y, x]
    return new_image


def salt_and_pepper_noise_generator(image, image_width, image_height, p0):
    p1 = 1 - p0
    pixels = image.load()
    new_image = np.zeros((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width):
            current_value = np.random.uniform(0.0, 1.0, 1)[0]
            if current_value <= p0:
                new_image[y, x] = 0
            elif current_value >= p1:
                new_image[y, x] = 255
            else:
                new_image[y, x] = pixels[x, y]
    save_image(new_image, save_path + "salt_and_pepper_noise_image.ppm")
    img = Image.fromarray(new_image)
    img.show()
    return new_image


def save_image(image, file_path):
    img = Image.fromarray(image)
    img = img.convert("I")
    img.save(file_path)


save_path = "../../generated/"
