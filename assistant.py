from openai import OpenAI
import os
import time

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

file = client.files.create(
    # file=open("solomoni_information.pdf", "rb"), 
    file=open("kurisu_voicelines.pdf", "rb"),
    purpose="assistants"
)

assistant = client.beta.assistants.create(
    name="Amadeus",
    instructions="kurisu_instructions.txt",
    tools = [{"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids=[file.id]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role="user",
    content="A bunch of theories are out there, but don't you think they're implausible?"#"You don't think it's a bunch of nonsense?"#"Do you think it's possible to build a time machine?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions=''

)

time.sleep(20)

run_status = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)
print(run_status)
print(run_status.status)
   
message_output = client.beta.threads.messages.list(
thread_id=thread.id
)

for msg in message_output.data:
    role = msg.role
    content = msg.content[0].text.value
    if role == "Assistant":
        role = "助手"
    print(f'{role.capitalize()}: {content}')