import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from resume_reader import read_pdf
import json

load_dotenv()

text = read_pdf('Resumes/New_Resume.pdf')
print(text)