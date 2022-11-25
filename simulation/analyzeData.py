from typing import Tuple
from helpers import conf_interval
import numpy as np
import sys
import csv


def get_data(filename):
    data = None
    with open(filename, "r") as f:
        csv_data = csv.DictReader(f, delimiter="\t")
        data = list(map(lambda row: {key: float(row[key]) for key in row }, csv_data))
    return data


def get_mean_and_ci(data, value_name) -> Tuple[float, Tuple[float, float]]:
    values = list(map(lambda d: d[value_name], data))
    mean = np.mean(values)
    ci = conf_interval(1.96, len(values), mean, np.std(values))
    return (mean, ci)

def print_value_info(data, value_name):
    (mean, ci) = get_mean_and_ci(
        data, value_name
    )
    print(f"Data for {value_name}")
    print(f"Mean = {mean}")
    print(f"Confidence interval = {ci}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Provide a filename or two filenames as arguments")
    data = get_data(sys.argv[1])
    if len(sys.argv) > 2:
        print("Two files detected. Performing analysis for their differences")
        more_data = get_data(sys.argv[2])
        if len(more_data) != len(data):
            raise ValueError("Both files should have the same amount of data")
        data = [{key: a[key] - b[key] for key in a} for a, b in zip(data, more_data)]
    
    interesting_values = ["wait_time", "entrance_queue", "operation_time"]
    for value in interesting_values:
        print_value_info(data, value)
        print("*"*80)

