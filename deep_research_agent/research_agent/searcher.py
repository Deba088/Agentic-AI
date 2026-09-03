from agents import Agent, WebSearchTool
from dotenv import load_dotenv

from models.schemas import SearchResult

load_dotenv(override=True)
MODEL_NAME = "gpt-5.4-nano"


def create_searcher_agent() -> Agent:
    instructions = """
    You are a research searcher agent.
    For each search query you receive, use the web_search tool to find relevant
    information and summarize what you find, keeping track of your sources.
    """.strip()

    return Agent(
        name="searcher",
        instructions=instructions,
        model=MODEL_NAME,
        tools=[WebSearchTool()],
        output_type=SearchResult,
    )
