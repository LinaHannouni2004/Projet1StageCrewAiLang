from crewai import Agent
from ..llm import build_llm

def build_analyst_agent():
    return Agent(
        role="Analyst",
        goal="Extract insights and summarize.",
        backstory="Expert in analysis.",
        llm=build_llm(),
        verbose=True,
    )
