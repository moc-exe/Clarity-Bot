import os
from groq import Groq
def get_groq_client_ready() -> Groq:
    return Groq(api_key=os.getenv("GROQ_API_KEY"))
def get_response(client: Groq, req: str, model: str) -> list[str]: 


    completion = client.chat.completions.create(
    # model="mixtral-8x7b-32768",
    model = f"{model}",
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
    
    result = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        result += content

    print(result, end ="\n\n\n\n")
    out = []
    start = 0
    end = 1500
    if len(result) > 1500: 
        while start < len(result):
            out.append(result[start:end])
            start = end
            end += 1500
    else:
        out.append(result)
    return out