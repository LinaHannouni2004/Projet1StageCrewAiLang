from dotenv import load_dotenv
load_dotenv()
from crew import AgenticCrew
def run():
    query = " Le prospectus visé par l’AMMC est constitué par quoi ? Explique en détail. "
    inputs = {
        "query": query   
    }

    result = AgenticCrew().crew().kickoff(inputs=inputs)

    print("\n=== FINAL RESULT ===\n")
    print(result)


if __name__ == "__main__":
    run()


