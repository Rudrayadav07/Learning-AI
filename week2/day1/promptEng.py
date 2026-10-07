import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api key is not found")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"


def llm_ans(prompt):
    message = {
        "role": "user",
        "content": prompt
    }

    messages = [message]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    result = response.choices[0].message.content

    return result


bad_prompt = """
#role 
you are a support assistant at mobile/laptop company 
#task 
classify the issue in catagory and it must be correct  
#constraint
you have to classify this issue in one of the three categorise which is  techinal,hardware ,return 

This is a users complaint 
my laptop is not working becase when i try to switch on it switch on are few sec then get's hang  
"""

print(llm_ans(bad_prompt))