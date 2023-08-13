from .generic import BrotherQLBackendGeneric as BrotherQLBackendGeneric
from _typeshed import Incomplete

def list_available_devices(): ...

class BrotherQLBackendNetwork(BrotherQLBackendGeneric):
    read_timeout: float
    strategy: str
    s: Incomplete
    dev: Incomplete
    def __init__(self, device_specifier) -> None: ...
