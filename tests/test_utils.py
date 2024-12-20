import pytest

from app.core.utils import retrieve_docs


class TestRetrieveDocs:

    # Retrieve documents when vectorstore is populated
    def test_retrieve_docs_when_vectorstore_populated(self, mocker):
        mock_vectorstore = mocker.patch('app.core.config.vectorstore')
        mock_vectorstore.value.similarity_search.return_value = [
            mocker.Mock(page_content="Document 1 content"),
            mocker.Mock(page_content="Document 2 content")
        ]
        result = retrieve_docs("test_topic", k=2, vectorstore=mock_vectorstore)
        assert result == "Document 1 content Document 2 content"

    # Default to retrieving 5 documents when 'k' is not specified
    def test_default_retrieve_5_docs(self, mocker):
        mock_vectorstore = mocker.patch('app.core.config.vectorstore')
        mock_vectorstore.value.similarity_search.return_value = [
            mocker.Mock(page_content=f"Document {i} content") for i in range(1, 6)
        ]
        result = retrieve_docs("test_topic", vectorstore=mock_vectorstore)
        expected_content = " ".join(-
            f"Document {i} content" for i in range(1, 6))
        assert result == expected_content

    # Raises AttributeError when vectorstore is empty

    def test_retrieve_docs_empty_vectorstore(self, mocker):
        mock_vectorstore = mocker.patch('app.core.config.vectorstore')
        mock_vectorstore.value = None

        with pytest.raises(AttributeError, match="Vector store is empty. Please ingest a PDF first."):
            retrieve_docs("test_topic")
