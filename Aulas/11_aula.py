import json
import time
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()
assistant_id = "asst_VjtHSDatJeOsCS5vlfZHZj6o"

# Criando assistant, também pode ser feito pela interface
if assistant_id:
    assistant = client.beta.assistants.retrieve(
        assistant_id=assistant_id
    )
else:
    assistant = client.beta.assistants.create(
        name="Tutor de Matemática da Asimov",
        instructions="Você é um tutor pessoal de matemática da empresa Asimov. \
            Escreva e execute códigos para responder as perguntas de matemática que lhe forem solicitadas.",
        tools=[{"type":"code_interpreter"}],
        model="gpt-3.5-turbo-0125"
    )

thread_id = "thread_HKuBLj6pMqwh40xiCH7Mj0qp"
if thread_id:
    thread = client.beta.threads.retrieve(
        thread_id=thread_id
    )
else: 
    thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Se eu jogar um dado honesto 1000 vezes, qual a probabilidade de eu obter 150 vezes o número 6? Resolva com um código"
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="O nome do usuário é Filipe Guedes e ele é um usuário premium."
)

while run.status in ["queued", "in_progress", "cancelling"]:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

if run.status == "completed":
    mensagens = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    # print(mensagens)

    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id
    )
    print("Steps: ")
    for step in run_steps.data[::-1]:
        print("=== Step:", step.step_details.type)
        if step.step_details.type == "tool_calls":
            for tool_call in step.step_details.tool_calls:
                print("------")
                print(tool_call.code_interpreter.input)
                if len(tool_call.code_interpreter.outputs):    
                    print("------")
                    print("Result")
                    print(tool_call.code_interpreter.outputs[0].logs)
        
        if step.step_details.type == "message_creation":
            message = client.beta.threads.messages.retrieve(
                thread_id=thread_id,
                message_id=step.step_details.message_creation.message_id,
            )
            print(message.content[0].text.value)

    print("Answer: ")
    print(mensagens.data[0].content[0].text.value)
else:
    print("Erro", run.status)