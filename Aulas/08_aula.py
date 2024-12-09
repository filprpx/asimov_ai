import openai, os, json
from dotenv import load_dotenv

load_dotenv(override=True)

client = openai.Client()

def obter_temperatura_atual(local, unidade="celsius"):
    if "são paulo" in local.lower():
        return json.dumps(
            {"local": "São Paulo", "temperatura": "32", "unidade": unidade}
            )
    elif "porto alegre" in local.lower():
        return json.dumps(
            {"local": "Porto Alegre", "temperatura": "25", "unidade": unidade}
            )
    elif "rio de janeiro" in local.lower():
        return json.dumps(
            {"local": "Rio de Janeiro", "temperatura": "35", "unidade": unidade}
            )
    else:
        return json.dumps(
            {"local": local, "temperatura": "unknown"}
            )


tools = [
        {
            "type": "function",
            "function": {
                "name": "obter_temperatura_atual",
                "description": "Obtém a temperatura atual em uma dada cidade",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "local": {
                            "type": "string",
                            "description": "O nome da cidade. Ex: São Paulo",
                        },
                        "unidade": {
                            "type": "string", 
                            "enum": ["celsius", "fahrenheit"]
                        },
                    },
                    "required": ["local"],
                },
            },
        }
    ]

funcoes_disponiveis = {
        "obter_temperatura_atual": obter_temperatura_atual,
    }

mensagens = [
    {"role": "user", 
     "content": "Qual é a temperatura em São Paulo e Porto Alegre?"}
    ]

resposta = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=mensagens,
    tools=tools,
    tool_choice="auto",
)
mensagem_resp = resposta.choices[0].message
tool_calls = mensagem_resp.tool_calls

if tool_calls:
    mensagens.append(mensagem_resp)
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = funcoes_disponiveis[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            local=function_args.get("local"),
            unidade=function_args.get("unidade"),
        )
        mensagens.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )
    segunda_resposta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=mensagens,
    )

mensagem_resp = segunda_resposta.choices[0].message
print(mensagem_resp.content)