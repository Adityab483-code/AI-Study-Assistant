from utils.gemini import model

from services.pdf_reader import (
    extract_pages
)

from services.rag_engine import (
    create_chunks,
    create_vector_store,
    retrieve_context
)
from utils.llm import (
    generate_response
)

def answer_question(
    pdf_file,
    question
):

    try:

        pages = extract_pages(
            pdf_file
        )

        chunks = create_chunks(
            pages
        )

        index = create_vector_store(
            chunks
        )

        context, source_pages = (
            retrieve_context(
                question,
                chunks,
                index
            )
        )

        prompt = f"""
Answer ONLY from the context.

If answer is unavailable,
say:

Information not found in notes.

CONTEXT:
{context}

QUESTION:
{question}
"""

        return generate_response(
    prompt
)

    except Exception as e:

        return f"Error: {e}"