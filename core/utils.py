from core.config import vectorstore


def retrieve_docs(topic: str, k: int = 5, vectorstore=vectorstore) -> str:
    """
    Retrieve and return concatenated content of documents related to a given topic.

    Parameters:
        topic (str): The topic to search for in the vector store.
        k (int, optional): The number of similar documents to retrieve. Defaults to 5.

    Returns:
        str: Concatenated content of the retrieved documents.

    Raises:
        AttributeError: If the vector store is empty.
    """
    if not vectorstore.value:
        raise AttributeError(
            "Vector store is empty. Please ingest a PDF first.")

    retrieved_docs = vectorstore.value.similarity_search(topic, k=k)
    retrieved_content = " ".join([doc.page_content for doc in retrieved_docs])

    return retrieved_content
