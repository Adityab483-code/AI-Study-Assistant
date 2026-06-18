from utils.gemini import model
from utils.deepseek import client


def generate_response(prompt):
    # ── FIX: handle missing Gemini model gracefully ──
    if model is not None:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini failed ({e}), falling back to DeepSeek...")

    # Fallback to DeepSeek / OpenRouter
    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Both AI providers failed. Please check your API keys.\n\nError: {e}"
