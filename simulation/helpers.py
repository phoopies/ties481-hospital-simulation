import random
import numpy as np

def happens(probability: float) -> bool:
    r = random.random()
    return r < probability

def conf_interval(t_value, n, mean, sd):
    p = t_value*(sd / np.sqrt(n))
    return (mean - p, mean + p)