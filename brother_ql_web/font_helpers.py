from __future__ import annotations

import logging
import subprocess
from collections import defaultdict


logger = logging.getLogger(__name__)
del logging


def get_fonts(folder: str | None = None) -> dict[str, dict[str, str]]:
    """
    Scan a folder (or the system) for .ttf / .otf fonts and
    return a dictionary of the structure  family -> style -> file path
    """
    fonts: dict[str, dict[str, str]] = defaultdict(dict)
    if folder:
        cmd = ["fc-scan", "--format", "%{file}:%{family}:style=%{style}\n", folder]
    else:
        cmd = ["fc-list", ":", "file", "family", "style"]
    for line in subprocess.check_output(cmd).decode("utf-8").split("\n"):
        line = line.strip()
        if not line:
            continue
        if "otf" not in line and "ttf" not in line:
            continue
        parts = line.split(":")
        if "style=" not in line or len(parts) < 3:
            # fc-list did not output all desired properties
            logger.warning("skipping invalid font %s", line)
            continue
        path = parts[0]
        families = parts[1].strip().split(",")
        styles = parts[2].split("=")[1].split(",")
        if len(families) == 1 and len(styles) > 1:
            families = [families[0]] * len(styles)
        elif len(families) > 1 and len(styles) == 1:
            styles = [styles[0]] * len(families)
        if len(families) != len(styles):
            logger.debug("Problem with this font: %s", line)
            continue
        for i in range(len(families)):
            fonts[families[i]][styles[i]] = path
            # logger.debug("Added this font: %s", (families[i], styles[i], path))
    return dict(fonts)
