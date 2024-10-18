import os
from groqclient import Groq
def get_groq_client_ready() -> Groq:
    return Groq(api_key=os.getenv("GROQ_API_KEY"))
def get_response(client: Groq, req: str) -> str: 


    completion = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[
        {
            "role": "user",
            "content": f"{req}"
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None
    )
    
    out = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        out += content

    return out