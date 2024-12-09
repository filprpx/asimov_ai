import openai, os
from dotenv import load_dotenv

load_dotenv(override=True)

client = openai.Client()

def geracao_texto(messages, model="gpt-3.5-turbo-0125", max_tokens=1000, temperature=0):
    oResponse = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True
    )

    full_response = ""
    print("Assistant: ", end="")
    for stream_response in oResponse:
        sResponse = stream_response.choices[0].delta.content
        if not sResponse: continue
    
        full_response += sResponse
        print(sResponse, end="")

    print()

    messages.append({"role":"assistant", "content": full_response})

    return messages

messages = []
while user_message := input("\nUser: "):
    if not user_message: continue

    messages.append({"role":"user", "content": user_message})
    messages = geracao_texto(messages)
    

