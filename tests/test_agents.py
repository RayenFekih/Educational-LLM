
import pytest
from fastapi import HTTPException

from app.core.agents import ingest_pdf, rag_agent


class TestIngestPdf:

    # Handles FileNotFoundError when the file is not found after saving
    @pytest.mark.asyncio
    async def test_file_not_found_error_handling(self, mocker):
        mock_file = mocker.Mock()
        mock_file.filename = "test.pdf"
        mock_file.read = mocker.AsyncMock(return_value=b"PDF content")

        mocker.patch("os.path.exists", return_value=False)

        # Call the function and assert HTTPException is raised
        with pytest.raises(HTTPException) as excinfo:
            await ingest_pdf(mock_file)

        # Assert the exception details
        assert excinfo.value.status_code == 400
        assert "The file ./test.pdf is not found." in str(excinfo.value.detail)

    # Manages exceptions when the PDF loading or processing fails
    @pytest.mark.asyncio
    async def test_pdf_loading_failure(self, mocker):
        mock_file = mocker.Mock()
        mock_file.filename = "test.pdf"
        mock_file.read = mocker.AsyncMock(return_value=b"PDF content")

        mocker.patch("os.path.exists", return_value=True)

        # Mock PyPDFLoader to raise an exception
        mocker.patch("langchain.document_loaders.PyPDFLoader.load",
                     side_effect=Exception("Loading error"))

        # Call the function and assert exception
        with pytest.raises(HTTPException) as excinfo:
            await ingest_pdf(mock_file)

        assert excinfo.value.status_code == 500
        assert "An error occurred: Loading error" in str(excinfo.value.detail)


class TestRagAgent:

    # Raises an error if the vector store is empty
    @pytest.mark.asyncio
    async def test_error_on_empty_vectorstore(self, mocker):
        mock_vectorstore = mocker.patch('app.core.utils.vectorstore')
        mock_vectorstore.value = None

        mock_prompt_template = mocker.Mock()

        with pytest.raises(AttributeError, match="Vector store is empty. Please ingest a PDF first."):
            await rag_agent("test_topic", mock_prompt_template)
