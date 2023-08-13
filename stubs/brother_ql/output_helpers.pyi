from _typeshed import Incomplete
from brother_ql.devicedependent import (
    DIE_CUT_LABEL as DIE_CUT_LABEL,
    ENDLESS_LABEL as ENDLESS_LABEL,
    ROUND_DIE_CUT_LABEL as ROUND_DIE_CUT_LABEL,
    label_type_specs as label_type_specs,
)

logger: Incomplete

def textual_label_description(labels_to_include): ...
def log_discovered_devices(available_devices, level=...) -> None: ...
def textual_description_discovered_devices(available_devices): ...
