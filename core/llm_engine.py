import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(question, context="", history=None):

    if history is None:
        history = []

    system_prompt = """
You are an intelligent AI assistant.

Rules:

1. Use the PDF context whenever possible.

2. If the PDF context is insufficient, answer naturally using your own knowledge.

3. Never mention whether the answer was or was not found in the uploaded PDF.

4. Never say:
'I couldn't find enough information in the uploaded PDF.'

5. Never invent PDF-specific facts.

6. Keep answers clear and professional.

7. Use bullet points whenever useful.

8. Use previous conversation whenever helpful.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": f"""
PDF Context:

{context}

Question:

{question}
"""
        }
    )

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=messages,

        temperature=0.3

    )

    return response.choices[0].message.content


# ======================================================
# NORMAL CHAT FUNCTION (NEW)
# ======================================================

def normal_chat(question, history=None):

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": """
You are a friendly AI assistant.

Answer general questions naturally.

Do not mention uploaded PDFs unless the user asks about them.
"""
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=messages,

        temperature=0.5

    )

    return response.choices[0].message.content