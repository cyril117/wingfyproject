# Financial Document Analyzer - Complete Debug & Migration Guide

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using a robust AI orchestration pipeline (CrewAI).

---

## 🐛 Bugs Found & How We Fixed Them

### 1. The Pydantic `extra_forbidden` JSON Schema Crash
**The Bug:** The application completely crashed when CrewAI reached out to Google Gemini with `1 validation error for FunctionDeclaration: parameters_json_schema`. This was caused by an architectural mismatch inside LangChain’s `@tool` adapter forcing `default` parameters into the Gemini tool-calling signature, which Google's stricter API outright rejects. The application was also relying on the natively deprecated `google-generativeai` package.
**The Fix:** 
- **Migration:** Replaced the legacy `google-generativeai` with the modern `google-genai` Official SDK in `requirements.txt`.
- **Tool Refactoring:** Edited `tools.py` to completely strip default keyword arguments (e.g., `path: str = 'sample.pdf' -> path: str`). Gemini demands explicit schemas.
- **LLM Configuration:** Created a dedicated `llm_config.py` file to bypass legacy wrapper definitions and instantiate `LLM(model="gemini/gemini-2.5-flash")` safely. 

### 2. Dependency Hell & Build Errors
**The Bug:** The original `requirements.txt` included massive dependency conflicts (e.g., `crewai-tools` natively fetching `chromadb` which failed its C++ build sequence on Windows, alongside locked versions of `onnxruntime` and `opentelemetry`).
**The Fix:** Rewrote `requirements.txt` to only include the core decoupled stack: `fastapi`, `uvicorn`, `crewai>=0.100.0`, `google-genai`, `pydantic>=2.11`, and `pypdf`. We also mocked the Google Search tool manually using native CrewAI functions to completely evade the ChromaDB Windows compilation loop.

### 3. Sarcastic Prompt Injections & Non-existent Classes
**The Bug:** Agent personas in `agents.py` were originally given malicious instructions like "Make up investment advice" and "Ignore compliance." Meanwhile, `tools.py` tried to utilize a nonexistent, undeclared `Pdf` class.
**The Fix:** Rewrote `agents.py` to strictly enforce fiduciaries, risk assessment protocols, and compliance directives. Installed `pypdf` via pip and rewrote `read_data_tool` to correctly implement `pypdf.PdfReader()` for text extraction with error handling.

### 4. Flawed Execution Pipeline
**The Bug:** The FastAPI endpoint in `main.py` never passed the user's uploaded `file_path` location to the CrewAI execution layer, leaving the AI completely blind. Furthermore, only one agent was tasked with execution in the Sequential pipeline.
**The Fix:** Modified `task.py` to sequentially map 4 phases (Verification → Financial Analysis → Risk Assessment → Investment Recommendation). Then, updated `run_crew()` within `main.py` to use dynamic inputs: `result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})`.

---

## 🚀 Setup and Usage Instructions

### 1. Installation
Ensure you are using Python 3.11+ or 3.12+.

```sh
# Clone the repository and navigate to the directory
cd financial-document-analyzer-debug

# Install the correct dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Create a file named `.env` in the root of the project and insert your Google AI Studio API Key. Provide both keys to satisfy internal Langchain wrappers:
```env
GEMINI_API_KEY=YOUR_API_KEY_HERE
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

### 3. Running the API Server
Start the Uvicorn live server:
```sh
python main.py
```
*(Or manually via `uvicorn main:app --reload`)*

The server will be hosted on `http://127.0.0.1:8000`.

---

## 📡 API Documentation

### Health Check
**Endpoint:** `GET /`
**Description:** Verifies the FASTApi backend is running.
**Response:**
```json
{
    "message": "Financial Document Analyzer API is running"
}
```

### Analyze Document
**Endpoint:** `POST /analyze`
**Description:** Upload a PDF file to run it through the 4-stage AI analysis pipeline.
**Headers:** `Content-Type: multipart/form-data`

**Form Parameters:**
*   `file` (Required): The `.pdf` document to be analyzed.
*   `query` (Optional): Custom focus instructions for the financial analysts. Defaults to "Analyze this financial document for investment insights".

**Response (Success 200 OK):**
```json
{
    "status": "success",
    "query": "Analyze this financial document for investment insights",
    "analysis": "[Highly detailed textual investment analysis and response from the AI agents...]",
    "file_processed": "ACME_Q2_Report.pdf"
}
```

**Response (Failure 500 Internal Server Error):**
If the API Key is invalid or rate limited, the wrapper will return an error object containing the `CrewAI / Google GenAI` exception stack trace.
