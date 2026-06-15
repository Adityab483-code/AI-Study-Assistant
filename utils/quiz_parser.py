import re


def parse_quiz(quiz_text):

    questions = []

    blocks = re.split(
        r"Q\d+\.",
        quiz_text
    )

    for block in blocks[1:]:

        try:

            lines = [
                line.strip()
                for line in block.split("\n")
                if line.strip()
            ]

            question = lines[0]

            options = []

            answer = ""

            explanation = ""

            for line in lines[1:]:

                if (
                    line.startswith("A)")
                    or line.startswith("B)")
                    or line.startswith("C)")
                    or line.startswith("D)")
                ):

                    options.append(line)

                elif line.startswith(
                    "Answer:"
                ):

                    answer = (
                        line.replace(
                            "Answer:",
                            ""
                        )
                        .strip()
                    )

                elif line.startswith(
                    "Explanation:"
                ):

                    explanation = (
                        line.replace(
                            "Explanation:",
                            ""
                        )
                        .strip()
                    )

            questions.append(
                {
                    "question": question,
                    "options": options,
                    "answer": answer,
                    "explanation": explanation
                }
            )

        except Exception:

            continue

    return questions
    print(questions[0])

    return questions