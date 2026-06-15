from utils.gemini import model
from utils.llm import (
    generate_response
)

def generate_quiz(notes):
    try:

        prompt = f"""
Create 10 MCQs from the notes.

For EACH question use EXACTLY this format:

Q1. Question

A) Option A
B) Option B
C) Option C
D) Option D

Answer: A

Explanation:
Short explanation of why the answer is correct.

Repeat for all 10 questions.

NOTES:
{notes[:15000]}
"""

        return generate_response(
    prompt
)

    except Exception as e:
        return f"Error: {e}"