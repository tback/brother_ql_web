from _typeshed import Incomplete
from brother_ql.backends import (
    backend_factory as backend_factory,
    guess_backend as guess_backend,
)
from brother_ql.reader import (
    OPCODES as OPCODES,
    chunker as chunker,
    hex_format as hex_format,
    interpret_response as interpret_response,
    match_opcode as match_opcode,
    merge_specific_instructions as merge_specific_instructions,
)
from pprint import pformat as pformat, pprint as pprint

logger: Incomplete

class BrotherQL_USBdebug:
    be: Incomplete
    sleep_time: float
    sleep_before_read: float
    continue_reading_for: float
    start: Incomplete
    interactive: bool
    merge_specific_instructions: bool
    instructions_data: Incomplete
    def __init__(self, dev, instructions_data, backend: str = ...) -> None: ...
    def continue_reading(self, seconds: float = ...) -> None: ...
    def log_interp_response(self, data) -> None: ...
    def print_and_debug(self) -> None: ...

def main() -> None: ...
