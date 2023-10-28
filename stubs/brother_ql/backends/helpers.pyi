from _typeshed import Incomplete
from brother_ql.backends import (
    backend_factory as backend_factory,
    guess_backend as guess_backend,
)
from brother_ql.reader import interpret_response as interpret_response

logger: Incomplete

def discover(backend_identifier: str = ...) -> list[str]: ...
def send(
    instructions: bytes,
    printer_identifier: Incomplete | None = ...,
    backend_identifier: Incomplete | None = ...,
    blocking: bool = ...,
): ...
