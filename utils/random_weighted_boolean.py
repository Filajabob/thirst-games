import random


def random_weighted_boolean(weight: float) -> bool:
    """
    Returns a random True or False, whereby True is more likely with a higher weight, and vice versa.
    :param weight: float: Probabilty of getting True, between 0 and 1
    :return: bool
    """
    return random.random() < (weight + 1) / 2
