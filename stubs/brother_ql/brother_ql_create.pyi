from _typeshed import Incomplete
from brother_ql.conversion import convert as convert
from brother_ql.devicedependent import label_type_specs as label_type_specs
from brother_ql.raster import BrotherQLRaster as BrotherQLRaster

stdout: Incomplete
logger: Incomplete

def main(): ...
def create_label(
    qlr,
    image,
    label_size,
    threshold: int = ...,
    cut: bool = ...,
    dither: bool = ...,
    compress: bool = ...,
    red: bool = ...,
    **kwargs
) -> None: ...
