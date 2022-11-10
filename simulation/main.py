"""
hospital flow simulation.
"""

from typing import List
import simpy
from DataManager import DataManager
from config import *
from helpers import *
from HospitalUnit import HospitalUnit
from OperationUnit import OperationUnit
from Hospital import Hospital
from PatientGenerator import PatientGenerator


def setup(env: simpy.Environment, dm: DataManager):
    """Create a hospital, a number of initial patients and keep creating patients"""

    # Create the units
    preparation_unit = HospitalUnit(
        env, PREPARATION["TIME_M"], PREPARATION["NUM_UNITS"], DISTRIBUTION
    )
    operation_unit = OperationUnit(
        env, OPERATION["TIME_M"], OPERATION["NUM_UNITS"], DISTRIBUTION, DEATH_PROB
    )
    recovery_unit = HospitalUnit(
        env, RECOVERY["TIME_M"], RECOVERY["NUM_UNITS"], DISTRIBUTION
    )

    # Create the hospital
    hospital = Hospital(preparation_unit, operation_unit, recovery_unit)

    patient_generator = PatientGenerator(env, T_INTER, DISTRIBUTION, ACCIDENT_PROB)

    # Create 4 initial patients
    # patient_generator.generate_patients(4)

    # Create more patients while the simulation is running
    while True:
        yield patient_generator.wait()
        patients = patient_generator.generate()
        if len(patients) > 1:
            dm.accidents += 1
        for patient in patients:
            env.process(patient.go_through(hospital, dm, VERBOSE))


if __name__ == "__main__":
    # Setup and start the simulation
    print("Hospital simulation")

    # random.seed(43)  # This helps reproducing the results

    # for storing all simulation data
    full_dm = DataManager(SIM_TIME)

    # Create an environment and start the setup process
    for _ in range(SIM_COUNT):
        dm = DataManager(SIM_TIME)
        env = simpy.Environment()
        hospital = setup(env, dm)
        env.process(hospital)

        # Execute!
        env.run(until=SIM_TIME)
        dm.output()
        full_dm += dm

    if SIM_COUNT > 1:
        print("\n\nAverage data from all simulations")
        full_dm.output()
