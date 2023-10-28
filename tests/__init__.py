import logging
from functools import cached_property
from pathlib import Path
from unittest import TestCase as _TestCase
from typing import Any

from brother_ql_web.configuration import Configuration


def patch_deprecation_warning() -> None:
    """
    Avoid the deprecation warning from `brother_ql.devicedependent`. This has been
    fixed in the Git version, but not in PyPI one:
    https://github.com/pklaus/brother_ql/commit/5c2b72b18bcf436c116f180a9147cbb6805958f5
    """
    original_logger = logging.getLogger("brother_ql.devicedependent").warning

    def warn(message: str, *args: Any, **kwargs: Any) -> None:
        if (
            message
            == "deprecation warning: brother_ql.devicedependent is deprecated and will be removed in a future release"  # noqa: E501
        ):
            return
        original_logger(message, *args, **kwargs)

    logging.getLogger("brother_ql.devicedependent").warn = warn  # type: ignore[assignment,method-assign]  # noqa: E501


patch_deprecation_warning()


class TestCase(_TestCase):
    @cached_property
    def example_configuration_path(self) -> str:
        return str(Path(__file__).parent.parent / "config.example.json")

    @property
    def example_configuration(self) -> Configuration:
        return Configuration.from_json(self.example_configuration_path)
