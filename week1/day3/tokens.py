import os 
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

load_dotenv()

my_api_key  = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api key not found")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"
role  ="user"
#system prompt
system_prompt = "you are a sciencetist"
message_system ={
    "role" : "system",
    "content": system_prompt
}

# 3 prompts 
prompt1= "hello"
prompt2 ="who is the greatest superhero of all time"
prompt3 ="tell me how to make jounural in detail 1000 words" 

prompts = [prompt1,prompt2,prompt3]
for prompt in prompts:
    message = {
    "role":role,
    "content" : prompt
    }
    messages = [message_system,message]
    result = response = client.chat.completions.create(model= model,messages=messages,max_tokens= 5000)
    usage = response.usage
    promptToken = usage.prompt_tokens
    CompletionsToken = usage.completion_tokens
    print(f"prompt:{prompt}-->your tokens :{promptToken} Completion Tokens:{CompletionsToken} total tokens:{promptToken+CompletionsToken} finishReason:{response.choices[0].finish_reason}")


messages = [message_system,message]
response = client.chat.completions.create(model= model,messages=messages)
result = response.choices[0].message.content
print(result)