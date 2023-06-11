import logging
from typing import Union

import firebase_admin
from firebase_admin import credentials


logger = logging.getLogger(__name__)


def init_firebase_app(credentials_file_path: Union[None, str] = None) -> None:
    """Initialisation of Firebase app"""
    try:
        cred = credentials.Certificate(credentials_file_path)
    except (FileNotFoundError, ValueError):
        logger.info("[Firebase App initialized] (credentials=default)")
        firebase_admin.initialize_app()
    else:
        logger.info("[Firebase App initialized] (credentials=file)")
        firebase_admin.initialize_app(cred)
