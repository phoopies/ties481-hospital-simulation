import random


def happens(probability: float) -> bool:
    r = random.random()
    return r < probability
