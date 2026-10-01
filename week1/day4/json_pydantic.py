import os 
import json
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
from pydantic import BaseModel
load_dotenv()


class Ticket(BaseModel):
    name:str
    email:str
    contact:int
    issue:str

schema = Ticket.model_json_schema()

response_format={
    "type":"json_object"
}

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api key not found")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"
system_prompt = f"""you have to extract the accurate data from this {schema} i need output in json format"""
message_system = {
    "role" : "system",
    "content": system_prompt
}
text = "hello my name is Rudra Yadav and i have an issue is my phone is not working please resolve it as fasst as you can i had an emergency i live in Indore and i have to go pune tommorow soo please and my email is rudraydav432@gmail.com and phone No. is 87701"
role = "user"
prompt = f"""This is a customer ticket please extract the personal information from this{text}"""

message = {
    "role": role,
    "content" : prompt
}

messages = [message_system,message]

response = client.chat.completions.create( model = model,messages = messages,response_format= response_format)
result = response.choices[0].message.content


raw_json = result
data_file = json.loads(raw_json)
ticket =Ticket(**data_file)

print(ticket.issue)
print(ticket.name)
print(ticket.contact)