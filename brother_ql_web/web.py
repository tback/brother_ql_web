from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, cast

import bottle
from brother_ql_web.configuration import Configuration
from brother_ql_web.labels import (
    LabelParameters,
    create_label_image,
    image_to_png_bytes,
    generate_label,
    print_label,
)
from brother_ql_web.utils import BACKEND_TYPE


logger = logging.getLogger(__name__)
del logging

CURRENT_DIRECTORY = Path(__file__).parent


def get_config(key: str) -> object:
    return bottle.request.app.config[key]


@bottle.route("/")  # type: ignore[misc]
def index() -> None:
    bottle.redirect("/labeldesigner")


@bottle.route("/static/<filename:path>")  # type: ignore[misc]
def serve_static(filename: str) -> bottle.HTTPResponse:
    return bottle.static_file(filename, root=str(CURRENT_DIRECTORY / "static"))


@bottle.route("/labeldesigner")  # type: ignore[misc]
@bottle.jinja2_view("labeldesigner.jinja2")  # type: ignore[misc]
def labeldesigner() -> dict[str, Any]:
    fonts = cast(dict[str, dict[str, str]], get_config("brother_ql_web.fonts"))
    font_family_names = sorted(list(fonts.keys()))
    configuration = cast(Configuration, get_config("brother_ql_web.configuration"))
    return {
        "font_family_names": font_family_names,
        "fonts": fonts,
        "label_sizes": get_config("brother_ql_web.label_sizes"),
        "website": configuration.website,
        "label": configuration.label,
        "default_orientation": configuration.label.default_orientation,
    }


def get_label_parameters(request: bottle.BaseRequest) -> LabelParameters:
    """
    Might raise LookupError()
    """
    d = request.params.decode()  # UTF-8 decoded form data

    font_family = d.get("font_family").rpartition("(")[0].strip()
    font_style = d.get("font_family").rpartition("(")[2].rstrip(")")
    context = {
        "text": d.get("text", ""),
        "font_size": int(d.get("font_size", 100)),
        "font_family": font_family,
        "font_style": font_style,
        "label_size": d.get("label_size", "62"),
        "margin": int(d.get("margin", 10)),
        "threshold": int(d.get("threshold", 70)),
        "align": d.get("align", "center"),
        "orientation": d.get("orientation", "standard"),
        "margin_top": int(d.get("margin_top", 24)),
        "margin_bottom": int(d.get("margin_bottom", 45)),
        "margin_left": int(d.get("margin_left", 35)),
        "margin_right": int(d.get("margin_right", 35)),
        "label_count": int(d.get("label_count", 1)),
        "high_quality": bool(d.get("high_quality", True)),
        "configuration": request.app.config["brother_ql_web.configuration"],
    }

    return LabelParameters(**context)


@bottle.get("/api/preview/text")  # type: ignore[misc]
@bottle.post("/api/preview/text")  # type: ignore[misc]
def get_preview_image() -> bytes:
    parameters = get_label_parameters(bottle.request)
    image = create_label_image(parameters=parameters)
    return_format = bottle.request.query.get("return_format", "png")
    if return_format == "base64":
        import base64

        bottle.response.set_header("Content-type", "text/plain")
        return base64.b64encode(image_to_png_bytes(image))
    else:
        bottle.response.set_header("Content-type", "image/png")
        return image_to_png_bytes(image)


@bottle.post("/api/print/text")  # type: ignore[misc]
@bottle.get("/api/print/text")  # type: ignore[misc]
def print_text() -> dict[str, bool | str]:
    """
    API to print a label

    returns: JSON
    """
    return_dict: dict[str, bool | str] = {"success": False}

    try:
        parameters = get_label_parameters(bottle.request)
    except LookupError as e:
        return_dict["error"] = str(e)
        return return_dict

    if parameters.text is None:
        return_dict["error"] = "Please provide the text for the label"
        return return_dict

    qlr = generate_label(
        parameters=parameters,
        configuration=cast(Configuration, get_config("brother_ql_web.configuration")),
        save_image_to="sample-out.png" if bottle.DEBUG else None,
    )

    if not bottle.DEBUG:
        try:
            print_label(
                parameters=parameters,
                qlr=qlr,
                configuration=cast(
                    Configuration, get_config("brother_ql_web.configuration")
                ),
                backend_class=cast(
                    BACKEND_TYPE,
                    get_config("brother_ql_web.backend_class"),
                ),
            )
        except Exception as e:
            return_dict["message"] = str(e)
            logger.warning("Exception happened: %s", e)
            return return_dict

    return_dict["success"] = True
    if bottle.DEBUG:
        return_dict["data"] = str(qlr.data)
    return return_dict


def main(
    configuration: Configuration,
    fonts: dict[str, dict[str, str]],
    label_sizes: list[tuple[str, str]],
    backend_class: BACKEND_TYPE,
) -> None:
    app = bottle.default_app()
    app.config["brother_ql_web.configuration"] = configuration
    app.config["brother_ql_web.fonts"] = fonts
    app.config["brother_ql_web.label_sizes"] = label_sizes
    app.config["brother_ql_web.backend_class"] = backend_class
    bottle.TEMPLATE_PATH.append(CURRENT_DIRECTORY / "views")
    debug = configuration.server.is_in_debug_mode
    app.run(host=configuration.server.host, port=configuration.server.port, debug=debug)
