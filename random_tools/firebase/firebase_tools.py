from typing import Union

import firebase_admin
from firebase_admin import credentials


def init_firebase_app(credentials_file_path: Union[None, str] = None) -> None:
    """Initialisation of Firebase app"""
    try:
        cred = credentials.Certificate(credentials_file_path)
    except (FileNotFoundError, ValueError):
        firebase_admin.initialize_app()
    else:
        firebase_admin.initialize_app(cred)
