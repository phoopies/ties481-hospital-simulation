# TODO might be interesting to know average times in different units and their queues.
# TODO maybe move some data over patient

class DataManager:
    def __init__(self, sim_time, sim_count = 1) -> None:
        self.waiting: float = 0
        self.throughput_time: float = 0
        self.hospital_throughput_time: float = 0
        self.patients_cleared: float = 0
        self.accidents: int = 0
        self.deaths: int = 0
        self.sim_time: float = sim_time
        self.sim_count: int = sim_count

    def output(self) -> str:
        print("*" * 50)
        print(f"{self.average_patients_cleared:.3g} patient(s) cleared!")
        print(f"Total time the operation unit was waiting: {self.average_waiting:.3g} minutes.")
        print(f"Total throughput time {self.average_throughput_time:.3g} minutes.")
        print(f"Average throughput time in hospital {self.average_throughput_time_in_hospital:.3g} minutes.")
        print(
            f"Operation unit(s) were in waiting mode {self.waiting_percentage:.3g}% of the total time."
        )
        print(f"{self.average_deaths:.3g} patient(s) died!")
        print(f"{self.average_accidents:.3g} accident(s) occurred!")


    def __add__(self, dm: "DataManager"):
        new_dm = DataManager(self.sim_time + dm.sim_time, self.sim_count + dm.sim_count)
        new_dm.waiting = self.waiting + dm.waiting
        new_dm.throughput_time = self.throughput_time + dm.throughput_time
        new_dm.hospital_throughput_time = self.hospital_throughput_time + dm.hospital_throughput_time
        new_dm.patients_cleared = self.patients_cleared + dm.patients_cleared
        new_dm.accidents = self.accidents + dm.accidents
        new_dm.deaths = self.deaths + dm.deaths
        return new_dm
    
    @property
    def average_patients_cleared(self):
        return float(self.patients_cleared) / self.sim_count

    @property
    def average_waiting(self):
        return float(self.waiting) / self.sim_count
    
    @property
    def average_deaths(self):
        return float(self.deaths) / self.sim_count
    
    @property
    def average_accidents(self):
        return float(self.accidents) / self.sim_count

    @property
    def average_throughput_time(self):
        return (
            self.throughput_time / self.patients_cleared
            if self.patients_cleared != 0
            else 0
        )

    @property
    def average_throughput_time_in_hospital(self):
        return (
            self.hospital_throughput_time / self.patients_cleared
            if self.patients_cleared != 0
            else 0
        )

    @property
    def waiting_percentage(self):
        return 100 * self.waiting / (self.sim_time + self.sim_count)
