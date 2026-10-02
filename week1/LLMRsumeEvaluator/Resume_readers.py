from pypdf import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        text.append(page_text)

    return "\n".join(text)