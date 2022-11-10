import random
from HospitalUnit import HospitalUnit, ProcessData
import simpy
from typing import Callable
from helpers import happens


class OperationUnit(HospitalUnit):
    def __init__(
        self,
        env: simpy.Environment,
        time_to_process_min: float,
        room_count: int,
        distribution: Callable[[float], float],
        death_probability: float,
    ) -> None:
        super().__init__(env, time_to_process_min, room_count, distribution)
        self.death_probability = death_probability

    def process(self) -> ProcessData:
        process_time = super().get_processing_time()
        pd: ProcessData = None
        if happens(self.death_probability):
            # Wait any time between 0 and actual operation time
            pd = yield self.env.process(super().process(process_time * random.random()))
            pd.success = False
        else:
            pd = yield self.env.process(super().process(process_time))
        return pd
