import logging
from typing import Union, List

from firebase_admin import firestore


logger = logging.getLogger(__name__)


def get_client_firestore():
    """Returns a Firestore client

    Returns:
        google.cloud.firestore_v1.client.Client: Firestore client
    """
    client_firestore = firestore.client()
    return client_firestore


def get_document(collection_name: str, document_name: str) -> Union[None, dict]:
    """Get a document from the collection : collection_name (to_dict format)

    Args:
        collection_name (str): Collection name
        document_name (str): Document Name

    Returns:
        Union[None, dict]: document in dict format or None
    """
    client_firestore = get_client_firestore()
    doc_ref = client_firestore.collection(collection_name).document(document_name)
    doc = doc_ref.get()
    if doc.exists:
        logger.info(f"[Firestore READ] (path={doc_ref.path}) (exists=true) (read=1)")
        return doc.to_dict()
    logger.info(f"[Firestore READ] (path={doc_ref.path}) (exists=false) (read=1)")
    return None


def get_documents(
    collection_name: str, condition: Union[None, List[str]] = None
) -> List[dict]:
    """Get a list of documents from the collection : collection_name (to_dict format)

    Args:
        collection_name (str): Collection name
        condition (List[str]): Conditions

    Returns:
        List[dict]: List of documents in dict format
    """
    client_firestore = get_client_firestore()
    if condition:
        doc_refs = client_firestore.collection(collection_name).where(*condition)
    else:
        doc_refs = client_firestore.collection(collection_name)

    docs = doc_refs.stream()
    docs_list = []
    for doc in docs:
        docs_list.append(doc.to_dict())
    logger.info(f"[Firestore READ] (collection={collection_name}) (condition={condition}) (read={len(docs_list)})")
    return docs_list


def create_document(
    collection_name: str,
    document_name: Union[None, str] = None,
    merge: bool = False,
    **kwargs,
) -> dict:
    """Create/update a document named "document_name" in the collection "collection_name"
    Document's fields are **kwargs

    Args:
        collection_name (str): the collection name
        document_name (Union[None, str]): the document name. Default None (random token is generate as name)
        merge (bool): existing documents keys, which are not present in document_data, will preserve the values of those keys.

    Returns:
        dict: kwargs
    """
    if not isinstance(merge, bool):
        raise ValueError("'merge' must be a bool")
    if ((not isinstance(document_name, str)) and (document_name is not None)) or (
        document_name == ""
    ):
        raise ValueError("'document_name' must be a str or None")

    client_firestore = get_client_firestore()
    if document_name:
        if merge:
            client_firestore.collection(collection_name).document(document_name).set(
                kwargs, merge=True
            )
        else:
            client_firestore.collection(collection_name).document(document_name).set(
                kwargs
            )
        logger.info(f"[Firestore WRITE] (path={collection_name}/{document_name}) (fields={len(kwargs)}) (write=1)")
    else:
        client_firestore.collection(collection_name).add(kwargs)
        logger.info(f"[Firestore WRITE] (path={collection_name}/__random_token__) (fields={len(kwargs)}) (write=1)")
    return kwargs


def delete_document(collection_name: str, document_name: str) -> None:
    """Delete a document from the collection : collection_name

    Args:
        collection_name (str): collection name
        document_name (str): document name
    """
    client_firestore = get_client_firestore()
    client_firestore.collection(collection_name).document(document_name).delete()
    print(f"[Firestore DELETE] (path={collection_name}/{document_name}) (delete=1)")
