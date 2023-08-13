from .generic import BrotherQLBackendGeneric as BrotherQLBackendGeneric
from _typeshed import Incomplete

def list_available_devices(): ...

class BrotherQLBackendPyUSB(BrotherQLBackendGeneric):
    dev: Incomplete
    read_timeout: float
    write_timeout: float
    strategy: str
    was_kernel_driver_active: bool
    write_dev: Incomplete
    read_dev: Incomplete
    def __init__(self, device_specifier) -> None: ...
