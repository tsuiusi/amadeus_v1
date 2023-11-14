from openai import OpenAI
import os
import time

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

name = "Amadeus"
with open('instructions.txt', 'r') as f:
    instructions = f.read()
filename = "kurisu_voicelines.pdf"
knowledge = client.files.create(
    file=open(filename, 'rb'),
    purpose='assistants'
)


assistant = client.beta.assistants.create(
    name=name,
    instructions=instructions,
    tools = [{"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[knowledge.id]
)

thread = client.beta.threads.create()

# message = client.beta.threads.messages.create(
#     thread_id = thread.id,
#     role="user",
#     content="Do you think it's possible to build a time machine?"
# )

while True:
    message = input("User: ")
    if message == "break":
        break

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role="user",
        content=message
    )   

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        if run_status.status == "completed":
            break
        time.sleep(1)
    
    message_output = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for msg in message_output.data:
        role = msg.role
        content = msg.content[0].text.value
        if role == "assistant":
            role = "助手"
            print(f'{role.capitalize()}: {content}')
            break
