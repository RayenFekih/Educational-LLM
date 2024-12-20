from core.agents import ingest_pdf, rag_agent
from core.prompts import question_prompt_template, summary_prompt_template
from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    """
    Endpoint to ingest a PDF file and process its content.

    Parameters:
        file (UploadFile): The PDF file to be ingested.

    Returns:
        PlainTextResponse: A response indicating the success of the PDF ingestion and processing.
    """
    return await ingest_pdf(file)


@router.post("/generate/questions")
async def generate_questions_endpoint(topic: str = Form(...), num_questions: int = Form(...)):
    """
    Endpoint to generate educational questions based on a given topic using a RAG approach.

    Parameters:
        topic (str): The subject matter for which questions are to be generated.
        num_questions (int): The total number of questions to create.

    Returns:
        PlainTextResponse: A response containing the generated questions.
    """
    return await rag_agent(topic, question_prompt_template, num_questions=num_questions)


@router.post("/generate/summary")
async def generate_summary_endpoint(topic: str = Form(...)):
    """
    Endpoint to generate a summary for a given topic using a RAG approach.

    Parameters:
        topic (str): The topic to summarize, provided as form data.

    Returns:
        PlainTextResponse: A response containing the generated summary.
    """
    return await rag_agent(topic, summary_prompt_template)
