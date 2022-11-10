import random
from typing import Callable, List
from Patient import Patient
import simpy
from helpers import happens


class PatientGenerator:
    def __init__(
        self,
        env: simpy.Environment,
        interval_time_min: float,
        distribution: Callable[[float], float],
        accident_probability: float,
    ) -> None:
        self.distribution = distribution
        self.env = env
        self.interval = interval_time_min
        self.accident_prob = accident_probability
        self.patients_generated = 0

    def generate_patient(self) -> Patient:
        self.patients_generated += 1
        return Patient(self.env, f"patient {self.patients_generated}")

    def generate_patients(self, count: int) -> List[Patient]:
        patients: List[Patient] = []
        for _ in range(count):
            patients.append(self.generate_patient())
        return patients

    def wait(self, wait_time_min: float = None):
        wait_time = wait_time_min or self.distribution(self.interval)
        return self.env.timeout(wait_time)

    def generate(self) -> List[Patient]:
        to_generate = random.randint(5, 15) if happens(self.accident_prob) else 1
        return self.generate_patients(to_generate)
