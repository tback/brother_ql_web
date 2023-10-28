from .generic import BrotherQLBackendGeneric as BrotherQLBackendGeneric
from _typeshed import Incomplete

available_backends: Incomplete

def guess_backend(identifier: str) -> str: ...
def backend_factory(
    backend_name: str,
) -> dict[str, list[str] | BrotherQLBackendGeneric]: ...
