import random


def random_chance(probability: float) -> bool:
    """
    Returns a random True or False, whereby True is more likely with a higher weight, and vice versa.
    :param probability: float: Probability of getting True, between 0 and 1
    :return: bool
    """
    return random.random() < probability


def advantage_chance(advantage: float):
    """
    Returns a random True or False, where if advantage is 0, it is a 50/50 to be True, and if it is 1, it is 100% to be True
    :param advantage: float: Probability of getting True, between 0 and 1
    :return: bool
    """
    return random.random() < (advantage + 1) / 2
