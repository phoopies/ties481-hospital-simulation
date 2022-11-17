import simpy
from Hospital import Hospital
from DataManager import DataManager
from HospitalUnit import WaitData, ProcessData
from HospitalData import HospitalData


class Patient:
    def __init__(self, env: simpy.Environment, name: str) -> None:
        self.env = env
        self.name = name
        self.data = (  # This data could be used for something but will not be for the time being
            HospitalData()
        )

    def go_through(
        self, hospital: Hospital, dm: DataManager, verbose: bool = False
    ) -> None:
        """the patient process: Patient arrives at the hospital
        and goes through the ``hospital`` processes
        """
        start_time = self.env.now
        if verbose:
            print(f"{self.name} arrives at the hospital at {self.env.now:.3g}")

        # Entrance queue length when the patient arrives at the hospital.
        entrance_queue_length = len(hospital.preparation.resource.queue)
        dm.entrance_queue.append(entrance_queue_length)

        prep_wd: WaitData = yield self.env.process(hospital.preparation.wait_for())
        self.data.preparation_queue_time = prep_wd.wait_time
        start_time_hospital = self.env.now

        if verbose:
            print(
                f"{self.name} waited for preparation room for {prep_wd.wait_time:.3g} minutes"
            )
        if verbose:
            print(f"{self.name} enters preparation at {self.env.now:.3g}")
        prep_pd: ProcessData = yield self.env.process(hospital.preparation.process())
        self.data.preparation_time = prep_pd.process_time
        if verbose:
            print(f"{self.name} finishes preparation at {self.env.now:.3g}")

        oper_wd: WaitData = yield self.env.process(hospital.operation.wait_for())
        self.data.operation_queue_time = oper_wd.wait_time
        hospital.preparation.release(prep_wd.request)

        if verbose:
            print(
                f"{self.name} leaves preparation and enters operation at {self.env.now:.3g}"
            )

        if oper_wd.wait_time and verbose:
            print(f"{self.name} waited for an operation for {oper_wd.wait_time}")

        oper_pd: ProcessData = yield self.env.process(hospital.operation.process())
        self.data.operation_time = oper_pd.process_time

        if not oper_pd.success:  # Patient died
            if verbose:
                print(f"{self.name} died in operation at {self.env.now}")
            hospital.operation.release(oper_wd.request)
            dm.deaths += 1
        else:
            if verbose:
                print("%s finishes operation at %.2f." % (self.name, self.env.now))

            rec_wd: WaitData = yield self.env.process(hospital.recovery.wait_for())
            self.data.recovery_queue_time = rec_wd.wait_time
            hospital.operation.release(oper_wd.request)

            if verbose:
                print(
                    f"{self.name} leaves operation and enters recovery at  {self.env.now:.3g}"
                )
            if rec_wd.wait_time:
                if verbose:
                    print(
                        f"{self.name} waited for an recovery room in operation for {rec_wd.wait_time:.3g} minutes"
                    )
                dm.waiting += rec_wd.wait_time

            rec_pd: ProcessData = yield self.env.process(hospital.recovery.process())
            self.data.recovery_time = rec_pd.process_time
            hospital.recovery.release(rec_wd.request)

            if verbose:
                print(f"{self.name} finishes and leaves recovery at {self.env.now:.3g}")

        # Collect more data
        total_time = self.env.now - start_time
        total_time_in_hospital = self.env.now - start_time_hospital

        dm.throughput_time += total_time
        dm.hospital_throughput_time += total_time_in_hospital
        dm.patients_cleared += 1

        if verbose:
            print(
                f"{self.name} was in hospital for {dm.hospital_throughput_time:.3g} minutes"
            )
