import logging
import sys


def _create_logger() -> logging.Logger:
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt="%(asctime)s : %(levelname)s : %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
    handler.setFormatter(formatter)

    _logger = logging.getLogger(__file__)
    _logger.addHandler(handler)
    return _logger


logger = _create_logger()
