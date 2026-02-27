import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.2
)
