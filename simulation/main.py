"""
hospital flow simulation.
"""

import simpy
from DataManager import DataManager
from config import *
from helpers import *
from HospitalUnit import HospitalUnit
from OperationUnit import OperationUnit
from Hospital import Hospital
from PatientGenerator import PatientGenerator
from Parser import Parser


def setup(env: simpy.Environment, dm: DataManager, config):
    """Create a hospital, a number of initial patients and keep creating patients"""
    # Create the units
    preparation_unit = HospitalUnit(
        env, *config.preparation, DISTRIBUTION
    )
    operation_unit = OperationUnit(
        env, *config.operation, DISTRIBUTION, config.death
    )
    recovery_unit = HospitalUnit(
        env, *config.recovery, DISTRIBUTION
    )

    # Create the hospital
    hospital = Hospital(preparation_unit, operation_unit, recovery_unit)

    patient_generator = PatientGenerator(env, config.arrival, DISTRIBUTION, config.accident)

    # DataManager for patients who arrived before `OFFSET` so their data can be ignored
    fake_dm = DataManager(42)

    # Create more patients while the simulation is running
    while True:
        yield patient_generator.wait()
        used_dm = fake_dm if env.now < OFFSET else dm
        patients = patient_generator.generate()
        if len(patients) > 1:
            used_dm.accidents += 1
        for patient in patients:
            env.process(patient.go_through(hospital, used_dm, VERBOSE))


def create_filename(config):
    return f'{config.arrival}-p{config.preparation[0]}t{config.preparation[1]}-o{config.operation[0]}t{config.operation[1]}-r{config.recovery[0]}t{config.recovery[1]}-d{config.death}-a{config.accident}'


def main():
    parser = Parser()
    config = parser.parse_args()
    # Setup and start the simulation
    print("Hospital simulation")
    
    if RANDOM_SEED:
        random.seed(RANDOM_SEED)
        np.random.seed(RANDOM_SEED)

    # for storing all simulation data
    full_dm = DataManager(0, 0)

    filename = config.filename or create_filename(config)

    sim_time = config.time + OFFSET
    # Create an environment and start the setup process
    for _ in range(config.count):
        dm = DataManager(config.time)
        env = simpy.Environment()
        hospital = setup(env, dm, config)
        env.process(hospital)

        # Execute!
        env.run(until=sim_time)
        dm.output()
        dm.output_to_save_file(f"{SAVE_FILE_LOCATION}\\{filename}.csv")
        full_dm += dm

    if SIM_COUNT > 1:
        print("\n\nAverage data from all simulations")
        full_dm.output()


if __name__ == "__main__":
    main()
