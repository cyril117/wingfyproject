from crewai import Task
from agents import verifier, financial_analyst, risk_assessor, investment_advisor

verification = Task(
    description="Verify the uploaded financial document located at {file_path}",
    expected_output="Validation result",
    agent=verifier,
)

analyze_financial_document = Task(
    description="Analyze financial metrics and performance.",
    expected_output="Detailed financial analysis",
    agent=financial_analyst,
)

risk_assessment = Task(
    description="Assess financial risks based on the company's performance.",
    expected_output="Risk report",
    agent=risk_assessor,
)

investment_analysis = Task(
    description="Provide investment recommendation based on the combined analysis.",
    expected_output="Investment decision",
    agent=investment_advisor,
)