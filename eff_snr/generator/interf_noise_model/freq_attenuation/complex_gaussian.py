from numpy import random, complex


def generate_complex_gaussian_distribution(n, mean_val, std_dev):
    return random.normal(loc=mean_val, scale=std_dev, size=(n, 2)).view(complex)
