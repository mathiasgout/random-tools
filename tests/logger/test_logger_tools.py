from random_tools.logger import logger_tools

import logging


def test_get_logger_TYPE():
    logger = logger_tools.get_logger(logger_name="logger_name")
    assert type(logger) == logging.Logger