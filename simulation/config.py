from numpy.random import exponential

CSV_SEPARATOR = "\t"
SAVE_FILE_LOCATION = "results"

PREPARATION = {  # Preparation facility info
    "NUM_UNITS": 3,
    "TIME_M": 40,
}

OPERATION = {  # Operation facility info
    "NUM_UNITS": 1,
    "TIME_M": 20,
}

RECOVERY = {  # Recovery facility info
    "NUM_UNITS": 3,
    "TIME_M": 40,
}

T_INTER = 25  # Generate accident/patient about every x time units

OFFSET = 0 # Ignore results for first `OFFSET` time units.
SIM_TIME = 1000  # Simulation time. Total simulation time will be `SIM_TIME` + `OFFSET`
SIM_COUNT = 20  # Simulation count - How many times should the simulation be run

ACCIDENT_PROB = 0.0 # Probability for an accident in each generation
DEATH_PROB = 0.0  # Probability for death in operation

VERBOSE = False # Print info about the patient going through the processes

RANDOM_SEED = 1337

DISTRIBUTION = exponential


