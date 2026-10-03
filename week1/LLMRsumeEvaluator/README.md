# LLM Resume Evaluator

A Python-based resume screening project that reads a candidate's resume in PDF or DOCX format, extracts structured information, and evaluates how well it matches a job description using Groq's LLM API.

## Overview

This project is designed to help automate the early stages of hiring by:

- Extracting relevant resume details such as education, skills, experience, and projects
- Comparing the candidate profile against a target job description
- Assigning a match score between 0 and 100
- Returning structured JSON output for easy integration into downstream systems

The application reads the resume file, sends the content to a language model, and formats the output using Pydantic schemas.

## Features

- Resume parsing for PDF and DOCX files
- Structured JSON schema for job descriptions and resumes
- LLM-powered comparison against hiring requirements
- Match scoring and rationale generation
- Easy configuration through environment variables

## Tech Stack

- Python 3.12+
- Groq API
- Pydantic
- pypdf
- python-docx
- python-dotenv

## Project Structure

```text
LLMRsumeEvaluator/
├── main.py                 # Main script for evaluating a resume
├── Resume_readers.py       # Resume parsing logic for PDF/DOCX
├── Schema.py               # Pydantic schema definitions
├── Resumes/                # Sample resume files
├── .env                    # Environment variables (not committed)
├── pyproject.toml          # Python project configuration
├── README.md               # Project documentation
└── .venv/                  # Local virtual environment
```

## Setup

1. Clone the repository and go to the project folder.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install the dependencies:

```bash
python -m pip install -U pip
python -m pip install -e .
```

If you use `uv`, you can also run:

```bash
uv sync
```

## Environment Variables

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

1. Place the resume you want to evaluate in the `Resumes/` folder or update the path in `main.py`.
2. Edit the job description inside `main.py` to match the role you want to evaluate for.
3. Run the script:

```bash
python main.py
```

The project currently uses this resume path by default:

```python
text = read_resume('Resumes/New_Resume.pdf')
```

You can change it to another file, such as:

```python
text = read_resume('Resumes/my_resumeee.pdf')
```

## Example Output

The script prints a JSON object containing:

- extracted resume details
- matched skills and education
- experience summary
- score from 0 to 100
- short explanation of the evaluation

## Important Notes

- The Groq API key must be valid or the script will raise an error.
- The job description is currently hardcoded in `main.py`.
- The model is set to `openai/gpt-oss-120b` and can be adjusted as needed.

## Limitations

This is a small prototype and is best suited for learning and experimentation. It does not yet include:

- a web UI
- multi-resume bulk processing
- database storage
- robust validation for malformed resume files
- advanced recruiter workflow features

## Future Enhancements

Possible improvements include:

- adding a web-based dashboard
- supporting resume batch evaluation
- saving evaluation results to JSON/CSV
- ranking multiple candidates for a job
- integrating with job portals or ATS systems

## License

This project is currently for educational and personal use.

## Author

Rudra Yadav
