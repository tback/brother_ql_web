from .generic import BrotherQLBackendGeneric as BrotherQLBackendGeneric
from _typeshed import Incomplete

available_backends: Incomplete

def guess_backend(identifier): ...
def backend_factory(backend_name): ...
