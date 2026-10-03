import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from Resume_readers import read_resume
import json
from Schema import jobSchema, ResumeSchema

load_dotenv()

text = read_resume('Resumes/New_Resume.pdf')
# print(text)

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api key not found")

response_format={
    "type":"json_object"
}
job_description = """
We are hiring a Backend Developer.

Required skills:
- Node.js
- Express.js
- MongoDB
- REST APIs
- JavaScript

Education:
B.Tech/B.E. in Computer Science or related field.

Experience:
0-2 years.

Preferred skills:
- Docker
- AWS
- Git
"""
client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"

system_Prompt = system_Prompt = f"""
You are a resume evaluator.

Your job is to:
1. Extract accurate information from the resume.
2. Compare the candidate against the provided {job_description}.
3. Give a match score from 0 to 100.

Return the extracted resume information according to this schema:

{ResumeSchema}

Do not invent information that is not present in the resume.
Return only valid JSON.
"""

message_system = {
    "role" : "system",
    "content":system_Prompt
}

role = "user"
prompt = f"""Use the following resume text:

{text}

Extract all relevant information from the resume and return it in JSON format according to this schema:

{ResumeSchema}

After extracting the resume information, evaluate how well this candidate matches the given job description.

Compare the candidate's:
- Skills
- Education
- Years of experience
- Work experience
- Projects

against the {job_description}.

Give the candidate a match score from 0 to 100.

Return:
1. The extracted resume information according to the schema.
2. The match score.
3. A brief explanation of why the candidate received that score.

Return only valid JSON."""

message={
    "role" : role,
    "content" : prompt 
}

messages = [message_system,message]
                                   
response = client.chat.completions.create(model=model,messages = messages,response_format= response_format)
result = response.choices[0].message.content
data = json.loads(result)

print(data)