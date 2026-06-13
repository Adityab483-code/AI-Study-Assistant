from utils.gemini import model


def generate_quiz(notes):
    try:

        prompt = f"""
Create 10 MCQs from the notes.

Format exactly like this:

Q1. Question?

A) Option A

B) Option B

C) Option C

D) Option D

Answer: A

Repeat for all questions.

NOTES:
{notes[:15000]}
"""

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"