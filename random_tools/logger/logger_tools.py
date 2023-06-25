import os
import time
import logging
from logging.handlers import WatchedFileHandler
from pathlib import Path
from typing import Optional


def get_loggers(
    logger_names: list[str],
    level: str = "DEBUG",
    stream: bool = True,
    file_path: Optional[str] = None,
) -> list[logging.Logger]:
    """Create logger(s)

    Args:
        logger_names (list[str]): list of logger names
        level (str): loggers level. Defaults to DEBUG
        stream (bool, optional): to add a StreamHandler. Defaults to True.
        file_path (Union[str, None], optional): path of file for the FileHandler. Defaults to None.

    Returns:
        list[logging.Logger]: list of loggers
    """
    # Création du logger
    loggers = []
    for logger_name in logger_names:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)  # Modification du niveau de criticité du logger
        loggers.append(logger)

    # Création d'un formatteur
    logging.Formatter.converter = time.gmtime
    formatter = logging.Formatter(
        "{"
        '"time":"%(asctime)s",'
        '"level":"%(levelname)s",'
        '"logger_name":"%(name)s",'
        '"file_name":"%(filename)s",'
        '"function_name":"%(funcName)s",'
        '"message":"%(message)s"'
        "}"
    )

    if stream:
        # Création d'un StreamHandler pour afficher la log dans la console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)  # Liaison le formatteur au handler
        for logger in loggers:
            logger.addHandler(stream_handler)

    if file_path:
        # Create log folder
        FOLDER_PATH = os.path.dirname(os.path.realpath(file_path))
        Path(FOLDER_PATH).mkdir(parents=True, exist_ok=True)

        file_handler = WatchedFileHandler(file_path)
        file_handler.setFormatter(formatter)  # Liaison le formatteur au handler
        for logger in loggers:
            logger.addHandler(file_handler)

    return loggers
