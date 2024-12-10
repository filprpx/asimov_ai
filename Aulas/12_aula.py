import json
import time
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

vector_id = "vs_iIilXBdmfjbtf9FtIjGaRXap"

if vector_id:
    vector_store = client.beta.vector_stores.retrieve(vector_store_id=vector_id)
else:
    vector_store = client.beta.vector_stores.create(name = "Apostilas Asimov")

print("Vector id", vector_store.id)


# Comentado para não fazer upload toda a vez 
# files = ["Arquivos/Explorando a API da OpenAI.pdf", "Arquivos/Explorando o Universo das IAs com Hugging Face.pdf"]

# file_stream = [open(f, "rb") for f in files]

# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#     vector_store_id=vector_store.id,
#     files=file_stream,
# )

assistant_id = "asst_PuLhM1GntSUWJaOI4JpamunT"

# Criando assistant, também pode ser feito pela interface
if assistant_id:
    assistant = client.beta.assistants.retrieve(
        assistant_id=assistant_id
    )
else:
    assistant = client.beta.assistants.create(
        name="Tutor Asimov",
        instructions="Você é um tutor de uma escola de programacão. Você é ótimo para response \
            perguntas teóricas sobre a api da OpenAI e sobre a utilizacão da biblioteca do hugging \
            face com python. Você utiliza as apostilas dos cursos para basear suas respostas. Caso \
            você não encontre as respostas nas apostilas informadas, você fala que não sabe responder.",
        tools=[{'type': 'file_search'}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        model='gpt-3.5-turbo-0125'
    )

print("Assistant id", assistant.id)



thread_id = ""
if thread_id:
    thread = client.beta.threads.retrieve(
        thread_id=thread_id
    )
else: 
    thread = client.beta.threads.create()

print("Thread id", thread.id)

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Segundo o documento fornecido, o que é o Hugging Face?"
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
                if tool_call.type == "file_search":
                    print(tool_call)

                elif tool_call.type == "code_interpreter":
                    print("------")
                    print(tool_call.code_interpreter.input)
                    if len(tool_call.code_interpreter.outputs):    
                        print("------")
                        print("Result")
                        print(tool_call.code_interpreter.outputs[0].logs)
        
        if step.step_details.type == "message_creation":
            message = client.beta.threads.messages.retrieve(
                thread_id=thread.id,
                message_id=step.step_details.message_creation.message_id,
            )
            print(message.content[0].text.value)

    print("Answer: ")
    print(mensagens.data[0].content[0].text.value)
else:
    print("Erro", run.status)


# Ao final da aula (Analisando arquivos PDF com Assistants Retrievel), ele monta um código para apontar as citacões aos arquivos