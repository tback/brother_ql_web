from brother_ql.helpers import ElementsManager as ElementsManager
from enum import IntEnum

class FormFactor(IntEnum):
    DIE_CUT: int
    ENDLESS: int
    ROUND_DIE_CUT: int
    PTOUCH_ENDLESS: int

class Color(IntEnum):
    BLACK_WHITE: int
    BLACK_RED_WHITE: int

class Label:
    identifier: str
    tape_size: tuple[int, int]
    form_factor: FormFactor
    dots_total: tuple[int, int]
    dots_printable: tuple[int, int]
    offset_r: int
    feed_margin: int
    restricted_to_models: list[str]
    color: Color
    def works_with_model(self, model: str) -> bool: ...
    @property
    def name(self) -> str: ...
    def __init__(
        self,
        identifier,
        tape_size,
        form_factor,
        dots_total,
        dots_printable,
        offset_r,
        feed_margin,
        restricted_to_models,
        color,
    ) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

ALL_LABELS: tuple[Label]

class LabelsManager(ElementsManager):
    DEFAULT_ELEMENTS: tuple[Label]
    ELEMENT_NAME: str
