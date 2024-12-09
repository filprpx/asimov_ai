import json
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

with open("Arquivos/chatbot_respostas.json", encoding="utf8") as f:
    json_respostas = json.load(f)

with open('Arquivos/chatbot_respostas.jsonl', 'w', encoding="utf8") as f:
    for entrada in json_respostas:
        resposta = {
            'resposta': entrada['resposta'],
            'categoria': entrada['categoria'],
            'fonte': 'AsimoBot'
        }
        entrada_jsonl = {
            'messages': [
                {'role': 'user', 'content': entrada['pergunta']},
                {'role': 'assistant', 'content': json.dumps(resposta, ensure_ascii=False, indent=2)}
            ]
        }
        json.dump(entrada_jsonl, f, ensure_ascii=False)
        f.write('\n')


file = client.files.create(
    file=open("Arquivos/chatbot_respostas.jsonl", "rb"),
    purpose="fine-tune"
)

breakpoint()

client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-3.5-turbo"
)

client.fine_tuning.jobs.list()