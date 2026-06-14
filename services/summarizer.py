from utils.llm import generate_response


def generate_summary(notes):

    prompt = f"""
    Summarize these notes in simple language.

    Notes:
    {notes}
    """

    return generate_response(
    prompt
)