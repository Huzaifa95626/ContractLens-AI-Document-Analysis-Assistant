# ContractLens — AI Document Analysis Assistant

ContractLens is a web application that helps users perform a first-pass review of contracts. Upload a PDF, DOCX, or TXT file to extract its text, receive a plain-language overview, and identify clause patterns that may deserve closer review.

> **Important:** ContractLens is an educational productivity tool, not a lawyer and not a substitute for legal advice. Its pattern-based flags can miss issues or flag language that is appropriate in context. Do not upload confidential or sensitive documents unless you understand and approve your deployment's data handling.

## Features

- Clean, responsive web interface
- Upload PDF, DOCX, and TXT documents (15 MB limit)
- Text extraction for supported file types
- Plain-language overview
- Heuristic screening for indemnity, unilateral changes, liability limits, renewals, termination, arbitration, confidentiality, payment, IP, and data-protection language
- Clause excerpts, attention levels, and suggested follow-up questions
- Screening indicator and review checklist
- Sample contract demo
- Optional OpenAI-generated summary using an API key
- Local fallback analysis works without an API key
- Uploaded documents are removed after the request is processed

## Technology

- Python 3
- Flask
- HTML, CSS, JavaScript
- pypdf and python-docx
- Optional OpenAI API integration

## Run locally

### 1. Install Python

Use Python 3.10 or newer. Verify:

```bash
python --version
```

### 2. Extract and open the project

Unzip the downloaded archive, open a terminal in the `ContractLens` folder, then create a virtual environment.

**Windows PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

**Linux/macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables (optional)

Copy `.env.example` to `.env`. The app works without an API key using local pattern-based analysis.

To enable AI-generated summaries, set `OPENAI_API_KEY` in `.env`. API usage may incur charges and document text is sent to the configured AI provider when this feature is enabled. Do not enable it for confidential documents unless permitted by your organization's policies.

### 5. Start the app

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser. Select **Explore a sample** to try the app without uploading a document.

## Project structure

```text
ContractLens/
├── app.py                 # Flask routes and upload handling
├── analyzer.py            # Text extraction and contract screening logic
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   └── results.html
├── static/
│   ├── app.js
│   └── style.css
└── uploads/               # Temporary processing directory
```

## How the analysis works

1. The application extracts readable text from the uploaded file.
2. Configured phrase patterns identify potential clause categories.
3. Each detected category is paired with an explanation and suggested follow-up.
4. If `OPENAI_API_KEY` is configured, an optional model generates a plain-language overview. If the API is unavailable, a local fallback summary is used.

The risk score is a **heuristic screening indicator only**. It is not calibrated, validated, or suitable for deciding whether a contract is legally safe.

## Current limitations

- Scanned/image-only PDFs need OCR before upload.
- The pattern scanner is not jurisdiction-aware and can miss important legal issues.
- Analysis history is kept in memory for the current process/session and is cleared on restart; this starter version is not a multi-user system.
- Authentication, database persistence, audit logs, malware scanning, production deployment configuration, and formal security review are not included.
- Use a production WSGI server and set a strong secret key before deploying.

## GitHub repository description

**ContractLens is an AI-assisted contract analysis web app that summarizes agreements, flags potentially important clauses, and provides plain-language review suggestions. Built with Python, Flask, HTML, CSS, and JavaScript, with optional OpenAI integration.**

Suggested GitHub topics:
`python` `flask` `artificial-intelligence` `document-analysis` `contract-review` `legaltech` `nlp` `openai` `web-application`

## Suggested first GitHub commit

```bash
git init
git add .
git commit -m "Build ContractLens contract analysis assistant"
```

## License

This project is provided as an educational starter project. Add a license file before redistributing it publicly.
