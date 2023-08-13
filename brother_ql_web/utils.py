from brother_ql.backends import backend_factory, guess_backend
from brother_ql.devicedependent import label_type_specs, label_sizes
from brother_ql_web.font_helpers import get_fonts


def collect_fonts(configuration):
    fonts = get_fonts()
    if configuration.server.additional_font_folder:
        fonts.update(get_fonts(configuration.server.additional_font_folder))
    return fonts


def get_label_sizes():
    return [(name, label_type_specs[name]["name"]) for name in label_sizes]


class BackendGuessingError(ValueError):
    pass


def get_backend_class(configuration):
    try:
        selected_backend = guess_backend(configuration.printer.printer)
    except ValueError:
        raise BackendGuessingError(
            "Couln't guess the backend to use from the printer string descriptor"
        )
    return backend_factory(selected_backend)["backend_class"]
