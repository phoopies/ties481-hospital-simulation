from HospitalUnit import HospitalUnit
from OperationUnit import OperationUnit


class Hospital:
    """A hospital has a limited number of facilities to accommodate patients.

    patients have to request one of the facilities in order. When they get to
    one, they can start the process and wait for it to finish. After finishing
    they can continue to the next step
    """

    def __init__(
        self,
        preparation_unit: HospitalUnit,
        operation_unit: OperationUnit,
        recovery_unit: HospitalUnit,
    ) -> None:
        self.preparation = preparation_unit
        self.operation = operation_unit
        self.recovery = recovery_unit
