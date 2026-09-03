import asyncio

from agents import Runner

from models.schemas import ListSearchQuery, ResearchReport, SearchResult
from research_agent.planner import create_research_planner_agent
from research_agent.searcher import create_searcher_agent
from research_agent.writer import create_writer_agent

planner_agent = create_research_planner_agent()
searcher_agent = create_searcher_agent()
writer_agent = create_writer_agent()


async def plan_searches(query: str) -> ListSearchQuery:
    result = await Runner.run(planner_agent, query)
    return result.final_output_as(ListSearchQuery)


async def perform_search(search_query) -> SearchResult:
    result = await Runner.run(searcher_agent, search_query.query)
    return result.final_output_as(SearchResult)


async def write_report(query: str, search_results: list[SearchResult]) -> ResearchReport:
    findings = "\n\n".join(
        f"Query: {r.query}\nSummary: {r.summary}\nSources: {', '.join(r.sources)}"
        for r in search_results
    )
    prompt = f"Original query: {query}\n\nResearch findings:\n{findings}"
    result = await Runner.run(writer_agent, prompt)
    return result.final_output_as(ResearchReport)


async def run_research(query: str) -> ResearchReport:
    plan = await plan_searches(query)
    search_results = await asyncio.gather(
        *(perform_search(search) for search in plan.searches)
    )
    return await write_report(query, list(search_results))


if __name__ == "__main__":
    user_query = input("Enter your research query: ")
    report = asyncio.run(run_research(user_query))
    print(report.answer)
