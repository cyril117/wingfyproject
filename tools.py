from crewai.tools import tool
from pypdf import PdfReader

@tool
def read_financial_pdf(path: str) -> str:
    """Read a financial PDF document and return its text."""
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

@tool
def analyze_investment(data: str) -> str:
    """Analyze investment insights from financial data."""
    return f"Investment analysis based on {len(data)} characters."

@tool
def assess_risk(data: str) -> str:
    """Assess financial risk from document data."""
    return f"Risk assessment generated for {len(data)} characters."