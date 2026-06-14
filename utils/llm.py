from utils.gemini import model
from utils.deepseek import client


def generate_response(prompt):

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception:

        print(
            "Using DeepSeek..."
        )

        response = (
            client.chat.completions.create(
                model="deepseek/deepseek-chat",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
        )