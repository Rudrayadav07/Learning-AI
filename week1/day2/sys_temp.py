import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key is not found")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"
role = "user"
prompt = "suggest one name"
message_system = {
    "role" : "system",
    "content" : "you are a brand manager who suggest brand name for my food brand",
}
message={
    "role" : role,
    "content" : prompt
}
messages = [message_system,message]

response = client.chat.completions.create(model=model, messages=messages,temperature = 2)
result = response.choices[0].message.content
print(result)