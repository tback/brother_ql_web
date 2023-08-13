import logging
from unittest import TestCase  # noqa: F401


def patch_deprecation_warning():
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
