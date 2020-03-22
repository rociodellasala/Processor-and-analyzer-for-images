import numpy as np


def gaussian_generator(mu, sigma, size):
    return np.random.normal(mu, sigma, size)


def rayleigh_generator(xi, size):
    return np.random.rayleigh(xi, size)


def exponential_generator(lambda_value, size):
    beta = 1 / lambda_value
    return np.random.exponential(beta, size)


def uniform_generator(lowest, highest, size):
    return np.random.uniform(lowest, highest, size)

