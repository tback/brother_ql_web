import logging
from unittest import TestCase  # noqa: F401


def patch_deprecation_warning():
    """
    Avoid the deprecation warning from `brother_ql.devicedependent`. This has been
    fixed in the Git version, but not in PyPI one:
    https://github.com/pklaus/brother_ql/commit/5c2b72b18bcf436c116f180a9147cbb6805958f5
    """
    original_logger = logging.getLogger("brother_ql.devicedependent").warning

    def warn(message, *args, **kwargs):
        if (
            message
            == "deprecation warning: brother_ql.devicedependent is deprecated and will be removed in a future release"  # noqa: E501
        ):
            return
        original_logger(message, *args, **kwargs)

    logging.getLogger("brother_ql.devicedependent").warn = warn


patch_deprecation_warning()
