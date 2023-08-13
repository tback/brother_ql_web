from _typeshed import Incomplete
from brother_ql.helpers import ElementsManager as ElementsManager

class Model:
    identifier: Incomplete
    min_max_length_dots: Incomplete
    min_max_feed: Incomplete
    number_bytes_per_row: Incomplete
    additional_offset_r: Incomplete
    mode_setting: Incomplete
    cutting: Incomplete
    expanded_mode: Incomplete
    compression: Incomplete
    two_color: Incomplete
    @property
    def name(self): ...
    def __init__(
        self,
        identifier,
        min_max_length_dots,
        min_max_feed,
        number_bytes_per_row,
        additional_offset_r,
        mode_setting,
        cutting,
        expanded_mode,
        compression,
        two_color,
    ) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

ALL_MODELS: Incomplete

class ModelsManager(ElementsManager):
    DEFAULT_ELEMENTS: Incomplete
    ELEMENTS_NAME: str
