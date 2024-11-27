import openai, os, json
from dotenv import load_dotenv
import yfinance as yf

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

# messages = []
# while user_message := input("\nUser: "):
#     if not user_message: continue

#     messages.append({"role":"user", "content": user_message})
#     messages = geracao_texto(messages)

def retorna_cotacao_historico(ticker, period="1mo"):
    ticker_obj = yf.Ticker(f"{ticker}.SA")
    hist = ticker_obj.history(period=period)["Close"]
    hist.index = hist.index.strftime("%Y-%m-%d")
    hist = round(hist, 2)

    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]

    return hist.to_json()

        
ticker = "ABEV3"
period = "1y"

historico = retorna_cotacao_historico(ticker, period)
print(historico)

tools = [
    {
        "type": "function",
        "function": {
            "name": "retorna_cotacao_historico",
            "description": "Retorna a cotacão diária histórica para uma acão da bovespa",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "O ticker da acao. ex: 'ABEV3' para AMBEV, 'PETRO4' para petrobras e etc.",
                    },
                    "period": {
                        "type": "string", 
                        "description": 'O periodo que será retornado de dados históricos \
                                        sendo "1mo" equivalente a 1 mês de dados, \
                                        "1d" um dia e "1y um ano."',
                        "enum": ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]
                    },
                },
                "required": ["local"],
            },
        },
    }
]

funcoes_disponiveis = {
    "retorna_cotacao_historico": retorna_cotacao_historico
}

mensagens = [{'role': 'user', 'content': 'Qual é a cotação da ambev agora'}]

# Código feio, mané. TODO Fazer melhor
resposta = client.chat.completions.create(
    messages=mensagens,
    model='gpt-3.5-turbo-0125',
    tools=tools,
    tool_choice='auto'
)

tool_calls = resposta.choices[0].message.tool_calls

if tool_calls:
    mensagens.append(resposta.choices[0].message)
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        function_to_call = funcoes_disponiveis[func_name]
        func_args = json.loads(tool_call.function.arguments)
        func_return = function_to_call(**func_args)
        mensagens.append({
            'tool_call_id': tool_call.id,
            'role': 'tool',
            'name': func_name,
            'content': func_return
        })
    segunda_resposta = client.chat.completions.create(
        messages=mensagens,
        model='gpt-3.5-turbo-0125',
    )
    mensagens.append(segunda_resposta.choices[0].message)
    print(segunda_resposta.choices[0].message.content)

