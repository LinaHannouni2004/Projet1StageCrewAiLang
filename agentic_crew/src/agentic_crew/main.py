from dotenv import load_dotenv
load_dotenv()

from crew import AgenticCrew


def run():

    query = """Selon la note d’opération, quelles sont les caractéristiques détaillées de la structure 
    de l’offre obligataire d’OCP SA, notamment le nombre d’obligations émises, leur valeur nominale, 
    le montant global de l’opération, ainsi que les spécificités des tranches A, B, C et D 
    (maturité, révision du taux et cotation) ?"""

    inputs = {
        "query": query
    }

    # --------------------------
    # 1️⃣ Run Orchestrator + Decision
    # --------------------------
    crew_instance = AgenticCrew()
    crew = crew_instance.crew()

    result = crew.kickoff(inputs=inputs)

    decision = str(result).upper()
    print("\n=== DECISION ===")
    print(decision)

    # --------------------------
    # 2️⃣ Intelligent Routing
    # --------------------------
    if "RAG" in decision:
        print("\n=== USING RAG PIPELINE ===")
        crew.tasks.append(crew_instance.rag_task())
        crew.tasks.append(crew_instance.analysis_task())

    elif "RESEARCH" in decision:
        print("\n=== USING RESEARCH PIPELINE ===")
        crew.tasks.append(crew_instance.research_task())
        crew.tasks.append(crew_instance.analysis_task())

    else:
        print("\n=== USING DIRECT RESPONSE ===")

    # Toujours finir par REPORT
    crew.tasks.append(crew_instance.report_task())

    # --------------------------
    # 3️⃣ Run Final Pipeline
    # --------------------------
    final_result = crew.kickoff(inputs=inputs)

    print("\n=== FINAL RESULT ===\n")
    print(final_result)


if __name__ == "__main__":
    run()
