from typing import Callable
import simpy
from simpy.resources.resource import Request


class ProcessData:
    def __init__(self, process_time: float = 0, success: bool = False) -> None:
        self.process_time = process_time
        self.success = success


class WaitData:
    def __init__(self, wait_time: float, request: Request = None) -> None:
        self.wait_time = wait_time
        self.request = request


class HospitalUnit:
    def __init__(
        self,
        env: simpy.Environment,
        process_time_min: float,
        room_count: int,
        distribution: Callable[[float], float],
    ) -> None:
        self.env = env
        self.process_time = process_time_min
        self.rooms = room_count
        self.distribution = distribution
        self.resource = simpy.Resource(env, room_count)

    def wait_for(self) -> WaitData:
        request = self.resource.request()
        wait_start_time = self.env.now
        yield request
        wait_time = self.env.now - wait_start_time
        return WaitData(wait_time, request)

    def process(self, process_time_min: float = None) -> ProcessData:
        """The process of the unit."""
        process_time = (
            process_time_min if process_time_min else self.get_processing_time()
        )
        yield self.env.timeout(process_time)
        return ProcessData(process_time, True)

    def release(self, request: Request):
        self.resource.release(request)

    def get_processing_time(self) -> float:
        return self.distribution(self.process_time)
