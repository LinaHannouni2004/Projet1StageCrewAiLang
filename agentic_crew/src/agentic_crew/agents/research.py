from crewai import Agent
from agentic_crew.tools.web_search_tool import get_web_search_tool
from ..llm import build_llm

def build_research_agent():
    return Agent(
        role="Researcher",
        goal="Search the web using tools and return reliable, structured findings with sources.",
        backstory="Expert in gathering external data and validating sources.",
        llm=build_llm(),
        tools=[get_web_search_tool()],
        verbose=True,
    )
