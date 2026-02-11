import time
from urllib import response
from agents.decision import DecisionAgent
from rag import RAGAgent

from agents.research import ResearchAgent
from agents.analyst import AnalystAgent
from agents.report import ReportAgent
from agents.direct import DirectAgent



class OrchestratorAgent:
    def __init__(self):
        self.decision_agent = DecisionAgent()
        self.rag_agent = RAGAgent()
        self.research_agent = ResearchAgent()
        self.analyst_agent = AnalystAgent()
        self.report_agent = ReportAgent()
        self.direct_agent = DirectAgent()


        self.state = {
            "query": None,
            "decision": None,
            "reason": None,
            "confidence": None,
            "route": None,
            "raw_data": None,
            "analysis": None,
            "report": None,
            "trace": [],
            "start_time": None,
            "end_time": None
        }

    # ---------- LOG ----------
    def log(self, msg):
        print(f"[Orchestrator] {msg}")

    # ---------- TRACE ----------
    def trace(self, step, data=None):
        self.state["trace"].append({
            "step": step,
            "time": time.time(),
            "data": data
        })

    # ---------- ROUTING ----------
    def route(self, decision, query):
        if decision == "RAG":
            self.log("Routing → RAG Agent")
            self.trace("route_rag")
            return self.rag_agent.run(query)

        elif decision == "RESEARCH":
            self.log("Routing → Research Agent")
            self.trace("route_research")
            return self.research_agent.run(query)

        else:
            self.log("Routing → Direct Agent (Gemini reasoning)")
            self.trace("route_direct")

            response = self.direct_agent.run(query)
            return response


    # ---------- MAIN ----------
    def run(self, query):
        self.state["query"] = query
        self.state["start_time"] = time.time()

        self.log("Starting workflow")
        self.trace("start", query)

        # 1️ Decision
        decision_result = self.decision_agent.run(query)
        self.state["decision"] = decision_result["decision"]
        self.state["reason"] = decision_result["reason"]
        self.state["confidence"] = decision_result["confidence"]

        self.log(f"Decision → {self.state['decision']}")
        self.trace("decision", decision_result)

        # 2️ Retrieve data
        raw_data = self.route(self.state["decision"], query)
        self.state["raw_data"] = raw_data
        self.trace("data_retrieved", raw_data[:200] if isinstance(raw_data, str) else raw_data)

        # 3️ Analysis
        self.log("Running Analyst Agent")
        analysis = self.analyst_agent.run(query, raw_data)
        self.state["analysis"] = analysis
        self.trace("analysis_done")

        # 4️ Report generation
        self.log("Generating Report")
        report = self.report_agent.run(query, analysis)
        self.state["report"] = report
        self.trace("report_generated")

        # 5️ End
        self.state["end_time"] = time.time()
        duration = self.state["end_time"] - self.state["start_time"]

        self.log(f"Workflow completed in {duration:.2f}s")
        self.trace("end", {"duration": duration})

        return {
            "decision": self.state["decision"],
            "reason": self.state["reason"],
            "confidence": self.state["confidence"],
            "report": report,
            "trace": self.state["trace"]
        }
