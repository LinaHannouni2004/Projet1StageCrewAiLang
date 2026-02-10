from crewai_tools import SerperDevTool

def get_web_search_tool():
    # SerperDevTool lit SERPER_API_KEY depuis l'env
    return SerperDevTool(n_results=5)
