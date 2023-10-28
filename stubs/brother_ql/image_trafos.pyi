from PIL import Image

def filtered_hsv(
    im: Image.Image,
    filter_h: int,
    filter_s: int,
    filter_v: int,
    default_col: tuple[int, int, int] = ...,
) -> Image.Image: ...
