import numpy as np
from number_generators import gaussian_generator
from PIL import Image


def gaussian_noise_generator(percentage, is_additive, image, image_width, image_height, mu, sigma):
    noise_values = None
    pixels = image.load()
    new_image = np.zeros((image_height, image_width))
    if is_additive:
        noise_values = np.zeros((image_height, image_width))
    else:
        noise_values = np.ones((image_height, image_width))
    for y in range(0, image_height):
        for x in range(0, image_width):
            if np.random.uniform(0.0, 1.0, 1)[0] > percentage:
                noise_values[y, x] = gaussian_generator(mu, sigma, 1)[0]
            if is_additive:
                new_image[y, x] = pixels[x, y] + noise_values[y, x]
            else:
                new_image[y, x] = pixels[x, y] * noise_values[y, x]
    img = Image.fromarray(new_image)
    img.show()
    return new_image
