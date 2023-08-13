import logging
from pathlib import Path

import bottle
from brother_ql_web.configuration import Configuration
from brother_ql_web.labels import (
    LabelParameters,
    create_label_image,
    image_to_png_bytes,
    generate_label,
    print_label,
)


logger = logging.getLogger(__name__)
del logging

CURRENT_DIRECTORY = Path(__file__).parent


def get_config(key: str) -> object:
    return bottle.request.app.config[key]


@bottle.route("/")
def index():
    bottle.redirect("/labeldesigner")


@bottle.route("/static/<filename:path>")
def serve_static(filename):
    return bottle.static_file(filename, root=CURRENT_DIRECTORY / "static")


@bottle.route("/labeldesigner")
@bottle.jinja2_view("labeldesigner.jinja2")
def labeldesigner():
    fonts = get_config("brother_ql_web.fonts")
    font_family_names = sorted(list(fonts.keys()))
    return {
        "font_family_names": font_family_names,
        "fonts": fonts,
        "label_sizes": get_config("brother_ql_web.label_sizes"),
        "website": get_config("brother_ql_web.configuration").website,
        "label": get_config("brother_ql_web.configuration").label,
        "default_orientation": get_config(
            "brother_ql_web.configuration"
        ).label.default_orientation,
    }


def get_label_parameters(request):
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


@bottle.get("/api/preview/text")
@bottle.post("/api/preview/text")
def get_preview_image():
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


@bottle.post("/api/print/text")
@bottle.get("/api/print/text")
def print_text():
    """
    API to print a label

    returns: JSON
    """
    return_dict = {"success": False}

    try:
        parameters = get_label_parameters(bottle.request)
    except LookupError as e:
        return_dict["error"] = e.msg
        return return_dict

    if parameters.text is None:
        return_dict["error"] = "Please provide the text for the label"
        return return_dict

    qlr = generate_label(
        parameters=parameters,
        configuration=get_config("brother_ql_web.configuration"),
        save_image_to="sample-out.png" if bottle.DEBUG else None,
    )

    if not bottle.DEBUG:
        try:
            print_label(
                parameters=parameters,
                qlr=qlr,
                configuration=get_config("brother_ql_web.configuration"),
                backend_class=get_config("brother_ql_web.backend_class"),
            )
        except Exception as e:
            return_dict["message"] = str(e)
            logger.warning("Exception happened: %s", e)
            return return_dict

    return_dict["success"] = True
    if bottle.DEBUG:
        return_dict["data"] = str(qlr.data)
    return return_dict


def main(configuration: Configuration, fonts, label_sizes, backend_class):
    app = bottle.default_app()
    app.config["brother_ql_web.configuration"] = configuration
    app.config["brother_ql_web.fonts"] = fonts
    app.config["brother_ql_web.label_sizes"] = label_sizes
    app.config["brother_ql_web.backend_class"] = backend_class
    bottle.TEMPLATE_PATH.append(CURRENT_DIRECTORY / "views")
    debug = configuration.server.is_in_debug_mode
    app.run(host=configuration.server.host, port=configuration.server.port, debug=debug)
