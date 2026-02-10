from crewai import Agent
from ..llm import build_llm

def build_report_agent():
    return Agent(
        role="Report Writer",
        goal="Generate a professional structured report with sources.",
        backstory="Expert in business writing.",
        llm=build_llm(),
        verbose=True,
    )
