import os

from core.config import LLM_model, embedding_model, vectorstore
from core.utils import retrieve_docs
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter


async def ingest_pdf(file):
    """
    Ingests a PDF file, processes its content, and updates the vector store.

    Parameters:
        file: An uploaded PDF file object.

    Returns:
        PlainTextResponse: A response indicating the PDF was uploaded and processed successfully.

    Raises:
        HTTPException: If the file is not found or another error occurs during processing.
    """

    file_location = f"./{file.filename}"
    try:

        # Load and check if file exists
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Check if the file was successfully created
        if not os.path.exists(file_location):
            raise FileNotFoundError(
                f"The file {file_location} is not found.")

        # Load and process the PDF
        loader = PyPDFLoader(file_location)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200, chunk_overlap=20)
        texts = text_splitter.split_documents(documents)

        vectorstore.value = FAISS.from_documents(texts, embedding_model)
        return PlainTextResponse(content="PDF uploaded and processed successfully.\n")

    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


async def rag_agent(topic: str, prompt_template: PromptTemplate, **kwargs) -> PlainTextResponse:
    """
    Generates a response using a Retrieval-Augmented Generation (RAG) approach.

    Parameters:
        topic (str): The topic for which documents are to be retrieved and questions generated.
        prompt_template (PromptTemplate): The template used to format the prompt for the language model.
        **kwargs: Additional keyword arguments to be passed to the question chain.

    Returns:
        PlainTextResponse: The generated questions or responses as plain text.
    """
    # Retrieve docs related to the specified topic
    retrieved_content = retrieve_docs(topic)

    # Generate questions
    question_chain = prompt_template | LLM_model | StrOutputParser()
    questions = question_chain.invoke({
        "topic": topic,
        "retrieved_content": retrieved_content,
        **kwargs
    })

    return PlainTextResponse(content=questions)
