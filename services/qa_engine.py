from utils.gemini import model


def answer_question(notes, question):
    try:

        question_words = set(
            question.lower().split()
        )

        notes_words = set(
            notes.lower().split()
        )

        matches = len(
            question_words.intersection(notes_words)
        )

        if matches == 0:
            return (
                "Information not available "
                "in uploaded notes."
            )

        prompt = f"""
Answer ONLY using the notes below.

If the answer is not present,
reply exactly:

Information not available in uploaded notes.

NOTES:
{notes[:15000]}

QUESTION:
{question}
"""

        response = model.generate_content(
            prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Error: {e}"