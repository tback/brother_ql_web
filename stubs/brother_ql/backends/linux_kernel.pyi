from .generic import BrotherQLBackendGeneric as BrotherQLBackendGeneric
from _typeshed import Incomplete

def list_available_devices() -> list[dict[str, str | None]]: ...

class BrotherQLBackendLinuxKernel(BrotherQLBackendGeneric):
    read_timeout: float
    strategy: str
    dev: Incomplete
    write_dev: Incomplete
    read_dev: Incomplete
    def __init__(self, device_specifier: str) -> None: ...
