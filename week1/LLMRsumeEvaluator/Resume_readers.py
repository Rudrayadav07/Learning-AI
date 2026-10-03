import os
from pypdf import PdfReader
from docx import Document
def read_resume(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension == ".pdf":
        return read_pdf(file_path)
    elif extension == ".docx":
        return read_docx(file_path)
    else:
        print("unexpected document")
        
    


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        text.append(page_text)
    return "\n".join(text)


def read_docx(file_path):
    Documents = Document(file_path)
    text = []
    for paragraph in Documents.paragraphs:
        paragraph_text = paragraph.text
        text.append(paragraph_text) 
    return "\n".join(text) 