from random_tools.logger import logger_tools

import logging


def test_get_logger_TYPE():
    loggers = logger_tools.get_loggers(logger_names=["logger_name"])
    assert type(loggers) == list    
    assert type(loggers[0]) == logging.Logger