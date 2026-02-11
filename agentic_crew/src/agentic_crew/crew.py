from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.rag_tool import RAGTool


from crewai_tools import SerperDevTool


@CrewBase
class AgenticCrew():
    """Multi-Agent Enterprise AI Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

   

    @agent
    def orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestrator'], 
            verbose=True,
            llm=None 
        
        )

    @agent
    def decision(self) -> Agent:
        return Agent(
            config=self.agents_config['decision'],
            verbose=True,
            llm=None 
        )

    @agent
    def rag(self) -> Agent:
     rag_tool = RAGTool()
     return Agent (
            role="Knowledge Retrieval Agent (RAG Specialist)",
            goal="Retrieve grounded information from internal documents",
            backstory="Specialist in enterprise document retrieval using vector search",
            verbose=True,
            allow_delegation=False,
            tools=[RAGTool()],
            llm=None                
    )

    @agent
    def research(self) -> Agent:
        return Agent(
            config=self.agents_config['research'],
            verbose=True,
            tools=[SerperDevTool()],
            llm=None 
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            verbose=True
        )

    @agent
    def report(self) -> Agent:
        return Agent(
            config=self.agents_config['report'],
            verbose=True
        )

    # =========================
    # TASKS
    # =========================

    @task
    def orchestrator_task(self) -> Task:
        return Task(
            config=self.tasks_config['orchestrator_task']
        )

    @task
    def decision_task(self) -> Task:
        return Task(
            config=self.tasks_config['decision_task']
        )

    @task
    def rag_task(self) -> Task:
        return Task(
            config=self.tasks_config['rag_task']
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task']
        )

    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'],
            output_file='output/final_report.md'
        )

    # =========================
    # CREW
    # =========================

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.orchestrator(),
                self.decision(),
                self.rag(),
                self.research(),
                self.analyst(),
                self.report(),
        ],
            tasks=[
                self.orchestrator_task(),
                self.decision_task(),
                self.rag_task(),        
                self.research_task(),   
                self.analysis_task(),
                self.report_task(),
        ],
        process=Process.sequential,
        verbose=True,
    )

