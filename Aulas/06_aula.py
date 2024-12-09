import openai, os
from dotenv import load_dotenv

load_dotenv(override=True)

client = openai.Client()

def geracao_texto_stream(messages, model="gpt-3.5-turbo-0125", max_tokens=1000, temperature=0):
    oResponse = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True
    )

    return oResponse


messages = [
    {"role": "user", "content":"Crie uma história sobre uma viagem a marte"}
]
oResponse = geracao_texto_stream(messages)

full_response = ""
for stream_response in oResponse:
    sResponse = stream_response.choices[0].delta.content
    if not sResponse: continue

    full_response += sResponse
    print(sResponse, end="")

