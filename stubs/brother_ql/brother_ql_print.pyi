from _typeshed import Incomplete
from brother_ql.backends import (
    available_backends as available_backends,
    backend_factory as backend_factory,
    guess_backend as guess_backend,
)
from brother_ql.backends.helpers import discover as discover, send as send
from brother_ql.output_helpers import (
    log_discovered_devices as log_discovered_devices,
    textual_description_discovered_devices as textual_description_discovered_devices,
)

logger: Incomplete

def main() -> None: ...
