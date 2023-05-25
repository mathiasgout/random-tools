import logging
import os
import time
from pathlib import Path

from typing import Union


def get_logger(
    logger_name: str, stream: bool = True, file_path: Union[str, None] = None
) -> logging.Logger:
    """Create a logger

    Args:
        logger_name (str): logger name
        stream (bool, optional): to add a StreamHandler. Defaults to True.
        file_path (Union[str, None], optional): path of file for the FileHandler. Defaults to None.

    Returns:
        logging.Logger: the logger
    """
    # Création du logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Modification du niveau de criticité du logger

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
        logger.addHandler(stream_handler)

    if file_path:
        # Create log folder
        FOLDER_PATH = os.path.dirname(os.path.realpath(file_path))
        Path(FOLDER_PATH).mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)  # Liaison le formatteur au handler
        logger.addHandler(file_handler)

    return logger
