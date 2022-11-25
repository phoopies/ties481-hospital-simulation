import argparse
from config import *

# Additional type
def process_type(s):
    try:
        d = s.split(",")
        count, time = int(d[0]), float(d[1])
        return count, time
    except:
        raise argparse.ArgumentTypeError(
            "Process argument should be of format 'count[int],time[float]'"
        )


class Parser(argparse.ArgumentParser):
    def __init__(self) -> None:
        super().__init__(prog="Hospital simulation")

        self.add_argument("-v", "--arrival", type=float, default=T_INTER)

        self.add_argument(
            "-p",
            "--preparation",
            type=process_type,
            default=(PREPARATION["NUM_UNITS"], PREPARATION["TIME_M"]),
        )

        self.add_argument(
            "-o",
            "--operation",
            type=process_type,
            default=(OPERATION["NUM_UNITS"], OPERATION["TIME_M"]),
        )

        self.add_argument(
            "-r",
            "--recovery",
            type=process_type,
            default=(RECOVERY["NUM_UNITS"], RECOVERY["TIME_M"]),
        )

        self.add_argument("-a", "--accident", type=float, default=ACCIDENT_PROB)
        self.add_argument("-d", "--death", type=float, default=DEATH_PROB)

        self.add_argument("-c", "--count", type=int, default=SIM_COUNT)
        self.add_argument("-t", "--time", type=float, default=SIM_TIME)

        self.add_argument("-f", "--filename", type=str, default=None)

        # self.add_argument("-s", "--seed", type=int, default=RANDOM_SEED)
