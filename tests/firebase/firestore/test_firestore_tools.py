from random_tools.firebase.firestore import firestore_tools

from unittest.mock import call, Mock

import firebase_admin
import pytest


def test_get_client_firestore(mocker):
    class FirestoreClient:
        pass

    # Patchs
    mocker.patch(
        "firebase_admin.firestore.client", return_value=Mock(spec=FirestoreClient)
    )
    # Le type de ce que retourne la fonction 'firebase_admin.firestore.client' est 'FirestoreClient'

    # Calls
    client = firestore_tools.get_client_firestore()

    # Verifications
    assert isinstance(client, FirestoreClient)


def test_get_document_EXISTING_DOCUMENT(mocker):
    # Patchs
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")
    mock_firestore_client.return_value.collection.return_value.document.return_value.get.return_value.to_dict.return_value = {
        "field1": "field_1"
    }

    # Calls
    document = firestore_tools.get_document(
        collection_name="collection_name", document_name="document_name"
    )

    # Verifications
    calls = [
        call(),
        call().collection("collection_name"),
        call().collection().document("document_name"),
        call().collection().document().get(),
    ]
    firebase_admin.firestore.client.assert_has_calls(calls)
    assert document == {"field1": "field_1"}


def test_get_document_NO_EXISTING_DOCUMENT(mocker):
    # Patchs
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")
    mock_firestore_client.return_value.collection.return_value.document.return_value.get.return_value.exists = (
        False
    )

    # Calls
    document = firestore_tools.get_document(
        collection_name="collection_name", document_name="document_name"
    )

    # Verifications
    calls = [
        call(),
        call().collection("collection_name"),
        call().collection().document("document_name"),
        call().collection().document().get(),
    ]
    firebase_admin.firestore.client.assert_has_calls(calls)
    assert document is None


def test_get_documents_CONDITION(mocker):
    class MyDoc:
        def __init__(self, a):
            self.a = a

        def to_dict(self):
            return {"a": self.a}

    # Patchs
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")
    mock_firestore_client.return_value.collection.return_value.where.return_value.stream.return_value = iter(
        [MyDoc("yes"), MyDoc("no")]
    )

    # Calls
    documents = firestore_tools.get_documents(
        collection_name="collection_name", condition=["a", "in", ["yes", "no"]]
    )

    # Verifications
    calls = [
        call(),
        call().collection("collection_name"),
        call().collection().where("a", "in", ["yes", "no"]),
        call().collection().where().stream(),
    ]
    firebase_admin.firestore.client.assert_has_calls(calls)
    assert documents == [{"a": "yes"}, {"a": "no"}]


def test_get_documents_NO_CONDITION(mocker):
    class MyDoc:
        def __init__(self, a):
            self.a = a

        def to_dict(self):
            return {"a": self.a}

    # Patchs
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")
    mock_firestore_client.return_value.collection.return_value.stream.return_value = (
        iter([MyDoc("yes"), MyDoc("no")])
    )

    # Calls
    documents = firestore_tools.get_documents(collection_name="collection_name")

    # Verifications
    calls = [
        call(),
        call().collection("collection_name"),
        call().collection().stream(),
    ]
    firebase_admin.firestore.client.assert_has_calls(calls)
    assert documents == [{"a": "yes"}, {"a": "no"}]


def test_create_document_WITH_NAME(mocker):
    # Patchs
    mocker.patch("firebase_admin.firestore.client")

    # Calls
    document = firestore_tools.create_document(
        collection_name="collection_name",
        document_name="document_name",
        field1="field_1",
    )

    # Verifications
    calls = [
        call(),
        call().collection("collection_name"),
        call().collection().document("document_name"),
        call().collection().document().set({"field1": "field_1"}),
    ]
    firebase_admin.firestore.client.assert_has_calls(calls)
    assert document == {"field1": "field_1"}


def test_create_document_WITH_NAME_MERGE(mocker):
    # Patchs
    mocker.patch("firebase_admin.firestore.client")

    # Calls
    document = firestore_tools.create_document(
        collection_name="collection_name",
        document_name="document_name",
        field1="field_1",
        merge=True,
    )

    # Verifications
    calls = [
        call(),
        call().collection("collection_name"),
        call().collection().document("document_name"),
        call().collection().document().set({"field1": "field_1"}, merge=True),
    ]
    firebase_admin.firestore.client.assert_has_calls(calls)
    assert document == {"field1": "field_1"}


def test_create_document_NO_NAME(mocker):
    # Patchs
    mocker.patch("firebase_admin.firestore.client")

    # Calls
    document = firestore_tools.create_document(
        collection_name="collection_name",
        field1="field_1",
    )

    # Verifications
    calls = [
        call(),
        call().collection("collection_name"),
        call().collection().add({"field1": "field_1"}),
    ]
    firebase_admin.firestore.client.assert_has_calls(calls)
    assert document == {"field1": "field_1"}


def test_create_document_MERGE_NOT_BOOL(mocker):
    # Patchs
    mocker.patch("firebase_admin.firestore.client")

    # Verifications
    with pytest.raises(ValueError) as e:
        document = firestore_tools.create_document(
            collection_name="collection_name",
            document_name="document_name",
            field1="field_1",
            merge="dsl",
        )


def test_create_document_DOCUMENT_NAME_ERROR1(mocker):
    # Patchs
    mocker.patch("firebase_admin.firestore.client")

    # Verifications
    with pytest.raises(ValueError) as e:
        document = firestore_tools.create_document(
            collection_name="collection_name", document_name="", field1="field_1"
        )


def test_create_document_DOCUMENT_NAME_ERROR2(mocker):
    # Patchs
    mocker.patch("firebase_admin.firestore.client")

    # Verifications
    with pytest.raises(ValueError) as e:
        document = firestore_tools.create_document(
            collection_name="collection_name", document_name=1, field1="field_1"
        )


def test_delete_document(mocker):
    # Patchs
    mocker.patch("firebase_admin.firestore.client")

    # Calls
    firestore_tools.delete_document(
        collection_name="collection_name",
        document_name="document_name",
    )

    # Verifications
    calls = [
        call(),
        call().collection("collection_name"),
        call().collection().document("document_name"),
        call().collection().document().delete(),
    ]
    firebase_admin.firestore.client.assert_has_calls(calls)
