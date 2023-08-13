from _typeshed import Incomplete
from collections.abc import Generator

logger: Incomplete
OPCODES: Incomplete
dot_widths: Incomplete
RESP_ERROR_INFORMATION_1_DEF: Incomplete
RESP_ERROR_INFORMATION_2_DEF: Incomplete
RESP_MEDIA_TYPES: Incomplete
RESP_STATUS_TYPES: Incomplete
RESP_PHASE_TYPES: Incomplete
RESP_BYTE_NAMES: Incomplete

def hex_format(data): ...
def chunker(data, raise_exception: bool = ...) -> Generator[Incomplete, None, None]: ...
def match_opcode(data): ...
def interpret_response(data): ...
def merge_specific_instructions(
    chunks, join_preamble: bool = ..., join_raster: bool = ...
): ...

class BrotherQLReader:
    DEFAULT_FILENAME_FMT: str
    brother_file: Incomplete
    raster_no: Incomplete
    black_rows: Incomplete
    red_rows: Incomplete
    compression: bool
    page_counter: int
    two_color_printing: bool
    cut_at_end: bool
    high_resolution_printing: bool
    filename_fmt: Incomplete
    def __init__(self, brother_file) -> None: ...
    mwidth: Incomplete
    mlength: Incomplete
    def analyse(self): ...
