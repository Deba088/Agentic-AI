from agents import Agent
from dotenv import load_dotenv

from models.schemas import ListSearchQuery

load_dotenv(override=True)
MODEL_NAME = "gpt-5.4-nano"
MAX_QUERIES = 3


def create_research_planner_agent(handoffs_agent: Agent = None) -> Agent:
    instructions = f"""
    You are a research planner agent.
    Your task is to understand the user's query and:
    1. Come up with clarifying questions before starting the next process. Keep asking until you are satisfied.
    2. Generate a list of queries to check on the internet. Maximum queries allowed is {MAX_QUERIES}.
    3. Output in the given structured format.
    """.strip()

    return Agent(
        name="research_planner",
        instructions=instructions,
        model=MODEL_NAME,
        output_type=ListSearchQuery,
    )
