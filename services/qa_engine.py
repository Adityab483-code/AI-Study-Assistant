from services.pdf_reader import (
    extract_pages
)

from services.rag_engine import (
    create_chunks,
    create_vector_store,
    retrieve_context
)

from services.web_search import (
    web_search
)

from utils.llm import (
    generate_response
)


def answer_question(
    pdf_file,
    question,
    search_mode
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

        print(
            "MODE:",
            search_mode
        )

        if search_mode == "🌐 Web Only":

            results = web_search(
                question
            )

            web_context = "\n".join(
                [
                    f"{item['title']}\n{item['body']}"
                    for item in results
                ]
            )

            prompt = f"""
Answer the question using the web search results.

QUESTION:
{question}

WEB RESULTS:
{web_context}
"""

            return generate_response(
                prompt
            )

        prompt = f"""
Answer ONLY from the context.

If answer is unavailable,
say exactly:

Information not found in notes.

CONTEXT:
{context}

QUESTION:
{question}
"""

        answer = generate_response(
            prompt
        )

        if search_mode == "🚀 Hybrid":

            if (
                "information not found" in answer.lower()
                or "not available" in answer.lower()
                or "not present" in answer.lower()
            ):

                results = web_search(
                    question
                )

                web_context = "\n".join(
                    [
                        f"{item['title']}\n{item['body']}"
                        for item in results
                    ]
                )

                web_prompt = f"""
Answer the question using the web search results.

QUESTION:
{question}

WEB RESULTS:
{web_context}
"""

                return generate_response(
                    web_prompt
                )

        return answer

    except Exception as e:

        return f"Error: {e}"