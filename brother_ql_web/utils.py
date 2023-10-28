from __future__ import annotations

from typing import cast

from brother_ql.backends import backend_factory, BrotherQLBackendGeneric, guess_backend
from brother_ql.devicedependent import label_type_specs, label_sizes
from brother_ql_web.configuration import Configuration
from brother_ql_web.font_helpers import get_fonts


def collect_fonts(configuration: Configuration) -> dict[str, dict[str, str]]:
    fonts = get_fonts()
    if configuration.server.additional_font_folder:
        fonts.update(get_fonts(configuration.server.additional_font_folder))
    return fonts


def get_label_sizes() -> list[tuple[str, str]]:
    return [(name, cast(str, label_type_specs[name]["name"])) for name in label_sizes]


class BackendGuessingError(ValueError):
    pass


def get_backend_class(configuration: Configuration) -> type[BrotherQLBackendGeneric]:
    try:
        selected_backend = guess_backend(configuration.printer.printer)
    except ValueError:
        raise BackendGuessingError(
            "Couln't guess the backend to use from the printer string descriptor"
        )
    return cast(
        type[BrotherQLBackendGeneric],
        backend_factory(selected_backend)["backend_class"],
    )
