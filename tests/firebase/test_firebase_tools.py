from random_tools.firebase import firebase_tools

import firebase_admin


def test_init_firebase_WITH_GCP_PATH(mocker):
    # Patchs
    mocker.patch("firebase_admin.initialize_app")
    mocker.patch("firebase_admin.credentials.Certificate")

    # Calls
    firebase_tools.init_firebase_app(credentials_file_path="/path/that/exist")

    # Verifications
    firebase_admin.initialize_app.assert_called_once()


def test_init_firebase_WITH_GCP_PATH_THAT_DOES_NOT_EXIST(mocker):
    # Patchs
    mocker.patch("firebase_admin.initialize_app")
    mocker.patch(
        "firebase_admin.credentials.Certificate", side_effect=FileNotFoundError
    )

    # Calls
    firebase_tools.init_firebase_app(credentials_file_path="/path/that/does/not/exist")

    # Verifications
    firebase_admin.initialize_app.assert_called_once()


def test_init_firebase_WITHOUT_GCP_PATH(mocker):
    # Patchs
    mocker.patch("firebase_admin.initialize_app")
    mocker.patch("firebase_admin.credentials.Certificate", side_effect=ValueError)

    # Calls
    firebase_tools.init_firebase_app()

    # Verifications
    firebase_admin.initialize_app.assert_called_once()
