from crewai import Crew, Task
from .agents.research import build_research_agent
from .agents.analyst import build_analyst_agent
from .agents.report import build_report_agent

def build_crew(user_query: str) -> Crew:
    researcher = build_research_agent()
    analyst = build_analyst_agent()
    reporter = build_report_agent()

    t1 = Task(
        description=f"Use Serper web search to research: {user_query}. Provide sources (URLs).",
        expected_output="Findings with sources (URLs).",
        agent=researcher,
    )

    t2 = Task(
        description="Analyze the findings and extract key insights.",
        expected_output="Structured insights and summary.",
        agent=analyst,
        context=[t1],
    )

    t3 = Task(
        description="Write a professional report with Executive Summary, Key Insights, Technical Analysis, Recommendations. Add sources (URLs).",
        expected_output="Markdown report with sources.",
        agent=reporter,
        context=[t2],
        output_file="output/final_report.md",
    )

    return Crew(
        agents=[researcher, analyst, reporter],
        tasks=[t1, t2, t3],
        verbose=True,
    )
