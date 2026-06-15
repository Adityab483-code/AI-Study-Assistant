from utils.llm import generate_response


def generate_summary(notes):

    prompt = f"""
Create a professional study summary.

IMPORTANT RULES:
- Use proper line breaks.
- Leave ONE blank line between sections.
- Leave ONE blank line between bullet points.
- Never write everything in one paragraph.
- Never write section titles and content on the same line.

Format exactly like:

📖 OVERVIEW

Overview text here.

🎯 KEY CONCEPTS

• Point 1

• Point 2

• Point 3

🧠 IMPORTANT DEFINITIONS

• Term: Definition

• Term: Definition

🔑 KEY TAKEAWAYS

• Takeaway 1

• Takeaway 2

🚀 QUICK REVISION NOTES

• Revision Point 1

• Revision Point 2

NOTES:
{notes[:15000]}
"""

    return generate_response(
        prompt
    )