from crewai import Agent
from llm_config import gemini_llm
from tools import read_financial_pdf, analyze_investment, assess_risk

verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify authenticity and structure of financial documents",
    backstory="Expert financial auditor",
    llm=gemini_llm,
    tools=[read_financial_pdf],
)

financial_analyst = Agent(
    role="Financial Analyst",
    goal="Analyze company performance",
    backstory="Investment banking analyst",
    llm=gemini_llm,
    tools=[analyze_investment],
)

risk_assessor = Agent(
    role="Risk Analyst",
    goal="Evaluate financial risk",
    backstory="Risk management expert",
    llm=gemini_llm,
    tools=[assess_risk],
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide final investment recommendation",
    backstory="Senior portfolio strategist",
    llm=gemini_llm,
)
