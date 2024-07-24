import os
from together import Together
from dotenv import load_dotenv


load_dotenv()
client = Together(api_key=os.getenv('TOGETHER_API_KEY'))


messages=[{
    "role": "user",
    "content": """Create a python flask webpage with a prompt input form. When the user submits the form it is stored in a messages.content field of this variable stream = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    messages=[{
        "role": "user",
        "content": "What some baby names.",
    }],
    max_tokens=512,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>"], 
    stream=True) 
    into together.ai. The 'stream' variable is processed like this 
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="", flush=True)
    The stream chunks should appear in realtime async on the same flask page as the input prompt.""",
}]

stream = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    messages=messages,
    max_tokens=512,
    temperature=0.7,
    top_p=0.7,
    top_k=50,
    repetition_penalty=1,
    stop=["<|eot_id|>"],
    stream=True
)

output = ""
for chunk in stream:
    # print(chunk.choices[0].delta.content or "", end="", flush=True)
    output += chunk.choices[0].delta.content or "" #, end="", flush=True

print(output)