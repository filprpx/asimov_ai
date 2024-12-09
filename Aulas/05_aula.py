import openai, os
from dotenv import load_dotenv

load_dotenv(override=True)

def geracao_texto(messages, model="gpt-3.5-turbo-0125", max_tokens=1000, temperature=0):
    oResponse = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature
    )

    sResponse = oResponse.choices[0].message.content
    messages.append(oResponse.choices[0].message.model_dump(exclude_none=True))

    return sResponse, messages, oResponse



# Looks for the env variable OPENAI_API_KEY
client = openai.Client()

messages = [
    {"role": "user", "content":"O que é uma maça em 5 palavras?"}
]


sResponse, messages, oResponse = geracao_texto(messages)
print(sResponse)
messages.append({"role":"user", "content": "E qual a sua cor?"})
sResponse, messages, oResponse = geracao_texto(messages)
print(sResponse)

## Explorando response
print("\nExplorando response")

# Informacoes de consumo de tokens
print("\n Consumo de tokens")
print(oResponse.usage) # CompletionUsage(completion_tokens=11, prompt_tokens=42, total_tokens=53, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0))

# Retorna última resposta do modelo no formato para se inserir nas messages
print("\n Message dump")
print(oResponse.choices[0].message.model_dump(exclude_none=True)) # {'content': 'Vermelha, verde ou amarela.', 'role': 'assistant'}

# max_tokens => limita a quantidade de tokens da resposta
# temperature => controla a "criatividade" da resposta 0-2 (menos criativo - mais criativo)
