from agents import Agent
from dotenv import load_dotenv

from models.schemas import ResearchReport

load_dotenv(override=True)
MODEL_NAME = "gpt-5.4-nano"


def create_writer_agent() -> Agent:
    instructions = """
    You are a research writer agent.
    You will receive the original user query along with a collection of search
    results gathered by the searcher agent. Analyze all the findings, resolve
    any contradictions, and write a clear, well-structured answer to the
    original query, citing sources where relevant.
    """.strip()

    return Agent(
        name="writer",
        instructions=instructions,
        model=MODEL_NAME,
        output_type=ResearchReport,
    )
