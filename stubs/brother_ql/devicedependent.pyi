import logging
from brother_ql.labels import FormFactor

logger: logging.Logger
DIE_CUT_LABEL: FormFactor
ENDLESS_LABEL: FormFactor
ROUND_DIE_CUT_LABEL: FormFactor
PTOUCH_ENDLESS_LABEL: FormFactor
label_type_specs: dict[str, dict[str, str | int | tuple[int, int]]]
label_sizes: list[str]
models: list[str]
min_max_length_dots: dict[str, tuple[int, int]]
min_max_feed: dict[str, tuple[int, int]]
number_bytes_per_row: dict[str, int]
right_margin_addition: dict[str, int]
modesetting: dict[str, bool]
cuttingsupport: dict[str, bool]
expandedmode: dict[str, bool]
compressionsupport: dict[str, bool]
two_color_support: dict[str, bool]
