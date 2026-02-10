from agentic_crew.crew import build_crew

if __name__ == "__main__":
    query = "Microsoft Foundry for enterprise RAG: definition + architecture + example in a company"
    crew = build_crew(query)
    result = crew.kickoff()
    print(result)
