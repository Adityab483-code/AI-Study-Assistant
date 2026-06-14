from utils.llm import generate_response
from services.text_processor import chunk_text,build_grounded_prompt

def generate_summary(notes: str) ->str:
    text_chunks=chunk_text(notes,chunk_size=1200,overlap=150)
    combined_context="\n---CONTEXT SEPARATOR---\n".join(text_chunks)
    prompt = f"""
    you are an expert academic verification assistant.your goal is to write a highly detailed ,comprehensive ,and deeply structured summary based only on the verified source material provided below.
    
    CRITICAL ANTI-HALLUCINATION INSTRUCTIONS:
    1.rely only on the clear facts explicitly mentioned in the context.
    2.do no assume,explorate,or bring in outside historical or technical facts not written below.
    3.if a concept connot be verified directly from this text,completely ignore it.do not invent explanations.
    4.for every main point or definition you write, ensure it can be tracked straight back to a sentence in the text.

    --START OF VERIFIED SOURCE MATERIAL---
    {combined_context}
    ---END OF VERIFIED SOURCE MATERIAL---
    please structure your response beautifully using the following format:
    #1.comprehensive summary:
    [provide a deep,thorough or introduction ,5-6 sentences high-level overview of what this chapter/material covers based strictly on the text.]
     
    ---
    #2.key concepts:
    * **[core concept 1]**: detailed explanation of the core concept directly from the text.
    * **[core concept 2]**: detailed explanation of the core concept directly from the text.
    * [add as many terms as are present in the text]

    ---
    #3.chapter breakdown &details:
    * **important insight**:provide detailed bullet points on the specific sub topics ,processes or facts written in the material.
    * **supporting detail**:ensure nothing important from the text is omitted,keeping descriptions clear and thorough.
    
    DETAILED GROUNDED SUMMARY:
    """
    print("printing advanced structure summary and anti_hallucinationpipelines....")

    summary_output=generate_response(prompt)
    return summary_output